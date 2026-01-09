# DarkDork - Complete Usage Guide

## Quick Start (5 Minutes)

### 1. Running the Application

#### Option A: Run from Source (Development)
```bash
# Navigate to the directory
cd /home/user/DarkDork

# Run the main application
python darkdork.py
```

#### Option B: Run with CLI
```bash
# Execute a single dork
python darkdork_cli.py -d "filetype:pdf confidential" -t example.com

# Execute from file
python darkdork_cli.py -f dorks.txt -t example.com

# List all categories
python darkdork_cli.py --list-categories

# Search the library
python darkdork_cli.py --search "password" --severity Critical
```

### 2. First Search (GUI)

1. **Launch the application:**
   ```bash
   python darkdork.py
   ```

2. **The GUI will open with three tabs:**
   - Dork Categories (pre-built dorks)
   - Custom Dork Builder (create your own)
   - Search History (view past searches)

3. **Execute your first search:**
   - Go to "Dork Categories" tab
   - Select "Exposed Documents" from dropdown
   - Click on any dork in the list
   - (Optional) Enter target domain: `example.com`
   - Click "Execute Dork"
   - Your browser opens with results!

4. **View results:**
   - Check the "Search Results" area for logs
   - Go to "Search History" tab to see all searches

### 3. Export Your Results

```bash
# From GUI: File → Export Results
# Choose format: CSV, JSON, HTML, or TXT

# From CLI:
python darkdork_cli.py -d "filetype:sql" -t example.com -e results.json
```

---

## Advanced Usage

### Using the Dork Library System

```bash
# Create comprehensive dork library
python darkdork_library.py

# This creates dork_library.json with 70+ dorks
```

**In Python code:**
```python
from darkdork_library import DorkLibrary

# Load library
lib = DorkLibrary()

# Search for dorks
results = lib.search_dorks(
    query="password",
    severity="Critical",
    tags=["credentials"]
)

# Get statistics
stats = lib.get_statistics()
print(f"Total dorks: {stats['total_dorks']}")
print(f"Categories: {stats['categories']}")
```

### Using the Database System

```python
from darkdork_db import DarkDorkDatabase

# Create database
db = DarkDorkDatabase('my_assessment.db')

# Create a project
project_id = db.create_project(
    "Client Security Assessment",
    "External security review",
    "client.com"
)

# Record a search
search_id = db.record_search(
    "filetype:pdf confidential",
    project_id=project_id,
    target_domain="client.com"
)

# Add results
result_id = db.add_result(
    search_id,
    "https://client.com/confidential.pdf",
    title="Exposed Document",
    severity="High"
)

# Create finding
finding_id = db.create_finding(
    result_id,
    "Exposed Confidential Document",
    "Document is publicly accessible",
    "High",
    cvss_score=7.5
)

# Get statistics
stats = db.get_statistics()
print(stats)
```

### Setting Up Automation

```python
from darkdork_automation import AutomationManager, ScheduledTask

# Create automation manager
manager = AutomationManager()

# Setup daily monitoring
dorks = [
    "filetype:pdf confidential",
    "inurl:admin intitle:login",
    "intitle:\"index of\" .env"
]

manager.setup_daily_monitoring("example.com", dorks)

# Or create a custom workflow
workflow_id = manager.create_security_assessment_workflow("example.com")

# Execute workflow
manager.workflow_engine.execute_workflow(workflow_id)

# Start scheduler
manager.scheduler.run()
```

### Using Integrations

```python
from darkdork_integrations import IntegrationManager

# Setup integrations
manager = IntegrationManager()

# Configure Shodan
manager.setup_shodan("YOUR_SHODAN_API_KEY")

# Configure Slack notifications
manager.setup_slack("https://hooks.slack.com/services/YOUR/WEBHOOK/URL")

# Search Shodan
shodan = manager.get_integration('shodan')
results = shodan.search('apache')

# Send notification about finding
manager.notify_finding(
    "Critical Finding",
    "Found exposed database at example.com/db.sql",
    "critical"
)
```

### Advanced Export Options

```python
from darkdork_exports import ExportManager

exporter = ExportManager()

# Sample data
data = [
    {
        'timestamp': '2026-01-09 10:30:00',
        'dork': 'filetype:pdf confidential',
        'target': 'example.com',
        'severity': 'high'
    }
]

# Export to PDF (requires reportlab)
exporter.export_to_pdf(
    data,
    'report.pdf',
    title='Security Assessment Report',
    include_summary=True
)

# Export to DOCX (requires python-docx)
exporter.export_to_docx(
    data,
    'report.docx',
    title='Client Security Report'
)

# Export to XML
exporter.export_to_xml(data, 'results.xml')

# Export to HTML
exporter.export_to_html(
    data,
    'dashboard.html',
    title='Security Dashboard',
    include_css=True
)
```

---

## Command-Line Interface Examples

### Basic Searches

```bash
# Single dork with target
python darkdork_cli.py -d "filetype:pdf confidential" -t example.com

# Single dork, open in browser
python darkdork_cli.py -d "inurl:admin" -t example.com -b

# With custom delay
python darkdork_cli.py -d "filetype:sql" -t example.com --delay 5
```

### Batch Operations

```bash
# Create a dorks file
cat > my_dorks.txt << EOF
filetype:pdf confidential
inurl:admin intitle:login
intitle:"index of" .env
filetype:sql "CREATE TABLE"
EOF

# Execute all dorks
python darkdork_cli.py -f my_dorks.txt -t example.com

# Execute and export
python darkdork_cli.py -f my_dorks.txt -t example.com -e results.json
```

### Category-Based Searches

```bash
# List available categories
python darkdork_cli.py --list-categories

# Execute entire category
python darkdork_cli.py -c "Exposed Documents" -t example.com

# Execute and export
python darkdork_cli.py -c "Login Pages" -t example.com -e logins.csv --format csv
```

### Library Operations

```bash
# Search library
python darkdork_cli.py --search "password"

# Filter by severity
python darkdork_cli.py --search "config" --severity High

# Filter by tags
python darkdork_cli.py --tags credentials database

# Show statistics
python darkdork_cli.py --stats
```

---

## Configuration

### Main Configuration File: `darkdork_config.json`

```json
{
  "rate_limit_seconds": 2,
  "results_per_page": 10,
  "auto_export": false,
  "default_export_format": "csv",
  "search_engine": "google"
}
```

### Using Configuration Presets

```bash
# View available presets
cat config_presets.json

# Copy a preset to your config
python -c "
import json
with open('config_presets.json') as f:
    presets = json.load(f)
with open('darkdork_config.json', 'w') as f:
    json.dump(presets['presets']['forensics'], f, indent=2)
"
```

**Available Presets:**
- `conservative` - 5s rate limit, respectful
- `standard` - 2s rate limit, recommended
- `rapid` - 1s rate limit, for bug bounties
- `forensics` - 3s rate limit, HTML exports
- `pentesting` - 2s rate limit, CSV exports
- `compliance` - 4s rate limit, comprehensive logging

---

## Integration Setup

### Setting Up Shodan Integration

```python
from darkdork_integrations import IntegrationConfig

# Save API key
config = IntegrationConfig()
config.set_api_key('shodan', 'YOUR_SHODAN_API_KEY')

# Now use in your code
from darkdork_integrations import ShodanIntegration
shodan = ShodanIntegration(config.get_api_key('shodan'))
results = shodan.search('apache')
```

### Setting Up Slack Notifications

```python
from darkdork_integrations import SlackIntegration

slack = SlackIntegration('https://hooks.slack.com/services/YOUR/WEBHOOK/URL')

slack.send_notification(
    "Found exposed database file!",
    title="Critical Finding - DarkDork",
    severity="critical"
)
```

### Setting Up Burp Suite Integration

```python
from darkdork_integrations import BurpSuiteIntegration

# Burp Suite must be running with REST API extension
burp = BurpSuiteIntegration('localhost', 8080)

# Send discovered URLs to Burp
burp.send_to_burp('https://example.com/admin/login.php')
```

---

## Automation Examples

### Daily Scheduled Searches

```python
from darkdork_automation import TaskScheduler, ScheduledTask

scheduler = TaskScheduler()

# Create daily task
task = ScheduledTask(
    name="Daily Security Check",
    dork_query="filetype:pdf confidential",
    target_domain="example.com",
    schedule="daily",
    enabled=True
)

scheduler.add_task(task)

# Start scheduler (runs in background)
scheduler.run()

# Keep script running
import time
try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    scheduler.stop()
```

### Continuous Monitoring

```python
from darkdork_automation import ContinuousMonitor

monitor = ContinuousMonitor()

# Add monitors
monitor.add_monitor(
    "Production Environment",
    "site:example.com filetype:env",
    check_interval=3600  # Check every hour
)

monitor.start_monitoring()
```

### Complete Assessment Workflow

```python
from darkdork_automation import AutomationManager

manager = AutomationManager()

# Create comprehensive workflow
workflow_id = manager.create_security_assessment_workflow("client.com")

# Execute workflow
results = manager.workflow_engine.execute_workflow(workflow_id)

print(f"Workflow completed: {len(results)} steps")
```

---

## Troubleshooting

### Application Won't Start

```bash
# Check Python version
python --version  # Should be 3.7+

# Check tkinter is available
python -c "import tkinter; print('tkinter OK')"

# Run with error output
python darkdork.py 2>&1 | tee error.log
```

### Import Errors

```bash
# If you get import errors, ensure you're in the correct directory
cd /home/user/DarkDork

# Check PYTHONPATH
export PYTHONPATH=/home/user/DarkDork:$PYTHONPATH

# Or run as module
python -m darkdork
```

### Database Issues

```bash
# Reset database
rm darkdork.db

# Recreate tables
python -c "from darkdork_db import DarkDorkDatabase; db = DarkDorkDatabase(); print('Database recreated')"
```

### Export Issues

```bash
# Install optional dependencies
pip install reportlab python-docx

# Test exports
python darkdork_exports.py
```

---

## Best Practices

### Security Assessments

1. **Always get authorization** before testing
2. **Use project management** to segregate clients
3. **Export results regularly** for backup
4. **Tag searches** for organization
5. **Verify findings** before reporting
6. **Use rate limiting** (2-3 seconds minimum)

### Bug Bounty Hunting

1. **Use rapid preset** for faster searches
2. **Set up monitoring** for new programs
3. **Create custom dorks** for specific targets
4. **Export to JSON** for automation
5. **Track usage** in database

### Compliance Auditing

1. **Use compliance preset** (conservative)
2. **Export to PDF** for reports
3. **Document authorization** in project metadata
4. **Use tags** for compliance frameworks (PCI, HIPAA)
5. **Archive results** for audit trail

---

## Performance Tips

### Speed Up Searches

```python
# Use CLI for batch operations (faster than GUI)
python darkdork_cli.py -f dorks.txt -t example.com

# Reduce rate limit for internal testing (not for production!)
# In darkdork_config.json: "rate_limit_seconds": 1

# Use database for result caching
# Avoids re-searching same dorks
```

### Optimize Database

```bash
# Vacuum database periodically
sqlite3 darkdork.db "VACUUM;"

# Backup database
cp darkdork.db darkdork_backup_$(date +%Y%m%d).db
```

### Manage Disk Space

```bash
# Clean old exports
find . -name "*.pdf" -mtime +30 -delete
find . -name "*.csv" -mtime +30 -delete

# Archive old database
gzip darkdork_old.db
```

---

## Example Workflows

### Workflow 1: Quick Target Assessment

```bash
#!/bin/bash
TARGET="example.com"

echo "Starting assessment of $TARGET"

# Execute key categories
python darkdork_cli.py -c "Exposed Documents" -t $TARGET -e docs.json
python darkdork_cli.py -c "Login Pages" -t $TARGET -e logins.json
python darkdork_cli.py -c "Configuration" -t $TARGET -e configs.json

# Combine results
python -c "
import json
results = []
for f in ['docs.json', 'logins.json', 'configs.json']:
    with open(f) as file:
        results.extend(json.load(file))
with open('combined_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f'Total findings: {len(results)}')
"

echo "Assessment complete. Results in combined_results.json"
```

### Workflow 2: Continuous Monitoring

```python
#!/usr/bin/env python3
"""
Continuous monitoring script
Run with: nohup python monitor.py &
"""

from darkdork_automation import TaskScheduler, ScheduledTask
from darkdork_integrations import SlackIntegration
import time

# Setup
scheduler = TaskScheduler()
slack = SlackIntegration('YOUR_WEBHOOK_URL')

# Define targets
targets = ['example.com', 'example2.com', 'example3.com']
critical_dorks = [
    'filetype:env "DB_PASSWORD"',
    'intitle:"index of" database.sql',
    'filetype:sql "password"'
]

# Create tasks
for target in targets:
    for dork in critical_dorks:
        task = ScheduledTask(
            name=f"{target}: {dork[:30]}",
            dork_query=dork,
            target_domain=target,
            schedule="every_6h",
            enabled=True
        )
        scheduler.add_task(task)

# Start monitoring
slack.send_notification(
    f"Started monitoring {len(targets)} targets with {len(critical_dorks)} dorks",
    "DarkDork Monitor Started",
    "info"
)

scheduler.run()

# Keep running
try:
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    scheduler.stop()
    slack.send_notification(
        "Monitoring stopped",
        "DarkDork Monitor Stopped",
        "info"
    )
```

### Workflow 3: Professional Report Generation

```python
#!/usr/bin/env python3
"""
Generate professional assessment report
"""

from darkdork_db import DarkDorkDatabase
from darkdork_exports import ExportManager
from datetime import datetime

# Load data from database
db = DarkDorkDatabase('assessment.db')

# Get project
project_id = 1  # Replace with your project ID
project = db.get_project(project_id)

# Get all searches for project
searches = db.list_searches(project_id)

# Get all findings
findings = db.list_findings()

# Prepare data for export
report_data = []
for search in searches:
    results = db.get_results(search['id'])
    for result in results:
        report_data.append({
            'Date': search['executed_at'],
            'Dork': search['dork_query'],
            'URL': result['url'],
            'Title': result.get('title', 'N/A'),
            'Severity': result.get('severity', 'Info'),
            'Verified': 'Yes' if result.get('verified') else 'No'
        })

# Export to multiple formats
exporter = ExportManager()

client_name = project['name']
date_str = datetime.now().strftime('%Y%m%d')

# PDF for client
exporter.export_to_pdf(
    report_data,
    f'Report_{client_name}_{date_str}.pdf',
    title=f'Security Assessment - {client_name}',
    include_summary=True
)

# DOCX for editing
exporter.export_to_docx(
    report_data,
    f'Report_{client_name}_{date_str}.docx',
    title=f'Security Assessment - {client_name}'
)

# CSV for analysis
exporter.export_to_csv(
    report_data,
    f'Data_{client_name}_{date_str}.csv'
)

# JSON for archival
exporter.export_to_json(
    report_data,
    f'Archive_{client_name}_{date_str}.json'
)

print(f"Generated reports for {client_name}")
print(f"  - PDF: Report_{client_name}_{date_str}.pdf")
print(f"  - DOCX: Report_{client_name}_{date_str}.docx")
print(f"  - CSV: Data_{client_name}_{date_str}.csv")
print(f"  - JSON: Archive_{client_name}_{date_str}.json")
```

---

## Next Steps

1. **Try the quick start** above
2. **Explore the GUI** interface
3. **Test CLI commands** for automation
4. **Set up integrations** you need
5. **Create your first assessment** project
6. **Automate** recurring tasks
7. **Generate reports** for stakeholders

For detailed information, see:
- `docs/USER_MANUAL.md` - Complete 100+ page guide
- `QUICKSTART.md` - 5-minute quick start
- `docs/BUILD_GUIDE.md` - Packaging instructions

---

**Ready to start? Run:** `python darkdork.py`
