#!/usr/bin/env python3
"""
Custom dependency analyzer to detect circular imports.
Alternative to pydeps for this project.
"""

import ast
import os
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple


class DependencyAnalyzer:
    def __init__(self, package_path: str):
        self.package_path = Path(package_path)
        self.dependencies = defaultdict(list)
        self.module_files = {}
        
    def find_python_files(self) -> List[Path]:
        """Find all Python files in the package."""
        python_files = []
        for path in self.package_path.rglob("*.py"):
            if "__pycache__" not in str(path):
                python_files.append(path)
        return python_files
    
    def get_module_name(self, filepath: Path) -> str:
        """Convert file path to module name."""
        relative = filepath.relative_to(self.package_path.parent)
        parts = list(relative.parts)
        
        # Remove .py extension
        if parts[-1].endswith('.py'):
            parts[-1] = parts[-1][:-3]
        
        # Remove __init__
        if parts[-1] == '__init__':
            parts = parts[:-1]
        
        return '.'.join(parts)
    
    def parse_imports(self, filepath: Path) -> List[Tuple[str, int, str]]:
        """Parse imports from a Python file."""
        imports = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), str(filepath))
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return imports
        
        module_name = self.get_module_name(filepath)
        package_prefix = module_name.split('.')[0]
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    # Absolute import
                    if node.module.startswith(package_prefix):
                        imports.append((node.module, node.lineno, f"from {node.module} import ..."))
                    elif node.module.startswith('.'):
                        # Relative import with module
                        level = node.level
                        parts = module_name.split('.')
                        base_parts = parts[:-(level-1)] if level > 1 else parts[:-1] if level == 1 else parts
                        
                        if node.module != '.':
                            target_module = '.'.join(base_parts + [node.module[1:]])
                        else:
                            target_module = '.'.join(base_parts)
                        
                        imports.append((target_module, node.lineno, f"from {node.module} import ..."))
                elif node.level > 0:
                    # Relative import: from . import something
                    for alias in node.names:
                        parts = module_name.split('.')
                        level = node.level
                        base_parts = parts[:-(level-1)] if level > 1 else parts[:-1] if level == 1 else parts
                        target_module = '.'.join(base_parts + [alias.name])
                        imports.append((target_module, node.lineno, f"from . import {alias.name}"))
            
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith(package_prefix):
                        imports.append((alias.name, node.lineno, f"import {alias.name}"))
        
        return imports
    
    def analyze(self):
        """Analyze all dependencies in the package."""
        python_files = self.find_python_files()
        
        print(f"\n{'='*70}")
        print(f"ANALYZING DEPENDENCIES IN: {self.package_path}")
        print(f"{'='*70}\n")
        print(f"Found {len(python_files)} Python files\n")
        
        # Build dependency graph
        for filepath in python_files:
            module_name = self.get_module_name(filepath)
            self.module_files[module_name] = filepath
            imports = self.parse_imports(filepath)
            
            for target, lineno, import_str in imports:
                self.dependencies[module_name].append((target, lineno, import_str))
        
        return self
    
    def find_cycles(self) -> List[List[str]]:
        """Find circular dependencies using DFS."""
        cycles = []
        visited = set()
        rec_stack = []
        
        def dfs(node: str, path: List[str]):
            if node in rec_stack:
                # Found a cycle
                cycle_start = rec_stack.index(node)
                cycle = rec_stack[cycle_start:] + [node]
                cycles.append(cycle)
                return
            
            if node in visited:
                return
            
            visited.add(node)
            rec_stack.append(node)
            
            # Visit all dependencies
            for target, _, _ in self.dependencies.get(node, []):
                if target in self.module_files:  # Only follow internal modules
                    dfs(target, path + [node])
            
            rec_stack.pop()
        
        # Start DFS from each module
        for module in self.module_files:
            if module not in visited:
                dfs(module, [])
        
        return cycles
    
    def print_dependency_graph(self):
        """Print the complete dependency graph."""
        print(f"\n{'='*70}")
        print("DEPENDENCY GRAPH")
        print(f"{'='*70}\n")
        
        for module in sorted(self.dependencies.keys()):
            deps = self.dependencies[module]
            if deps:
                print(f"\n{module}:")
                for target, lineno, import_str in deps:
                    print(f"  → {target:30} (line {lineno:3})")
    
    def print_cycles(self):
        """Find and print circular dependencies."""
        print(f"\n{'='*70}")
        print("CIRCULAR DEPENDENCY DETECTION")
        print(f"{'='*70}\n")
        
        cycles = self.find_cycles()
        
        if not cycles:
            print("✓ No circular dependencies found!\n")
            return
        
        # Remove duplicate cycles
        unique_cycles = []
        seen = set()
        for cycle in cycles:
            # Normalize cycle to start with smallest module name
            normalized = tuple(sorted(set(cycle)))
            if normalized not in seen:
                seen.add(normalized)
                unique_cycles.append(cycle)
        
        print(f"⚠ Found {len(unique_cycles)} circular dependency cycle(s):\n")
        
        for i, cycle in enumerate(unique_cycles, 1):
            print(f"Cycle #{i}:")
            for j in range(len(cycle) - 1):
                print(f"  {cycle[j]}")
                print(f"    ↓")
            print(f"  {cycle[-1]}")
            print()


if __name__ == "__main__":
    import sys
    
    package_path = sys.argv[1] if len(sys.argv) > 1 else "todo"
    
    analyzer = DependencyAnalyzer(package_path)
    analyzer.analyze()
    analyzer.print_dependency_graph()
    analyzer.print_cycles()
