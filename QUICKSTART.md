# DarkDork Quick Start Guide

Get started with DarkDork in 5 minutes!

## 1. Installation

### Option A: Windows Executable
1. Download `DarkDork-1.0.0-Windows-x64.exe`
2. Double-click to run
3. Click "Execute Dork" on any pre-loaded dork

### Option B: macOS Application
1. Download `DarkDork-1.0.0-macOS.dmg`
2. Open the DMG file
3. Drag DarkDork to Applications folder
4. Launch from Applications

### Option C: Linux
1. Download package for your distribution
2. Install:
   ```bash
   # Debian/Ubuntu
   sudo dpkg -i DarkDork-1.0.0-Linux-x64.deb

   # Fedora/RHEL
   sudo rpm -i DarkDork-1.0.0-Linux-x64.rpm
   ```
3. Run: `darkdork`

### Option D: Python
```bash
python darkdork.py
```

## 2. Your First Search (30 seconds)

1. **Launch DarkDork**

2. **Go to "Dork Categories" tab** (should be default)

3. **Select a category**
   - Click the dropdown menu
   - Choose "Exposed Documents"

4. **Pick a dork**
   - Click on any dork in the list
   - Try: `filetype:pdf "confidential"`

5. **Click "Execute Dork"**
   - Your browser will open with results

That's it! You just performed your first Google dork search.

## 3. Targeting a Specific Domain (1 minute)

Want to search only one website?

1. **Enter target domain**
   - In "Target Domain" field, type: `example.com`
   - Don't include `http://` or `www.`

2. **Select any dork**

3. **Click "Execute Dork"**
   - Searches only that domain

## 4. Building Custom Dorks (2 minutes)

### Simple Example: Find PDFs About Security

1. **Go to "Custom Dork Builder" tab**

2. **Build your dork**
   - Click "filetype:" button
   - Type: `pdf`
   - Press space
   - Type: `"security report" 2024`

3. **Result:** `filetype:pdf "security report" 2024`

4. **Click "Execute Custom Dork"**

### Advanced Example: Find Login Pages

1. **Custom Dork Builder tab**

2. **Build:**
   - Click "inurl:" → type `admin`
   - Click "intitle:" → type `login`
   - Result: `inurl:admin intitle:login`

3. **Click "Execute Custom Dork"**

## 5. Common Use Cases

### Find Exposed Documents
```
Category: Exposed Documents
Dork: filetype:pdf "confidential"
Target: yourcompany.com
```

### Discover Admin Panels
```
Category: Login Pages
Dork: inurl:admin intitle:login
Target: (leave blank for all sites)
```

### Find Configuration Files
```
Category: Vulnerable Servers
Dork: intitle:"Index of" "config"
Target: yourcompany.com
```

### Locate Database Errors
```
Category: SQL Errors
Dork: intext:"SQL syntax" site:
Target: yourcompany.com
```

## 6. Export Your Results (1 minute)

### Export Search History

1. **Go to "Search History" tab**
   - See all your searches

2. **Click "File" → "Export History"**

3. **Choose format**
   - CSV for Excel
   - JSON for programming

4. **Save the file**

### Export Current Results

1. **Click "File" → "Export Results"**

2. **Choose format**
   - TXT for simple text
   - HTML for formatted report

## 7. Pro Tips

### Batch Searching
Execute multiple dorks at once:
1. **Click "Tools" → "Batch Search"**
2. **Enter dorks** (one per line)
3. **Click "Execute All"**

### Save Custom Dorks
1. Build a dork in Custom Dork Builder
2. Click "Save Current"
3. Load anytime with "Load Selected"

### Adjust Rate Limiting
Slow down searches to be respectful:
1. **Click "File" → "Settings"**
2. **Increase "Rate Limit"** to 3-5 seconds
3. **Click "Save"**

## 8. Google Dork Operators Cheat Sheet

| Operator | What It Does | Example |
|----------|--------------|---------|
| `site:` | Search specific domain | `site:example.com` |
| `filetype:` | Find specific files | `filetype:pdf` |
| `intitle:` | Search page titles | `intitle:login` |
| `inurl:` | Search URLs | `inurl:admin` |
| `intext:` | Search page content | `intext:password` |
| `"quotes"` | Exact phrase | `"confidential document"` |
| `-minus` | Exclude term | `-www` |
| `OR` or `\|` | Either term | `pdf OR doc` |

## 9. Best Practices

### Always Remember

✅ **Get Authorization** - Only search domains you're authorized to test

✅ **Document Everything** - Export your searches for reports

✅ **Be Respectful** - Don't hammer Google with rapid searches

✅ **Verify Findings** - Check results manually

❌ **Never:**
- Search without authorization
- Download sensitive files you find
- Reduce rate limit below 2 seconds
- Use for malicious purposes

## 10. Example Workflows

### Security Assessment Workflow

**Step 1: Reconnaissance**
```
1. Exposed Documents category
2. Target: client-domain.com
3. Execute all in category
4. Note interesting findings
```

**Step 2: Authentication Testing**
```
1. Login Pages category
2. Target: client-domain.com
3. Execute all in category
4. Map login portals
```

**Step 3: Configuration Review**
```
1. Vulnerable Servers category
2. Target: client-domain.com
3. Look for exposed configs
4. Document findings
```

**Step 4: Export Report**
```
1. Export history as CSV
2. Export results as HTML
3. Include in report
```

### Bug Bounty Workflow

**Step 1: Scope Check**
```
- Review program scope
- Note authorized domains
```

**Step 2: Information Gathering**
```
1. Use multiple categories
2. Target each in-scope domain
3. Take notes in external tool
```

**Step 3: Validation**
```
- Manually verify each finding
- Check if issue is known
- Document reproduction steps
```

**Step 4: Reporting**
```
- Export evidence
- Screenshot findings
- Submit to program
```

## 11. Common Issues

### Browser Doesn't Open
**Solution:** Set your default browser in OS settings

### No Results Found
**Solution:** Try simpler dorks first, Google may have nothing matching

### Too Many Results
**Solution:** Add more specific terms or use `site:` operator

### Application Won't Start
**Solution:**
- Windows: Right-click → Run as Administrator
- macOS: System Preferences → Security → Allow
- Linux: `chmod +x darkdork`

## 12. Getting Help

### Documentation
- Full manual: `docs/USER_MANUAL.md`
- Build guide: `docs/BUILD_GUIDE.md`
- README: `README.md`

### In Application
- Click "Help" → "Documentation"
- Click "Help" → "About"

### Support
- Check documentation first
- Review GitHub issues (if open source)
- Contact: [Your support email]

## 13. Legal Reminder

⚠️ **IMPORTANT LEGAL NOTICE**

DarkDork is for **authorized security testing only**.

**You MUST have:**
- Written authorization
- Defined scope
- Clear permission

**Unauthorized access is ILLEGAL and may result in:**
- Criminal charges
- Civil liability
- Professional consequences

**Use responsibly and ethically!**

---

## Quick Reference Card

Print this for your desk:

```
┌─────────────────────────────────────────────┐
│         DARKDORK QUICK REFERENCE            │
├─────────────────────────────────────────────┤
│ BASIC OPERATORS                             │
│  site:example.com    Search specific site  │
│  filetype:pdf        Find PDFs              │
│  intitle:"text"      Text in title          │
│  inurl:admin         Text in URL            │
│  intext:password     Text in content        │
│                                             │
│ COMBINATIONS                                │
│  site:example.com filetype:pdf              │
│  inurl:admin intitle:login                  │
│  intext:error site:example.com              │
│                                             │
│ EXCLUSION                                   │
│  site:example.com -www                      │
│  filetype:pdf -site:example.com             │
│                                             │
│ REMEMBER                                    │
│  ✓ Get authorization first                 │
│  ✓ Use rate limiting (2+ seconds)          │
│  ✓ Export your findings                    │
│  ✓ Document everything                     │
│  ✗ Never: unauthorized access              │
└─────────────────────────────────────────────┘
```

---

**Ready to get started?**

Launch DarkDork and try your first search now!

For detailed information, see the full User Manual in `docs/USER_MANUAL.md`.

---

**Version:** 1.0.0
**Last Updated:** 2026-01-09
