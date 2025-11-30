#!/bin/bash

# Unified AI Vendor Setup and Run Script

echo "🤖 Unified AI Vendor Assistant"
echo "=============================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate || . .venv/Scripts/activate
echo "✓ Virtual environment activated"

# Install requirements
echo ""
echo "Installing dependencies..."
pip3 install -q -r requirements.txt
echo "✓ Dependencies installed"

# Check for .env file
echo ""
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Created .env file - Please edit it and add your API keys!"
    echo ""
    echo "Required API keys:"
    echo "  - OpenAI: OPENAI_API_KEY"
    echo "  - Azure OpenAI: AZURE_OPENAI_* variables"
    echo "  - Google Gemini: GEMINI_API_KEY"
    echo "  - GitHub Models: GITHUB_TOKEN"
    echo "  - AWS Bedrock: AWS credentials (aws configure)"
    echo ""
    echo "Edit .env now and re-run this script."
    exit 0
else
    echo "✓ .env file found"
fi

# Run the application
echo ""
echo "Starting Unified AI Vendor Assistant..."
echo "📱 Open http://localhost:5000 in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
