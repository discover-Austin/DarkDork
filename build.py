#!/usr/bin/env python3
"""
DarkDork Build Script
Creates standalone executables for Windows, macOS, and Linux using PyInstaller

Usage:
    python build.py

Requirements:
    pip install pyinstaller
"""

import os
import sys
import platform
import subprocess


def build_executable():
    """Build standalone executable using PyInstaller"""

    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',  # Create a single executable file
        '--windowed',  # Don't show console window (GUI app)
        '--name=DarkDork',
        '--icon=icon.ico' if os.path.exists('icon.ico') else '',
        '--add-data=LICENSE:.',  # Include license file
        'darkdork.py'
    ]

    # Remove empty icon parameter if no icon exists
    cmd = [arg for arg in cmd if arg]

    print("Building DarkDork executable...")
    print(f"Platform: {platform.system()}")
    print(f"Architecture: {platform.machine()}")
    print()

    try:
        subprocess.run(cmd, check=True)
        print("\n" + "="*60)
        print("Build completed successfully!")
        print("="*60)
        print(f"\nExecutable location: dist/DarkDork{'.exe' if platform.system() == 'Windows' else ''}")
        print("\nDistribution files:")
        print("  - Copy the executable from the 'dist' folder")
        print("  - Include the LICENSE file")
        print("  - Include README.md for documentation")

    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("\nError: PyInstaller not found!", file=sys.stderr)
        print("Install it with: pip install pyinstaller", file=sys.stderr)
        sys.exit(1)


def create_installer_script():
    """Create platform-specific installer scripts"""

    system = platform.system()

    if system == 'Windows':
        # Create Inno Setup script for Windows installer
        inno_script = """
; DarkDork Installer Script
; Requires Inno Setup: https://jrsoftware.org/isinfo.php

[Setup]
AppName=DarkDork
AppVersion=1.0.0
AppPublisher=Your Organization
AppPublisherURL=https://yourorganization.com
DefaultDirName={pf}\\DarkDork
DefaultGroupName=DarkDork
OutputDir=installers
OutputBaseFilename=DarkDork-Setup-Windows
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
LicenseFile=LICENSE

[Files]
Source: "dist\\DarkDork.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\DarkDork"; Filename: "{app}\\DarkDork.exe"
Name: "{group}\\Uninstall DarkDork"; Filename: "{uninstallexe}"
Name: "{commondesktop}\\DarkDork"; Filename: "{app}\\DarkDork.exe"

[Run]
Filename: "{app}\\DarkDork.exe"; Description: "Launch DarkDork"; Flags: nowait postinstall skipifsilent
"""
        with open('installer.iss', 'w') as f:
            f.write(inno_script)
        print("\nWindows installer script created: installer.iss")
        print("Use Inno Setup to compile: iscc installer.iss")

    elif system == 'Darwin':  # macOS
        # Create .app bundle structure
        print("\nFor macOS distribution:")
        print("1. Use the PyInstaller output in dist/")
        print("2. Create a .dmg using: hdiutil create -volname DarkDork -srcfolder dist/DarkDork.app -ov -format UDZO DarkDork.dmg")

    elif system == 'Linux':
        # Create .deb package structure
        print("\nFor Linux distribution:")
        print("1. Create a .deb package or AppImage")
        print("2. Or distribute the executable from dist/")


if __name__ == '__main__':
    print("="*60)
    print("DarkDork Build Script")
    print("="*60)
    print()

    build_executable()
    create_installer_script()

    print("\n" + "="*60)
    print("Next Steps:")
    print("="*60)
    print("1. Test the executable in dist/")
    print("2. Create installer packages for distribution")
    print("3. Sign the executables (important for commercial distribution)")
    print("4. Include LICENSE and README.md with distribution")
    print()
