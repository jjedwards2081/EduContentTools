#!/usr/bin/env python3
"""
EduContentTools Launcher
Launch the application in CLI or GUI mode.
"""

import sys
import os


def check_gui_available():
    """Check if GUI can be launched."""
    try:
        # First check if tkinter module exists
        import tkinter
        return True, None
    except ImportError as e:
        return False, f"tkinter not installed: {str(e)}"
    except Exception as e:
        return False, f"tkinter module error: {str(e)}"


def main():
    """Launch the application."""
    # Check if GUI mode is explicitly requested
    if len(sys.argv) > 1 and sys.argv[1] == '--gui':
        # User explicitly wants GUI
        can_run_gui, error = check_gui_available()
        if not can_run_gui:
            print("=" * 70)
            print("ERROR: Cannot start GUI")
            print("=" * 70)
            print(f"\n{error}")
            print("\nPlease use CLI mode instead:")
            print("  python launcher.py --cli")
            print("  or")
            print("  python main.py")
            print("=" * 70)
            sys.exit(1)
        
        from gui_app import main as gui_main
        gui_main()
    
    elif len(sys.argv) > 1 and sys.argv[1] == '--cli':
        # Launch CLI explicitly
        from main import main as cli_main
        cli_main()
    
    else:
        # Default: Try GUI first, fall back to CLI
        # Note: We can't fully test Tk initialization without risking a crash
        # on systems with incompatible Tk, so we just launch CLI by default
        # Users who want GUI must explicitly request it with --gui
        print("=" * 70)
        print("EduContentTools - Starting in CLI mode")
        print("=" * 70)
        print("\nTo use GUI mode (if available), run:")
        print("  python launcher.py --gui")
        print("\nStarting CLI interface...")
        print("=" * 70)
        print()
        from main import main as cli_main
        cli_main()


if __name__ == "__main__":
    main()
