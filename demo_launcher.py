#!/usr/bin/env python3
"""
AI Meme Generator - Demo Launcher
Easy-to-use demo for presentations and showcasing

This launcher runs the meme generator in demo mode without requiring API keys.
Perfect for classroom demonstrations and presentations.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_banner():
    """Print a nice banner"""
    print(Colors.HEADER + Colors.BOLD)
    print("=" * 70)
    print("🎨 AI MEME GENERATOR - DEMO MODE")
    print("=" * 70)
    print(Colors.ENDC)
    print(Colors.OKCYAN + "Perfect for presentations and demonstrations!" + Colors.ENDC)
    print()


def check_requirements():
    """Check if basic requirements are met"""
    print(Colors.OKBLUE + "📋 Checking requirements..." + Colors.ENDC)

    # Check Python version
    if sys.version_info < (3, 8):
        print(Colors.FAIL + "❌ Python 3.8+ required" + Colors.ENDC)
        return False
    print(Colors.OKGREEN + "✓ Python version OK" + Colors.ENDC)

    # Check if required files exist
    required_files = ['app.py', 'demo_mode.py', 'template_selector.py', 'meme_creator.py']
    for file in required_files:
        if not os.path.exists(file):
            print(Colors.FAIL + f"❌ Missing file: {file}" + Colors.ENDC)
            return False
    print(Colors.OKGREEN + "✓ All required files present" + Colors.ENDC)

    # Check if memes.json exists
    if not os.path.exists('memes.json'):
        print(Colors.WARNING + "⚠️  memes.json not found" + Colors.ENDC)
        if os.path.exists('memes.json.zip'):
            print(Colors.OKBLUE + "📦 Extracting memes.json.zip..." + Colors.ENDC)
            try:
                import zipfile
                with zipfile.ZipFile('memes.json.zip', 'r') as zip_ref:
                    zip_ref.extractall('.')
                print(Colors.OKGREEN + "✓ Dataset extracted" + Colors.ENDC)
            except Exception as e:
                print(Colors.FAIL + f"❌ Failed to extract: {e}" + Colors.ENDC)
                return False
        else:
            print(Colors.FAIL + "❌ Dataset file missing" + Colors.ENDC)
            return False
    else:
        print(Colors.OKGREEN + "✓ Dataset ready" + Colors.ENDC)

    return True


def install_dependencies():
    """Install required dependencies"""
    print()
    print(Colors.OKBLUE + "📦 Installing dependencies..." + Colors.ENDC)

    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '--user', '--quiet',
            'flask', 'pillow', 'requests', 'python-dotenv'
        ])
        print(Colors.OKGREEN + "✓ Dependencies installed" + Colors.ENDC)
        return True
    except subprocess.CalledProcessError as e:
        print(Colors.WARNING + f"⚠️  Some dependencies may already be installed" + Colors.ENDC)
        return True
    except Exception as e:
        print(Colors.FAIL + f"❌ Failed to install dependencies: {e}" + Colors.ENDC)
        return False


def create_demo_env():
    """Create a .env file for demo mode"""
    if not os.path.exists('.env'):
        print(Colors.OKBLUE + "📝 Creating demo configuration..." + Colors.ENDC)
        with open('.env', 'w') as f:
            f.write('# AI Meme Generator - Demo Mode Configuration\n')
            f.write('FLASK_ENV=development\n')
            f.write('PORT=5000\n')
            f.write('# Demo mode - no API key required\n')
            f.write('DEMO_MODE=true\n')
        print(Colors.OKGREEN + "✓ Configuration created" + Colors.ENDC)


def run_demo():
    """Run the demo application"""
    print()
    print(Colors.HEADER + Colors.BOLD + "=" * 70 + Colors.ENDC)
    print(Colors.OKGREEN + Colors.BOLD + "🚀 Starting AI Meme Generator..." + Colors.ENDC)
    print(Colors.HEADER + Colors.BOLD + "=" * 70 + Colors.ENDC)
    print()
    print(Colors.OKCYAN + "Demo features:" + Colors.ENDC)
    print("  • 81 popular meme templates")
    print("  • Pre-generated captions (no API key needed)")
    print("  • Simple web interface")
    print("  • Instant meme creation")
    print()
    print(Colors.WARNING + Colors.BOLD + "📍 Open your browser to: http://localhost:5000" + Colors.ENDC)
    print(Colors.WARNING + "   Press Ctrl+C to stop the server" + Colors.ENDC)
    print()
    print(Colors.HEADER + "=" * 70 + Colors.ENDC)
    print()

    time.sleep(2)

    # Set environment variable for demo mode
    os.environ['DEMO_MODE'] = 'true'
    os.environ['FLASK_ENV'] = 'development'

    # Run the app
    try:
        subprocess.run([sys.executable, 'app_demo.py'])
    except KeyboardInterrupt:
        print()
        print(Colors.OKGREEN + "\n✓ Demo stopped" + Colors.ENDC)
    except FileNotFoundError:
        # Fallback to regular app
        try:
            subprocess.run([sys.executable, 'app.py'])
        except KeyboardInterrupt:
            print()
            print(Colors.OKGREEN + "\n✓ Demo stopped" + Colors.ENDC)


def main():
    """Main demo launcher"""
    print_banner()

    # Check requirements
    if not check_requirements():
        print()
        print(Colors.FAIL + "❌ Requirements check failed" + Colors.ENDC)
        print(Colors.WARNING + "Please run: pip install -r requirements.txt" + Colors.ENDC)
        sys.exit(1)

    # Install dependencies
    print()
    response = input(Colors.OKBLUE + "Install/update dependencies? (y/n): " + Colors.ENDC)
    if response.lower() in ['y', 'yes', '']:
        if not install_dependencies():
            print(Colors.WARNING + "⚠️  Continuing anyway..." + Colors.ENDC)

    # Create demo config
    create_demo_env()

    # Create generated_memes directory
    os.makedirs('generated_memes', exist_ok=True)

    print()
    print(Colors.OKGREEN + Colors.BOLD + "✓ Demo ready!" + Colors.ENDC)
    print()

    # Wait for user
    input(Colors.OKBLUE + "Press Enter to start the demo... " + Colors.ENDC)

    # Run the demo
    run_demo()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(Colors.OKGREEN + "\n✓ Demo cancelled" + Colors.ENDC)
        sys.exit(0)
    except Exception as e:
        print()
        print(Colors.FAIL + f"❌ Error: {e}" + Colors.ENDC)
        sys.exit(1)
