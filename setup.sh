#!/bin/bash

# Lecture Note Sharing Platform (LNSP) — Automated Setup Script
# This script sets up the development environment for both SQLite and MySQL.
# Usage: bash setup.sh

set -e  # Exit on any error

echo "=========================================="
echo "LNSP Setup — Automated Environment Config"
echo "=========================================="
echo ""

# Step 1: Create .env from .env.example if it doesn't exist
echo "📋 Step 1: Creating .env file..."
if [ -f .env ]; then
    echo "   ✓ .env already exists — skipping"
else
    cp .env.example .env
    echo "   ✓ .env created from .env.example"
    echo "   ⚠️  Please edit .env with your database credentials if using MySQL"
fi
echo ""

# Step 2: Create virtual environment
echo "🐍 Step 2: Creating Python virtual environment..."
if [ -d venv ]; then
    echo "   ✓ venv already exists — skipping"
else
    python3 -m venv venv
    echo "   ✓ venv created"
fi
echo ""

# Step 3: Activate virtual environment
echo "🔌 Step 3: Activating virtual environment..."
source venv/Scripts/activate
echo "   ✓ venv activated"
echo ""

# Step 4: Install dependencies
echo "📦 Step 4: Installing dependencies from requirements.txt..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "   ✓ Dependencies installed"
echo ""

# Step 5: Initialize database
echo "🗄️  Step 5: Initializing database..."
python init_db.py
echo "   ✓ Database initialized"
echo ""

# Step 6: Display next steps
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Activate venv (if not already active):"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the app:"
echo "     python run.py"
echo ""
echo "  3. Open browser and navigate to:"
echo "     http://localhost:5000"
echo ""
echo "To switch databases, edit .env and change DB_CONNECTION:"
echo "  - DB_CONNECTION=sqlite  (default)"
echo "  - DB_CONNECTION=mysql   (requires MySQL credentials in DATABASE_URL)"
echo ""
echo "=========================================="