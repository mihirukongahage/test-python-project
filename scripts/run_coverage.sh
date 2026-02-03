#!/bin/bash

echo "🧪 Running tests with coverage..."
echo ""

# Run tests with coverage
coverage run -m pytest test_todo.py -v

# Generate terminal report
echo ""
echo "📊 Coverage Report:"
echo "==================="
coverage report -m

# Generate HTML report
echo ""
echo "📄 Generating HTML report..."
coverage html

echo ""
echo "✅ Coverage analysis complete!"
echo ""
echo "View detailed HTML report:"
echo "  file://$(pwd)/htmlcov/index.html"
echo ""
echo "Or open with: xdg-open htmlcov/index.html"
