# DarkDork User Manual v1.0

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [User Interface Overview](#user-interface-overview)
5. [Using Dork Categories](#using-dork-categories)
6. [Custom Dork Builder](#custom-dork-builder)
7. [Search History](#search-history)
8. [Export Features](#export-features)
9. [Configuration](#configuration)
10. [Advanced Usage](#advanced-usage)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)
13. [Legal Compliance](#legal-compliance)

---

## 1. Introduction

### What is DarkDork?

DarkDork is a professional Google dorking tool designed specifically for:
- **Security Researchers** conducting authorized assessments
- **Penetration Testers** performing reconnaissance
- **Forensic Investigators** gathering OSINT intelligence
- **Red Team Operators** simulating attacks
- **Security Auditors** identifying exposure risks

### What is Google Dorking?

Google dorking (also known as Google hacking) uses advanced Google search operators to find:
- Sensitive documents and files
- Login portals and admin interfaces
- Configuration files and credentials
- Vulnerable web applications
- Exposed network devices
- Database errors and system information

### Key Benefits

✅ **Time Savings** - Pre-built dork libraries save research time
✅ **Comprehensive Coverage** - 50+ curated dorks across 10 categories
✅ **Professional Documentation** - Track and export all findings
✅ **Team Collaboration** - Share custom dorks and results
✅ **Compliance Ready** - Built-in documentation for audit trails

---

## 2. Installation

### System Requirements

**Minimum Requirements:**
- Operating System: Windows 10/11, macOS 10.14+, or Linux
- Python: 3.7 or higher
- RAM: 2 GB
- Disk Space: 50 MB
- Internet Connection: Required

**Recommended:**
- Python 3.10+
- 4 GB RAM
- Modern web browser (Chrome, Firefox, Edge)

### Installation Methods

#### Method 1: Standalone Executable (Recommended for End Users)

1. Download the DarkDork executable for your platform
2. Extract to your preferred location
3. Run the executable:
   - **Windows**: Double-click `DarkDork.exe`
   - **macOS**: Open `DarkDork.app`
   - **Linux**: Execute `./DarkDork`

#### Method 2: Python Installation (Recommended for Developers)

```bash
# Clone or extract the repository
cd darkdork

# Install the package
pip install -e .

# Run the application
darkdork
```

#### Method 3: Direct Execution

```bash
# Navigate to the directory
cd darkdork

# Run directly
python darkdork.py
```

### First Launch

On first launch, DarkDork will:
1. Create configuration files in the application directory
2. Initialize the search history database
3. Display the main interface

---

## 3. Getting Started

### Quick Start Tutorial

**5-Minute Quick Start:**

1. **Launch DarkDork**
   - Open the application using your preferred method

2. **Select a Dork Category**
   - Go to the "Dork Categories" tab
   - Select "Exposed Documents" from the dropdown

3. **Choose a Target (Optional)**
   - Enter a domain in "Target Domain" field (e.g., `example.com`)
   - Leave blank to search globally

4. **Execute a Dork**
   - Select a dork from the list
   - Click "Execute Dork"
   - Results open in your default browser

5. **Review Results**
   - Check the "Search Results" area for execution logs
   - Visit the "Search History" tab to see all searches

### First Search Example

**Scenario:** Find PDF documents on a specific domain

1. Navigate to "Dork Categories" tab
2. Select "Exposed Documents" category
3. Enter target domain: `example.com`
4. Select dork: `filetype:pdf "confidential"`
5. Click "Execute Dork"
6. Review results in browser
7. Export findings from "Search History" tab

---

## 4. User Interface Overview

### Main Window Layout

```
┌─────────────────────────────────────────────────┐
│  DarkDork - Professional Google Dorking Tool    │
├─────────────────────────────────────────────────┤
│  File  Tools  Help                              │
├─────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────┐  │
│  │ [Dork Categories] [Custom Builder] [History]│
│  │                                             │
│  │  Category Selection and Dork List          │
│  │                                             │
│  │  Target Domain: [________________]         │
│  │                                             │
│  │  [Execute Dork] [Execute All in Category]  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  Search Results:                                 │
│  ┌────────────────────────────────────────────┐ │
│  │ [Execution logs and results appear here]  │ │
│  │                                            │ │
│  └────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────┤
│  Status: Ready                                   │
└──────────────────────────────────────────────────┘
```

### Menu Bar

**File Menu:**
- Export Results - Export current search results
- Export History - Export complete search history
- Settings - Configure application preferences
- Exit - Close the application

**Tools Menu:**
- Clear History - Remove all search history
- Batch Search - Execute multiple dorks from text input

**Help Menu:**
- Documentation - View built-in documentation
- About - Application information and license

### Status Bar

The status bar displays:
- Current operation status
- Last executed dork
- System messages

---

## 5. Using Dork Categories

### Available Categories

DarkDork includes 10 pre-built categories:

#### 1. Exposed Documents
**Purpose:** Find sensitive files exposed on web servers

**Common Use Cases:**
- Finding leaked confidential documents
- Discovering exposed financial records
- Locating unprotected intellectual property

**Example Dorks:**
- `filetype:pdf "confidential"`
- `filetype:xls "password"`
- `filetype:docx "internal use only"`

#### 2. Login Pages
**Purpose:** Identify authentication portals and admin interfaces

**Common Use Cases:**
- Mapping attack surface
- Identifying admin panels
- Discovering authentication mechanisms

**Example Dorks:**
- `inurl:admin intitle:login`
- `inurl:wp-admin`
- `intitle:"phpMyAdmin"`

#### 3. Vulnerable Servers
**Purpose:** Find misconfigured servers with exposed files

**Common Use Cases:**
- Identifying directory listing vulnerabilities
- Finding backup files
- Discovering configuration files

**Example Dorks:**
- `intitle:"Index of" .bash_history`
- `intitle:"Index of" "database.sql"`
- `intitle:"Index of" ".env"`

#### 4. Network Devices
**Purpose:** Locate exposed network equipment and IoT devices

**Common Use Cases:**
- Discovering unsecured cameras
- Finding exposed routers
- Identifying network infrastructure

**Example Dorks:**
- `intitle:"Network Camera" inurl:ViewerFrame`
- `inurl:8080 intitle:"Surveillance"`
- `intitle:"netcam live image"`

#### 5. SQL Errors
**Purpose:** Find web applications exposing database errors

**Common Use Cases:**
- Identifying SQL injection vulnerabilities
- Discovering database technologies in use
- Finding development/test environments

**Example Dorks:**
- `intext:"SQL syntax" site:`
- `intext:"mysql_fetch" site:`
- `intext:"Warning: mysql" site:`

#### 6. Sensitive Directories
**Purpose:** Find exposed directory listings

**Common Use Cases:**
- Discovering backup directories
- Finding log files
- Locating admin areas

**Example Dorks:**
- `intitle:"Index of" "/private"`
- `intitle:"Index of" "/logs"`
- `intitle:"Index of" "/admin"`

#### 7. Exposed Credentials
**Purpose:** Search for leaked credentials and keys

**Common Use Cases:**
- Finding password files
- Discovering API credentials
- Locating SSH keys

**Example Dorks:**
- `filetype:log username password`
- `filetype:sql "password" | "pwd"`
- `"BEGIN RSA PRIVATE KEY" site:`

#### 8. Vulnerable Web Apps
**Purpose:** Identify potentially compromised web applications

**Common Use Cases:**
- Finding web shells
- Discovering backdoors
- Locating security.txt files

**Example Dorks:**
- `inurl:shell.php`
- `inurl:webshell`
- `inurl:security.txt`

#### 9. IoT Devices
**Purpose:** Locate smart home and IoT devices

**Common Use Cases:**
- Identifying unsecured smart devices
- Finding exposed control panels
- Discovering IoT vulnerabilities

**Example Dorks:**
- `intitle:"smart home" inurl:web`
- `intitle:"Dashboard" "smart meter"`
- `intitle:"Device Management" inurl:8080`

#### 10. API Keys & Tokens
**Purpose:** Search for exposed API credentials

**Common Use Cases:**
- Finding leaked API keys
- Discovering access tokens
- Locating configuration files with secrets

**Example Dorks:**
- `filetype:env "API_KEY"`
- `filetype:json "api_key"`
- `"x-api-key" site:`

### Executing Dorks from Categories

**Single Dork Execution:**

1. Select category from dropdown
2. Click on desired dork in the list
3. Optional: Enter target domain
4. Click "Execute Dork"
5. View results in browser

**Batch Category Execution:**

1. Select category from dropdown
2. Optional: Enter target domain
3. Click "Execute All in Category"
4. Confirm the batch operation
5. Wait for rate-limited execution
6. Review results in history

### Target Domain Filtering

**Purpose:** Focus searches on specific domains

**Usage:**
- Enter domain without protocol: `example.com`
- Automatically adds `site:example.com` to dorks
- Leave blank for global searches

**Examples:**
- `example.com` - Search only example.com
- `*.example.com` - Search all subdomains (if dork supports wildcards)
- Leave empty - Search entire internet

---

## 6. Custom Dork Builder

### Building Custom Dorks

The Custom Dork Builder allows you to create specialized search queries.

### Google Dork Operators Reference

#### Basic Operators

**site:**
- **Purpose:** Restrict results to specific domain
- **Syntax:** `site:example.com`
- **Example:** `site:example.com filetype:pdf`

**filetype: / ext:**
- **Purpose:** Search for specific file types
- **Syntax:** `filetype:pdf` or `ext:pdf`
- **Supported:** pdf, doc, docx, xls, xlsx, ppt, txt, sql, xml, json, etc.
- **Example:** `filetype:xls "financial report"`

**intitle:**
- **Purpose:** Search for words in page title
- **Syntax:** `intitle:"text"`
- **Example:** `intitle:"index of" "backup"`

**allintitle:**
- **Purpose:** All words must be in title
- **Syntax:** `allintitle:word1 word2`
- **Example:** `allintitle:admin login panel`

**inurl:**
- **Purpose:** Search for words in URL
- **Syntax:** `inurl:admin`
- **Example:** `inurl:login.php`

**allinurl:**
- **Purpose:** All words must be in URL
- **Syntax:** `allinurl:admin login`
- **Example:** `allinurl:admin config php`

**intext:**
- **Purpose:** Search for words in page content
- **Syntax:** `intext:"password"`
- **Example:** `intext:"connection string" site:example.com`

**allintext:**
- **Purpose:** All words must be in content
- **Syntax:** `allintext:username password email`
- **Example:** `allintext:confidential internal only`

**cache:**
- **Purpose:** View Google's cached version of page
- **Syntax:** `cache:example.com`
- **Example:** `cache:example.com/deleted-page`

**link:**
- **Purpose:** Find pages linking to a URL
- **Syntax:** `link:example.com`
- **Example:** `link:example.com/important-page`

**related:**
- **Purpose:** Find related/similar websites
- **Syntax:** `related:example.com`
- **Example:** `related:github.com`

**info:**
- **Purpose:** Get information about a page
- **Syntax:** `info:example.com`
- **Example:** `info:example.com/about`

#### Advanced Operators

**OR (|)**
- **Purpose:** Search for either term
- **Syntax:** `term1 OR term2` or `term1 | term2`
- **Example:** `"password" OR "pwd" filetype:sql`

**Exclusion (-)**
- **Purpose:** Exclude terms from results
- **Syntax:** `-term`
- **Example:** `site:example.com -www`

**Wildcard (*)**
- **Purpose:** Match any word
- **Syntax:** `* word`
- **Example:** `"admin * login"`

**Quotes ("")**
- **Purpose:** Exact phrase match
- **Syntax:** `"exact phrase"`
- **Example:** `"internal use only"`

**Number Range (..)**
- **Purpose:** Search within number range
- **Syntax:** `number1..number2`
- **Example:** `camera $100..$500`

### Using Quick-Insert Buttons

The Custom Dork Builder includes quick-insert buttons:

1. Click any operator button (e.g., "site:")
2. Operator is inserted at cursor position
3. Type your value after the operator
4. Add spaces between operators
5. Click "Execute Custom Dork"

### Custom Dork Examples

**Example 1: Find PDF Reports on Domain**
```
site:example.com filetype:pdf "annual report" 2024
```

**Example 2: Find Admin Panels Excluding Main Site**
```
inurl:admin -site:www.example.com site:*.example.com
```

**Example 3: Find Exposed Databases**
```
intitle:"index of" "database.sql" OR "db_backup.sql"
```

**Example 4: Find API Documentation**
```
site:example.com inurl:api intitle:"documentation" OR intitle:"api docs"
```

**Example 5: Find Configuration Files**
```
site:example.com (filetype:env OR filetype:config) "password"
```

### Saving Custom Dorks

1. Build your custom dork
2. Click "Save Current" button
3. Dork is saved to "Saved Custom Dorks" list
4. Load anytime with "Load Selected"
5. Delete with "Delete Selected"

**Saved Dorks Storage:**
- Stored in `saved_dorks.json`
- Persists between sessions
- Can be shared with team members

---

## 7. Search History

### Understanding Search History

Search history tracks:
- **Timestamp** - When the search was executed
- **Dork Query** - The exact dork used
- **Status** - Execution status (Executed, Error, etc.)

### Using Search History

**Viewing History:**
1. Navigate to "Search History" tab
2. View all searches in chronological order
3. Sort by clicking column headers

**Repeating Searches:**
1. Select a search from history
2. Click "Repeat Search"
3. Dork is executed again with current settings

**Clearing History:**
1. Click "Clear History" button
2. Confirm deletion
3. All history is permanently removed

### Exporting History

**Export to CSV:**
1. Click File → Export History
2. Choose CSV format
3. Select save location
4. Open in Excel or Google Sheets

**Export to JSON:**
1. Click File → Export History
2. Choose JSON format
3. Select save location
4. Use for programmatic analysis

**History Export Format:**

CSV:
```csv
timestamp,dork,status
2026-01-09 10:30:00,site:example.com filetype:pdf,Executed
```

JSON:
```json
[
  {
    "timestamp": "2026-01-09 10:30:00",
    "dork": "site:example.com filetype:pdf",
    "status": "Executed"
  }
]
```

---

## 8. Export Features

### Exporting Search Results

**Text Export:**
1. Click File → Export Results
2. Choose "Text files (*.txt)"
3. Select save location
4. Results saved with timestamps and URLs

**HTML Export:**
1. Click File → Export Results
2. Choose "HTML files (*.html)"
3. Select save location
4. Professional formatted report generated

**HTML Export Includes:**
- Styled headers and formatting
- Timestamps for each search
- Complete search URLs
- Print-friendly layout

### Report Generation Best Practices

**For Client Reports:**
1. Execute all relevant dorks
2. Export as HTML for professional appearance
3. Include screenshots from browser results
4. Add executive summary

**For Internal Documentation:**
1. Export history as CSV
2. Import into tracking system
3. Tag with project/client name
4. Archive with engagement documentation

**For Compliance/Audit:**
1. Export both results and history
2. Include timestamps
3. Store with authorization documentation
4. Maintain chain of custody

---

## 9. Configuration

### Accessing Settings

Click **File → Settings** to open configuration dialog.

### Configuration Options

#### Rate Limit (seconds)
- **Purpose:** Delay between consecutive searches
- **Range:** 1-10 seconds
- **Default:** 2 seconds
- **Recommendation:** Keep at 2+ to respect Google's terms
- **Commercial Use:** Consider 3-5 seconds

#### Results Per Page
- **Purpose:** Number of results to display
- **Range:** 5-100
- **Default:** 10
- **Note:** Affects export file size

### Configuration File

Settings are stored in `darkdork_config.json`:

```json
{
  "rate_limit_seconds": 2,
  "results_per_page": 10,
  "auto_export": false,
  "default_export_format": "csv",
  "search_engine": "google"
}
```

### Manual Configuration

Advanced users can edit `darkdork_config.json` directly:

1. Close DarkDork application
2. Open `darkdork_config.json` in text editor
3. Modify values
4. Save file
5. Restart application

---

## 10. Advanced Usage

### Batch Search Operations

**Purpose:** Execute multiple custom dorks sequentially

**Usage:**
1. Click Tools → Batch Search
2. Enter dorks (one per line) in text area
3. Click "Execute All"
4. Searches execute with rate limiting

**Example Batch Input:**
```
site:example.com filetype:pdf
site:example.com filetype:doc
site:example.com intitle:login
site:example.com inurl:admin
```

### Team Collaboration

**Sharing Custom Dorks:**
1. Locate `saved_dorks.json` file
2. Copy to shared location
3. Team members replace their local file
4. Restart DarkDork

**Sharing Results:**
1. Export results as HTML or CSV
2. Share via secure channel
3. Include context and authorization documentation

### Integration with Other Tools

**With Burp Suite:**
1. Use DarkDork to discover endpoints
2. Import discovered URLs into Burp Suite
3. Perform detailed testing

**With Nmap:**
1. Use Network Devices category
2. Extract IP addresses from results
3. Perform network scanning with Nmap

**With Metasploit:**
1. Identify vulnerable applications
2. Search for relevant exploits
3. Test with authorization

### Automation Tips

**Scheduled Searches:**
- Create batch files with common dorks
- Schedule with cron (Linux) or Task Scheduler (Windows)
- Automatically export results

**Command-Line Usage:**
While DarkDork is GUI-focused, you can:
1. Prepare custom dorks in files
2. Use batch search feature
3. Automate exports

---

## 11. Best Practices

### Before Starting

✅ **Obtain Authorization**
- Get written permission from client/organization
- Define scope of testing
- Document authorization

✅ **Understand Scope**
- Know which domains are in scope
- Understand what you're looking for
- Plan your dork categories

✅ **Prepare Documentation**
- Create engagement folder
- Prepare report templates
- Set up evidence collection

### During Usage

✅ **Start Broad, Then Focus**
- Begin with general category dorks
- Refine based on initial findings
- Create custom dorks for specific targets

✅ **Document Everything**
- Export results regularly
- Save interesting findings
- Take screenshots

✅ **Respect Rate Limits**
- Don't reduce rate limit below 2 seconds
- Consider target server load
- Be a responsible tester

✅ **Verify Findings**
- Manually verify important findings
- Don't rely solely on Google results
- Confirm vulnerabilities exist

### After Completion

✅ **Generate Reports**
- Export final results
- Create professional documentation
- Include recommendations

✅ **Secure Data**
- Encrypt sensitive findings
- Store securely
- Follow data retention policies

✅ **Responsible Disclosure**
- Report vulnerabilities appropriately
- Follow disclosure timelines
- Protect sensitive information

### Legal and Ethical Guidelines

1. **Always Have Authorization**
   - Written permission required
   - Clearly defined scope
   - Documented authorization period

2. **Respect Privacy**
   - Don't access personal information
   - Follow privacy laws
   - Protect discovered data

3. **Professional Conduct**
   - Act ethically
   - Follow industry standards
   - Maintain confidentiality

4. **Compliance**
   - Follow local laws
   - Adhere to GDPR, CCPA, etc.
   - Respect Terms of Service

---

## 12. Troubleshooting

### Common Issues

#### Application Won't Start

**Symptoms:** Double-clicking does nothing or shows error

**Solutions:**
1. Verify Python 3.7+ is installed: `python --version`
2. Check tkinter is available: `python -c "import tkinter"`
3. Run from command line to see errors: `python darkdork.py`
4. Check file permissions

#### Browser Doesn't Open

**Symptoms:** Clicking Execute Dork doesn't open browser

**Solutions:**
1. Set default web browser in OS settings
2. Check browser installation
3. Try different browser
4. Check firewall/security software

#### Searches Not Working

**Symptoms:** Browser opens but shows errors or no results

**Solutions:**
1. Verify internet connection
2. Check Google is accessible
3. Try reducing rate limit
4. Clear browser cookies
5. Try different search terms

#### Export Fails

**Symptoms:** Export operation shows error

**Solutions:**
1. Check disk space available
2. Verify write permissions
3. Choose different save location
4. Close file if already open
5. Try different export format

#### Settings Not Saving

**Symptoms:** Configuration changes don't persist

**Solutions:**
1. Check file write permissions
2. Verify `darkdork_config.json` exists
3. Run application with proper permissions
4. Check for disk errors

### Error Messages

**"Failed to execute dork"**
- Check internet connection
- Verify dork syntax
- Try simpler dork first

**"Failed to export"**
- Check destination folder permissions
- Ensure sufficient disk space
- Try different location

**"Failed to save configuration"**
- Check application directory permissions
- Verify disk is not full
- Try running as administrator (if appropriate)

### Getting Help

If issues persist:

1. Check documentation thoroughly
2. Review README.md
3. Contact support (if applicable)
4. Check GitHub issues (if open source)

---

## 13. Legal Compliance

### Authorization Requirements

**Required Before Use:**
1. **Written Authorization**
   - Signed agreement from target organization
   - Clearly defined scope
   - Specified time period

2. **Scope Documentation**
   - List of authorized domains
   - Approved testing methods
   - Restricted areas

3. **Rules of Engagement**
   - Working hours
   - Emergency contacts
   - Escalation procedures

### Compliance Frameworks

**PCI DSS:**
- Document all testing
- Follow requirement 11.3
- Maintain audit trails

**ISO 27001:**
- Follow security testing procedures
- Document methodology
- Maintain evidence

**NIST:**
- Follow SP 800-115 guidelines
- Document procedures
- Maintain chain of custody

### Data Protection

**GDPR Compliance:**
- Minimize personal data collection
- Document processing activities
- Ensure data security

**CCPA Compliance:**
- Handle California data appropriately
- Follow disclosure requirements
- Respect privacy rights

### Incident Response

**If Unauthorized Access Occurs:**
1. Stop immediately
2. Document what happened
3. Notify appropriate parties
4. Follow legal counsel guidance

**If Sensitive Data Found:**
1. Don't download or store
2. Document discovery
3. Notify appropriate parties
4. Follow disclosure procedures

---

## Appendix A: Keyboard Shortcuts

(Currently none - GUI-based operation)

## Appendix B: File Locations

- **Configuration:** `darkdork_config.json`
- **Saved Dorks:** `saved_dorks.json`
- **Exports:** User-selected location

## Appendix C: Supported File Types

Common file types for dorking:
- Documents: pdf, doc, docx, txt, rtf
- Spreadsheets: xls, xlsx, csv
- Presentations: ppt, pptx
- Data: sql, xml, json, yml
- Configuration: env, config, ini, properties
- Code: php, asp, jsp, py, java
- Archives: zip, rar, tar, gz
- Logs: log

## Appendix D: Additional Resources

**Learning Resources:**
- Google Advanced Search Operators Guide
- OWASP Testing Guide
- SANS Penetration Testing Resources

**Tools to Combine With:**
- Burp Suite
- OWASP ZAP
- Nmap
- Metasploit
- Shodan

---

**Document Version:** 1.0
**Last Updated:** 2026-01-09
**Application Version:** 1.0.0

For questions or support, refer to the main README.md file.
