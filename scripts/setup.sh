#!/bin/bash

echo "🚀 Setting up Todo Application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the application:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the app: python todo.py --help"
echo ""
echo "Example commands:"
echo "  python todo.py add 'Buy groceries' -p high"
echo "  python todo.py list"
echo "  python todo.py complete 1"
echo ""
