# DarkDork Build and Distribution Guide

Complete guide for building and distributing DarkDork across all platforms.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Building for Windows](#building-for-windows)
4. [Building for macOS](#building-for-macos)
5. [Building for Linux](#building-for-linux)
6. [Code Signing](#code-signing)
7. [Creating Installers](#creating-installers)
8. [Distribution Checklist](#distribution-checklist)
9. [Troubleshooting](#troubleshooting)

---

## 1. Overview

### Build Process Summary

DarkDork can be distributed in multiple formats:
- **Standalone Executables** (Windows EXE, macOS App, Linux binary)
- **Python Package** (via pip/PyPI)
- **Installers** (MSI, DMG, DEB, RPM)
- **Portable Packages** (ZIP, TAR.GZ)

### Build Tools

- **PyInstaller** - Creates standalone executables
- **Inno Setup** (Windows) - Creates professional installers
- **DMG Canvas** (macOS) - Creates DMG installers
- **dpkg/rpm** (Linux) - Creates distribution packages

---

## 2. Prerequisites

### Common Requirements

```bash
# Install PyInstaller
pip install pyinstaller

# Optional: Install development dependencies
pip install -r requirements.txt
```

### Platform-Specific Tools

**Windows:**
- Visual Studio Build Tools (for advanced features)
- Inno Setup 6+ (for installer creation)
- SignTool (for code signing)

**macOS:**
- Xcode Command Line Tools
- DMG Canvas or create-dmg
- Developer ID certificate (for signing)

**Linux:**
- build-essential
- dpkg (Debian/Ubuntu)
- rpm-build (Fedora/RHEL)

---

## 3. Building for Windows

### Method 1: Automated Build

```batch
# Run the automated build script
python build.py
```

This creates `dist/DarkDork.exe`

### Method 2: Manual PyInstaller Build

```batch
# Basic build
pyinstaller --onefile --windowed --name DarkDork darkdork.py

# Advanced build with icon
pyinstaller ^
  --onefile ^
  --windowed ^
  --name DarkDork ^
  --icon=icon.ico ^
  --add-data "LICENSE;." ^
  darkdork.py
```

### Creating Windows Icon

1. Create or obtain a 256x256 PNG logo
2. Convert to ICO format using online tool or:

```python
# Using PIL/Pillow
from PIL import Image
img = Image.open('logo.png')
img.save('icon.ico', format='ICO', sizes=[(256, 256)])
```

### Building 32-bit Version

```batch
# Use 32-bit Python installation
# Then build normally
pyinstaller --onefile --windowed --name DarkDork darkdork.py
```

### Creating Windows Installer

#### Using Inno Setup

1. Install Inno Setup from https://jrsoftware.org/isinfo.php
2. Use the included `installer.iss` script
3. Open in Inno Setup Compiler
4. Click Build → Compile
5. Installer created in `installers/` folder

**Custom Installer Script:**

```iss
; DarkDork Windows Installer
#define AppName "DarkDork"
#define AppVersion "1.0.0"
#define AppPublisher "Your Organization"
#define AppURL "https://yourorganization.com"
#define AppExeName "DarkDork.exe"

[Setup]
AppId={{YOUR-GUID-HERE}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=installers
OutputBaseFilename=DarkDork-Setup-{#AppVersion}-Windows
SetupIconFile=icon.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent
```

### Windows Build Checklist

- [ ] Build 64-bit executable
- [ ] Build 32-bit executable (optional)
- [ ] Test on Windows 10
- [ ] Test on Windows 11
- [ ] Sign executables (for commercial distribution)
- [ ] Create installer
- [ ] Sign installer
- [ ] Test installer
- [ ] Create portable ZIP package

### Creating Portable ZIP Package

```batch
# Create distribution folder
mkdir DarkDork-Portable
copy dist\DarkDork.exe DarkDork-Portable\
copy LICENSE DarkDork-Portable\
copy README.md DarkDork-Portable\
xcopy /E /I docs DarkDork-Portable\docs

# Create ZIP (using 7-Zip or PowerShell)
powershell Compress-Archive -Path DarkDork-Portable -DestinationPath DarkDork-1.0.0-Windows-Portable.zip
```

---

## 4. Building for macOS

### PyInstaller Build

```bash
# Basic build
python3 -m PyInstaller --onefile --windowed --name DarkDork darkdork.py

# Advanced build with icon
python3 -m PyInstaller \
  --onefile \
  --windowed \
  --name DarkDork \
  --icon=icon.icns \
  --add-data "LICENSE:." \
  darkdork.py
```

### Creating macOS Icon

1. Create 1024x1024 PNG logo
2. Convert to ICNS:

```bash
# Create iconset
mkdir icon.iconset
sips -z 16 16     logo.png --out icon.iconset/icon_16x16.png
sips -z 32 32     logo.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     logo.png --out icon.iconset/icon_32x32.png
sips -z 64 64     logo.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   logo.png --out icon.iconset/icon_128x128.png
sips -z 256 256   logo.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   logo.png --out icon.iconset/icon_256x256.png
sips -z 512 512   logo.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   logo.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 logo.png --out icon.iconset/icon_512x512@2x.png

# Convert to ICNS
iconutil -c icns icon.iconset
```

### Creating DMG Installer

#### Method 1: Using create-dmg

```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
  --volname "DarkDork" \
  --volicon "icon.icns" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "DarkDork.app" 175 120 \
  --hide-extension "DarkDork.app" \
  --app-drop-link 425 120 \
  "DarkDork-1.0.0-macOS.dmg" \
  "dist/DarkDork.app"
```

#### Method 2: Manual DMG Creation

```bash
# Create temporary DMG
hdiutil create -size 100m -fs HFS+ -volname "DarkDork" temp.dmg

# Mount it
hdiutil attach temp.dmg

# Copy application
cp -R dist/DarkDork.app "/Volumes/DarkDork/"
cp LICENSE "/Volumes/DarkDork/"
cp README.md "/Volumes/DarkDork/"

# Create symlink to Applications
ln -s /Applications "/Volumes/DarkDork/Applications"

# Unmount
hdiutil detach "/Volumes/DarkDork"

# Convert to compressed DMG
hdiutil convert temp.dmg -format UDZO -o DarkDork-1.0.0-macOS.dmg

# Clean up
rm temp.dmg
```

### macOS Build Checklist

- [ ] Build for Intel (x86_64)
- [ ] Build for Apple Silicon (arm64) if possible
- [ ] Create universal binary (optional)
- [ ] Test on macOS 10.14+
- [ ] Test on Apple Silicon Mac
- [ ] Sign application
- [ ] Notarize with Apple
- [ ] Create DMG installer
- [ ] Test DMG installation

### Creating Universal Binary

```bash
# Build for Intel
arch -x86_64 python3 -m PyInstaller darkdork.spec

# Build for ARM
arch -arm64 python3 -m PyInstaller darkdork.spec

# Combine (requires lipo tool)
lipo -create -output DarkDork \
  dist/DarkDork-x86_64 \
  dist/DarkDork-arm64
```

---

## 5. Building for Linux

### PyInstaller Build

```bash
# Basic build
python3 -m PyInstaller --onefile --name DarkDork darkdork.py

# Build without console window
python3 -m PyInstaller --onefile --windowed --name DarkDork darkdork.py
```

### Creating .deb Package (Debian/Ubuntu)

#### Package Structure

```
darkdork_1.0.0/
├── DEBIAN/
│   ├── control
│   ├── postinst
│   └── prerm
├── usr/
│   ├── bin/
│   │   └── darkdork
│   ├── share/
│   │   ├── applications/
│   │   │   └── darkdork.desktop
│   │   ├── icons/
│   │   │   └── hicolor/
│   │   │       └── 256x256/
│   │   │           └── apps/
│   │   │               └── darkdork.png
│   │   └── doc/
│   │       └── darkdork/
│   │           ├── LICENSE
│   │           └── README.md
```

#### control File

```
Package: darkdork
Version: 1.0.0
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Your Name <your.email@example.com>
Description: Professional Google Dorking Tool
 DarkDork is a professional-grade Google dorking tool designed
 for forensic investigators and cybersecurity organizations.
 .
 Features include pre-built dork categories, custom dork builder,
 multi-format export, and search history tracking.
Depends: python3 (>= 3.7), python3-tk
Homepage: https://yourorganization.com
```

#### Build Script

```bash
#!/bin/bash
# build-deb.sh

VERSION="1.0.0"
PKG_NAME="darkdork_${VERSION}"
BUILD_DIR="${PKG_NAME}"

# Create directory structure
mkdir -p "${BUILD_DIR}/DEBIAN"
mkdir -p "${BUILD_DIR}/usr/bin"
mkdir -p "${BUILD_DIR}/usr/share/applications"
mkdir -p "${BUILD_DIR}/usr/share/icons/hicolor/256x256/apps"
mkdir -p "${BUILD_DIR}/usr/share/doc/darkdork"

# Copy executable
cp dist/DarkDork "${BUILD_DIR}/usr/bin/darkdork"
chmod 755 "${BUILD_DIR}/usr/bin/darkdork"

# Copy desktop file
cat > "${BUILD_DIR}/usr/share/applications/darkdork.desktop" << EOF
[Desktop Entry]
Name=DarkDork
Comment=Professional Google Dorking Tool
Exec=darkdork
Icon=darkdork
Terminal=false
Type=Application
Categories=Network;Security;
EOF

# Copy icon
cp icon.png "${BUILD_DIR}/usr/share/icons/hicolor/256x256/apps/darkdork.png"

# Copy documentation
cp LICENSE "${BUILD_DIR}/usr/share/doc/darkdork/"
cp README.md "${BUILD_DIR}/usr/share/doc/darkdork/"

# Create control file
cat > "${BUILD_DIR}/DEBIAN/control" << EOF
Package: darkdork
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Your Name <your.email@example.com>
Description: Professional Google Dorking Tool
 DarkDork is a professional-grade Google dorking tool designed
 for forensic investigators and cybersecurity organizations.
Depends: python3 (>= 3.7), python3-tk
Homepage: https://yourorganization.com
EOF

# Build package
dpkg-deb --build "${BUILD_DIR}"

echo "Package created: ${PKG_NAME}.deb"
```

### Creating .rpm Package (Fedora/RHEL)

#### Spec File

```spec
Name:           darkdork
Version:        1.0.0
Release:        1%{?dist}
Summary:        Professional Google Dorking Tool

License:        Apache-2.0
URL:            https://yourorganization.com
Source0:        %{name}-%{version}.tar.gz

Requires:       python3 >= 3.7
Requires:       python3-tkinter

%description
DarkDork is a professional-grade Google dorking tool designed
for forensic investigators and cybersecurity organizations.

%prep
%setup -q

%build
python3 -m PyInstaller --onefile --name DarkDork darkdork.py

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps

install -m 755 dist/DarkDork %{buildroot}%{_bindir}/darkdork
install -m 644 darkdork.desktop %{buildroot}%{_datadir}/applications/
install -m 644 icon.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/darkdork.png

%files
%license LICENSE
%doc README.md
%{_bindir}/darkdork
%{_datadir}/applications/darkdork.desktop
%{_datadir}/icons/hicolor/256x256/apps/darkdork.png

%changelog
* Thu Jan 09 2026 Your Name <your.email@example.com> - 1.0.0-1
- Initial release
```

### Creating AppImage

```bash
# Install appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# Create AppDir structure
mkdir -p DarkDork.AppDir/usr/bin
mkdir -p DarkDork.AppDir/usr/share/applications
mkdir -p DarkDork.AppDir/usr/share/icons/hicolor/256x256/apps

# Copy files
cp dist/DarkDork DarkDork.AppDir/usr/bin/darkdork
cp darkdork.desktop DarkDork.AppDir/
cp icon.png DarkDork.AppDir/darkdork.png
cp icon.png DarkDork.AppDir/usr/share/icons/hicolor/256x256/apps/

# Create AppRun script
cat > DarkDork.AppDir/AppRun << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin/:${PATH}"
exec "${HERE}/usr/bin/darkdork" "$@"
EOF
chmod +x DarkDork.AppDir/AppRun

# Build AppImage
./appimagetool-x86_64.AppImage DarkDork.AppDir
```

### Linux Build Checklist

- [ ] Build executable
- [ ] Test on Ubuntu 22.04
- [ ] Test on Debian 11
- [ ] Test on Fedora 38
- [ ] Create .deb package
- [ ] Create .rpm package
- [ ] Create AppImage (optional)
- [ ] Test all packages

---

## 6. Code Signing

### Why Code Signing?

**Benefits:**
- Users trust the software
- No security warnings
- Required for enterprise deployment
- Professional appearance

### Windows Code Signing

```batch
# Using SignTool (part of Windows SDK)
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist\DarkDork.exe

# Sign installer
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com installers\DarkDork-Setup.exe
```

**Certificate Sources:**
- DigiCert
- Sectigo
- GlobalSign
- GoDaddy

**Cost:** $200-500/year for code signing certificate

### macOS Code Signing

```bash
# Sign the application
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/DarkDork.app

# Verify signature
codesign --verify --deep --strict --verbose=2 dist/DarkDork.app

# Check signature
spctl -a -t exec -vv dist/DarkDork.app
```

#### Notarization (Required for macOS 10.15+)

```bash
# Create ZIP for notarization
ditto -c -k --keepParent dist/DarkDork.app DarkDork.zip

# Submit for notarization
xcrun notarytool submit DarkDork.zip \
  --apple-id "your@email.com" \
  --team-id "TEAMID" \
  --password "app-specific-password" \
  --wait

# Get notarization info
xcrun notarytool info SUBMISSION_ID \
  --apple-id "your@email.com" \
  --team-id "TEAMID" \
  --password "app-specific-password"

# Staple notarization
xcrun stapler staple dist/DarkDork.app
```

**Requirements:**
- Apple Developer Account ($99/year)
- Developer ID Application certificate
- App-specific password

### Linux Code Signing

```bash
# GPG signing
gpg --armor --detach-sign darkdork_1.0.0_amd64.deb

# Creates darkdork_1.0.0_amd64.deb.asc
# Users can verify with:
# gpg --verify darkdork_1.0.0_amd64.deb.asc darkdork_1.0.0_amd64.deb
```

---

## 7. Creating Installers

### Windows MSI Installer

Using WiX Toolset:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*" Name="DarkDork" Language="1033" Version="1.0.0"
           Manufacturer="Your Organization" UpgradeCode="YOUR-GUID-HERE">
    <Package InstallerVersion="200" Compressed="yes" InstallScope="perMachine" />

    <Media Id="1" Cabinet="darkdork.cab" EmbedCab="yes" />

    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="DarkDork" />
      </Directory>
    </Directory>

    <ComponentGroup Id="ProductComponents" Directory="INSTALLFOLDER">
      <Component Id="DarkDorkExe" Guid="YOUR-GUID-HERE">
        <File Id="DarkDorkExe" Source="dist\DarkDork.exe" KeyPath="yes" />
      </Component>
    </ComponentGroup>

    <Feature Id="ProductFeature" Title="DarkDork" Level="1">
      <ComponentGroupRef Id="ProductComponents" />
    </Feature>
  </Product>
</Wix>
```

### Portable Packages

**Windows ZIP:**
```batch
powershell Compress-Archive -Path DarkDork-Portable -DestinationPath DarkDork-1.0.0-Windows-x64.zip
```

**macOS TAR.GZ:**
```bash
tar -czf DarkDork-1.0.0-macOS.tar.gz dist/DarkDork.app LICENSE README.md docs/
```

**Linux TAR.GZ:**
```bash
tar -czf DarkDork-1.0.0-Linux-x64.tar.gz dist/DarkDork LICENSE README.md docs/
```

---

## 8. Distribution Checklist

### Pre-Distribution

- [ ] All features tested
- [ ] Documentation complete
- [ ] License files included
- [ ] Version numbers updated
- [ ] Changelog created
- [ ] Icons created for all platforms
- [ ] Code signed (for commercial)
- [ ] Malware scanned

### Per-Platform Checklist

**Windows:**
- [ ] 64-bit EXE built and tested
- [ ] 32-bit EXE built and tested (optional)
- [ ] Code signed
- [ ] Installer created (EXE or MSI)
- [ ] Installer tested on clean system
- [ ] Portable ZIP package created
- [ ] SHA256 checksums generated

**macOS:**
- [ ] APP bundle built
- [ ] Code signed with Developer ID
- [ ] Notarized with Apple
- [ ] DMG created
- [ ] DMG tested on clean system
- [ ] TAR.GZ package created
- [ ] SHA256 checksums generated

**Linux:**
- [ ] Binary built and tested
- [ ] .deb package created (Debian/Ubuntu)
- [ ] .rpm package created (Fedora/RHEL)
- [ ] AppImage created (optional)
- [ ] All packages tested
- [ ] TAR.GZ package created
- [ ] SHA256 checksums generated

### Distribution Package Contents

Each package should include:
- [ ] DarkDork executable/application
- [ ] LICENSE file
- [ ] README.md
- [ ] User manual (docs/USER_MANUAL.md)
- [ ] Quick start guide
- [ ] Changelog

### File Naming Convention

```
DarkDork-{version}-{platform}-{arch}.{ext}

Examples:
- DarkDork-1.0.0-Windows-x64.exe
- DarkDork-1.0.0-Windows-x64.zip
- DarkDork-1.0.0-macOS.dmg
- DarkDork-1.0.0-macOS.tar.gz
- DarkDork-1.0.0-Linux-x64.deb
- DarkDork-1.0.0-Linux-x64.rpm
- DarkDork-1.0.0-Linux-x64.AppImage
```

### Generate Checksums

```bash
# SHA256 checksums
sha256sum DarkDork-* > SHA256SUMS.txt

# On macOS
shasum -a 256 DarkDork-* > SHA256SUMS.txt

# On Windows (PowerShell)
Get-ChildItem DarkDork-* | Get-FileHash -Algorithm SHA256 > SHA256SUMS.txt
```

---

## 9. Troubleshooting

### PyInstaller Issues

**Hidden Imports:**
If modules aren't being detected:
```bash
pyinstaller --hidden-import=module_name darkdork.py
```

**Data Files Missing:**
```bash
pyinstaller --add-data "file.txt:." darkdork.py
```

**Large File Size:**
Use UPX compression:
```bash
pyinstaller --onefile --upx-dir=/path/to/upx darkdork.py
```

### Platform-Specific Issues

**Windows: "Not a valid Win32 application"**
- Verify correct architecture (32-bit vs 64-bit)
- Rebuild with correct Python version

**macOS: "Damaged and can't be opened"**
- Sign the application
- Notarize with Apple
- User can also: `xattr -cr DarkDork.app`

**Linux: "No such file or directory"**
- Check executable permissions: `chmod +x DarkDork`
- Verify dependencies are installed

### Build Environment Issues

**Clean Build:**
```bash
# Remove build artifacts
rm -rf build/ dist/ *.spec
# Rebuild
python build.py
```

**Virtual Environment:**
Build in clean virtual environment:
```bash
python -m venv build_env
source build_env/bin/activate  # or build_env\Scripts\activate on Windows
pip install pyinstaller
python build.py
```

---

## Additional Resources

### Official Documentation
- PyInstaller: https://pyinstaller.org/
- Inno Setup: https://jrsoftware.org/isinfo.php
- Apple Notarization: https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution

### Code Signing
- Windows: https://learn.microsoft.com/en-us/windows/win32/seccrypto/cryptography-tools
- macOS: https://developer.apple.com/support/code-signing/

### Packaging Tools
- create-dmg: https://github.com/create-dmg/create-dmg
- WiX Toolset: https://wixtoolset.org/
- Debian Packaging: https://www.debian.org/doc/manuals/maint-guide/

---

**Document Version:** 1.0
**Last Updated:** 2026-01-09

For questions about building and distribution, refer to the README.md or contact support.
