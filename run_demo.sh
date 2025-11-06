#!/bin/bash
# AI Meme Generator - Demo Launcher Script
# Double-click this file to run the demo (Linux/Mac)

echo "🎨 AI Meme Generator - Demo Launcher"
echo "===================================="
echo ""

# Make demo_launcher.py executable
chmod +x demo_launcher.py

# Run the demo
python3 demo_launcher.py

# Keep window open on error
if [ $? -ne 0 ]; then
    echo ""
    echo "Press Enter to exit..."
    read
fi
