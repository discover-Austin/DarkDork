# DarkDork - Professional Google Dorking Tool

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

**DarkDork** is a professional-grade Google dorking tool designed specifically for forensic investigators, penetration testers, security researchers, and cybersecurity organizations. It provides an intuitive GUI interface for conducting advanced Google searches using specialized operators to uncover sensitive information, security vulnerabilities, and exposed assets.

## 🎯 Key Features

### Professional Capabilities
- **Pre-built Dork Categories**: 10+ carefully curated categories covering common security research scenarios
- **Custom Dork Builder**: Interactive interface with quick-insert operators
- **Batch Execution**: Run multiple dorks simultaneously with intelligent rate limiting
- **Search History**: Track all searches with timestamps and status
- **Multi-format Export**: Export results and history to CSV, JSON, HTML, and TXT
- **Target Domain Filtering**: Focus searches on specific domains
- **Configurable Settings**: Customize rate limits and search parameters

### Security-Focused Categories
1. **Exposed Documents** - Find sensitive PDFs, spreadsheets, and documents
2. **Login Pages** - Discover admin panels and authentication portals
3. **Vulnerable Servers** - Identify misconfigured servers and exposed files
4. **Network Devices** - Locate exposed cameras, routers, and IoT devices
5. **SQL Errors** - Find pages with database error messages
6. **Sensitive Directories** - Discover unprotected directory listings
7. **Exposed Credentials** - Search for leaked passwords and keys
8. **Vulnerable Web Apps** - Find potential web application vulnerabilities
9. **IoT Devices** - Locate smart home and IoT devices
10. **API Keys & Tokens** - Search for exposed API keys and tokens

## 📋 Requirements

- **Python 3.7 or higher**
- **tkinter** (included with standard Python installation)
- **Web browser** (for viewing search results)

### Supported Platforms
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+, Debian 10+, Fedora 30+)

## 🚀 Installation

### Option 1: Run from Source
```bash
# Clone the repository
git clone https://github.com/yourusername/darkdork.git
cd darkdork

# Run the application
python darkdork.py
```

### Option 2: Install as Package
```bash
# Clone and install
git clone https://github.com/yourusername/darkdork.git
cd darkdork
pip install -e .

# Run the application
darkdork
```

### Option 3: Build Standalone Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python build.py

# Executable will be in dist/DarkDork
```

## 📖 Usage Guide

### Quick Start

1. **Launch the Application**
   ```bash
   python darkdork.py
   ```

2. **Select a Category**
   - Navigate to the "Dork Categories" tab
   - Choose a category from the dropdown menu
   - Select a specific dork from the list

3. **Optional: Specify Target Domain**
   - Enter a domain name to focus your search (e.g., `example.com`)
   - This automatically adds `site:example.com` to your dork

4. **Execute the Search**
   - Click "Execute Dork" to run a single search
   - Click "Execute All in Category" to run all dorks in the category
   - Results open in your default web browser

### Custom Dork Building

1. Navigate to the "Custom Dork Builder" tab
2. Use the quick-insert buttons to add operators:
   - `site:` - Limit to specific domain
   - `filetype:` - Search for specific file types
   - `intitle:` - Search page titles
   - `inurl:` - Search URLs
   - `intext:` - Search page content
   - `ext:` - File extension

3. Build your query (example: `site:example.com filetype:pdf "confidential"`)
4. Click "Execute Custom Dork"
5. Save frequently used dorks for future use

### Google Dork Operators Reference

| Operator | Description | Example |
|----------|-------------|---------|
| `site:` | Limit results to specific domain | `site:example.com` |
| `filetype:` | Search for specific file types | `filetype:pdf` |
| `ext:` | Alternative to filetype | `ext:sql` |
| `intitle:` | Search in page titles | `intitle:"index of"` |
| `allintitle:` | All words must be in title | `allintitle:admin login` |
| `inurl:` | Search in URLs | `inurl:admin` |
| `allinurl:` | All words must be in URL | `allinurl:admin login` |
| `intext:` | Search in page content | `intext:password` |
| `allintext:` | All words must be in content | `allintext:username password` |
| `cache:` | View Google's cached version | `cache:example.com` |
| `link:` | Find pages linking to URL | `link:example.com` |
| `related:` | Find related websites | `related:example.com` |
| `info:` | Get information about page | `info:example.com` |

### Advanced Techniques

#### Combining Operators
```
site:example.com filetype:pdf "confidential"
inurl:admin intitle:login -site:example.com
filetype:sql "password" | "pwd" site:example.com
```

#### Wildcard Searches
```
intitle:"index of" "backup" *.sql
site:*.example.com filetype:xls
```

#### Excluding Terms
```
site:example.com -www -login
filetype:pdf -site:example.com "internal"
```

## 🔧 Configuration

Settings can be configured through the GUI (File → Settings) or by editing `darkdork_config.json`:

```json
{
  "rate_limit_seconds": 2,
  "results_per_page": 10,
  "auto_export": false,
  "default_export_format": "csv",
  "search_engine": "google"
}
```

### Configuration Options

- **rate_limit_seconds**: Delay between searches (default: 2)
- **results_per_page**: Number of results to display (default: 10)
- **auto_export**: Automatically export results (default: false)
- **default_export_format**: Default export format (csv, json, html)
- **search_engine**: Search engine to use (default: google)

## 📊 Export Formats

### CSV Export
Perfect for analysis in Excel or data processing tools:
```csv
timestamp,dork,status
2026-01-09 10:30:00,site:example.com filetype:pdf,Executed
```

### JSON Export
Ideal for programmatic processing:
```json
[
  {
    "timestamp": "2026-01-09 10:30:00",
    "dork": "site:example.com filetype:pdf",
    "status": "Executed"
  }
]
```

### HTML Export
Formatted reports for documentation:
- Professional styling
- Easy sharing with stakeholders
- Print-friendly format

## 🏢 Commercial Distribution

### Building for Distribution

1. **Create Standalone Executables**
   ```bash
   python build.py
   ```

2. **Code Signing** (Recommended for commercial use)
   - **Windows**: Use SignTool with a code signing certificate
   - **macOS**: Use Apple Developer ID certificate
   - **Linux**: Use GPG signing

3. **Create Installers**
   - **Windows**: Use Inno Setup (script included)
   - **macOS**: Create DMG file
   - **Linux**: Create .deb or .rpm packages

### Licensing for Commercial Distribution

This software is licensed under Apache 2.0, which allows:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Patent use
- ✅ Private use

Requirements:
- Include original LICENSE file
- State significant changes made
- Include copyright notice
- Include NOTICE file if provided

## ⚖️ Legal and Ethical Use

### ⚠️ IMPORTANT LEGAL NOTICE

**DarkDork is designed exclusively for authorized security testing and research.**

### Authorized Uses
✅ **Penetration Testing** - With written authorization
✅ **Bug Bounty Programs** - Within program scope
✅ **Security Research** - On your own systems
✅ **Forensic Investigations** - With proper legal authority
✅ **Red Team Exercises** - Within authorized scope
✅ **Security Audits** - With client permission
✅ **Educational Purposes** - In controlled environments

### Prohibited Uses
❌ **Unauthorized Access** - Accessing systems without permission
❌ **Data Theft** - Stealing or exfiltrating data
❌ **Malicious Intent** - Using for harmful purposes
❌ **Privacy Violations** - Invading personal privacy
❌ **Illegal Activities** - Any activities violating laws

### Best Practices

1. **Always obtain written authorization** before conducting security testing
2. **Respect scope limitations** defined in your authorization
3. **Follow responsible disclosure** practices for vulnerabilities found
4. **Comply with local laws** regarding computer security and privacy
5. **Document your testing** for accountability and legal protection
6. **Respect rate limits** to avoid overwhelming target systems
7. **Be ethical** - use your skills for defense, not offense

### Legal Frameworks to Consider

- **CFAA (USA)** - Computer Fraud and Abuse Act
- **GDPR (EU)** - General Data Protection Regulation
- **Computer Misuse Act (UK)**
- **Local cybersecurity laws** in your jurisdiction

## 🛡️ Security Best Practices

### For Security Professionals

1. **Scope Management**
   - Document authorization before testing
   - Stay within approved IP ranges/domains
   - Follow time windows for testing

2. **Data Handling**
   - Securely store exported results
   - Encrypt sensitive findings
   - Follow data retention policies
   - Use secure communication channels

3. **Reporting**
   - Document findings thoroughly
   - Use export features for evidence
   - Include timestamps in reports
   - Follow responsible disclosure

## 🤝 Support and Professional Services

### For Organizations

If you're interested in:
- **Custom development** for your organization
- **Training** for your security team
- **Support contracts**
- **Custom feature development**
- **Integration** with existing tools

Contact: [Your professional contact information]

## 📝 Changelog

### Version 1.0.0 (2026-01-09)
- Initial release
- 10 pre-built dork categories with 50+ dorks
- Custom dork builder with operator quick-insert
- Multi-format export (CSV, JSON, HTML, TXT)
- Search history tracking
- Batch search capabilities
- Configurable rate limiting
- Professional GUI interface
- Cross-platform support (Windows, macOS, Linux)

## 🔮 Roadmap

### Planned Features
- [ ] Integration with Shodan API
- [ ] Automated vulnerability scanning
- [ ] Report generation templates
- [ ] Team collaboration features
- [ ] Browser automation with Selenium
- [ ] Result parsing and analysis
- [ ] Integration with SIEM systems
- [ ] API for programmatic access
- [ ] Plugin system for extensions
- [ ] Dark mode UI theme

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Copyright 2026

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## ⚠️ Disclaimer

This tool is provided for educational and professional security testing purposes only. The developers and distributors of this software are not responsible for any misuse or damage caused by this tool. Users are solely responsible for ensuring they have proper authorization before conducting any security testing activities. Unauthorized access to computer systems is illegal and punishable by law.

By using this software, you agree to use it only for lawful purposes and in accordance with all applicable laws and regulations.

## 📧 Contact

For professional inquiries, custom development, or support:
- Website: [Your website]
- Email: [Your professional email]
- GitHub: [Your GitHub]

---

**Made with ❤️ for the cybersecurity community**

*Remember: With great power comes great responsibility. Use this tool ethically and legally.*
