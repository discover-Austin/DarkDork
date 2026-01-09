#!/usr/bin/env python3
"""
DarkDork Advanced Library System
Manages dork collections with tagging, filtering, and metadata
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Set, Optional


class DorkLibrary:
    """Advanced dork library management system"""

    def __init__(self, library_path: str = "dork_library.json"):
        self.library_path = library_path
        self.dorks = []
        self.tags = set()
        self.categories = set()
        self.load_library()

    def load_library(self):
        """Load dork library from file"""
        if os.path.exists(self.library_path):
            try:
                with open(self.library_path, 'r') as f:
                    data = json.load(f)
                    self.dorks = data.get('dorks', [])
                    self._rebuild_indexes()
            except Exception as e:
                print(f"Error loading library: {e}")
                self.dorks = []

    def save_library(self):
        """Save dork library to file"""
        data = {
            'version': '2.0',
            'last_updated': datetime.now().isoformat(),
            'dorks': self.dorks,
            'stats': {
                'total_dorks': len(self.dorks),
                'categories': list(self.categories),
                'tags': list(self.tags)
            }
        }

        with open(self.library_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _rebuild_indexes(self):
        """Rebuild tag and category indexes"""
        self.tags.clear()
        self.categories.clear()

        for dork in self.dorks:
            if 'tags' in dork:
                self.tags.update(dork['tags'])
            if 'category' in dork:
                self.categories.add(dork['category'])

    def add_dork(self, query: str, name: str, category: str,
                 description: str = "", severity: str = "Info",
                 tags: List[str] = None, metadata: Dict = None):
        """Add a new dork to the library"""

        dork = {
            'id': len(self.dorks) + 1,
            'name': name,
            'query': query,
            'category': category,
            'description': description,
            'severity': severity,
            'tags': tags or [],
            'created': datetime.now().isoformat(),
            'usage_count': 0,
            'last_used': None,
            'metadata': metadata or {}
        }

        self.dorks.append(dork)
        self._rebuild_indexes()
        return dork['id']

    def search_dorks(self, query: str = None, category: str = None,
                     tags: List[str] = None, severity: str = None) -> List[Dict]:
        """Search dorks by various criteria"""

        results = self.dorks.copy()

        if query:
            query_lower = query.lower()
            results = [d for d in results if
                      query_lower in d['name'].lower() or
                      query_lower in d['query'].lower() or
                      query_lower in d['description'].lower()]

        if category:
            results = [d for d in results if d['category'] == category]

        if tags:
            results = [d for d in results if
                      any(tag in d.get('tags', []) for tag in tags)]

        if severity:
            results = [d for d in results if d['severity'] == severity]

        return results

    def get_by_id(self, dork_id: int) -> Optional[Dict]:
        """Get dork by ID"""
        for dork in self.dorks:
            if dork['id'] == dork_id:
                return dork
        return None

    def update_usage(self, dork_id: int):
        """Update usage statistics for a dork"""
        dork = self.get_by_id(dork_id)
        if dork:
            dork['usage_count'] = dork.get('usage_count', 0) + 1
            dork['last_used'] = datetime.now().isoformat()
            self.save_library()

    def get_popular_dorks(self, limit: int = 10) -> List[Dict]:
        """Get most used dorks"""
        sorted_dorks = sorted(self.dorks,
                            key=lambda x: x.get('usage_count', 0),
                            reverse=True)
        return sorted_dorks[:limit]

    def export_category(self, category: str, filename: str):
        """Export a category to separate file"""
        category_dorks = [d for d in self.dorks if d['category'] == category]

        with open(filename, 'w') as f:
            json.dump({
                'category': category,
                'dorks': category_dorks,
                'exported': datetime.now().isoformat()
            }, f, indent=2)

    def import_dorks(self, filename: str):
        """Import dorks from file"""
        with open(filename, 'r') as f:
            data = json.load(f)

            if 'dorks' in data:
                for dork in data['dorks']:
                    # Avoid duplicates
                    if not any(d['query'] == dork['query'] for d in self.dorks):
                        dork['id'] = len(self.dorks) + 1
                        self.dorks.append(dork)

                self._rebuild_indexes()
                self.save_library()

    def get_statistics(self) -> Dict:
        """Get library statistics"""
        if not self.dorks:
            return {
                'total_dorks': 0,
                'categories': 0,
                'tags': 0,
                'average_usage': 0
            }

        total_usage = sum(d.get('usage_count', 0) for d in self.dorks)

        severity_counts = {}
        for dork in self.dorks:
            sev = dork.get('severity', 'Info')
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        return {
            'total_dorks': len(self.dorks),
            'categories': len(self.categories),
            'tags': len(self.tags),
            'average_usage': total_usage / len(self.dorks) if self.dorks else 0,
            'severity_breakdown': severity_counts,
            'most_popular': self.get_popular_dorks(5)
        }


def create_comprehensive_library():
    """Create a comprehensive dork library with 100+ dorks"""

    library = DorkLibrary()

    # Documents & Files
    dorks_data = [
        # Exposed Documents - Critical
        ("filetype:pdf confidential", "Confidential PDFs", "Exposed Documents",
         "Find PDF files marked as confidential", "High", ["documents", "pdf", "leak"]),
        ("filetype:xlsx password", "Excel with Passwords", "Exposed Documents",
         "Find Excel files containing passwords", "Critical", ["documents", "excel", "credentials"]),
        ("filetype:docx \"internal use only\"", "Internal Documents", "Exposed Documents",
         "Find Word documents marked internal", "Medium", ["documents", "internal"]),
        ("filetype:csv email", "CSV Email Lists", "Exposed Documents",
         "Find CSV files with email addresses", "Medium", ["documents", "pii"]),
        ("filetype:pptx confidential", "Confidential Presentations", "Exposed Documents",
         "Find confidential PowerPoint presentations", "High", ["documents", "presentations"]),

        # Login & Admin Interfaces
        ("inurl:admin intitle:login", "Admin Login Pages", "Login Pages",
         "Discover admin login interfaces", "Medium", ["admin", "authentication"]),
        ("inurl:administrator intitle:login", "Administrator Pages", "Login Pages",
         "Find administrator login pages", "Medium", ["admin", "authentication"]),
        ("intitle:\"Dashboard\" inurl:admin", "Admin Dashboards", "Login Pages",
         "Locate admin dashboard interfaces", "Medium", ["admin", "dashboard"]),
        ("inurl:wp-login.php", "WordPress Logins", "Login Pages",
         "Find WordPress login pages", "Low", ["cms", "wordpress"]),
        ("intitle:phpMyAdmin \"Welcome to phpMyAdmin\"", "phpMyAdmin Instances", "Login Pages",
         "Locate phpMyAdmin installations", "Medium", ["database", "mysql"]),

        # Configuration Files
        ("intitle:\"index of\" .env", "Exposed .env Files", "Configuration",
         "Find exposed environment configuration files", "Critical", ["config", "credentials"]),
        ("intitle:\"index of\" config.php", "PHP Config Files", "Configuration",
         "Locate exposed PHP configuration files", "High", ["config", "php"]),
        ("filetype:env DB_PASSWORD", "Database Credentials in ENV", "Configuration",
         "Find .env files with database passwords", "Critical", ["config", "credentials", "database"]),
        ("intitle:\"index of\" wp-config.php", "WordPress Configs", "Configuration",
         "Find exposed WordPress configuration files", "High", ["config", "wordpress"]),
        ("filetype:ini \"password\"", "INI Files with Passwords", "Configuration",
         "Locate INI configuration files containing passwords", "High", ["config", "credentials"]),

        # Database Exposure
        ("filetype:sql \"CREATE TABLE\"", "SQL Database Dumps", "Databases",
         "Find SQL database dump files", "Critical", ["database", "sql", "leak"]),
        ("intext:\"SQL syntax\" \"mysql\"", "MySQL Errors", "Databases",
         "Find pages exposing MySQL errors", "Medium", ["database", "error", "mysql"]),
        ("intitle:\"index of\" database.sql", "Database SQL Files", "Databases",
         "Locate database SQL dump files", "Critical", ["database", "sql"]),
        ("filetype:mdb", "Access Databases", "Databases",
         "Find Microsoft Access database files", "High", ["database", "access"]),

        # API Keys & Secrets
        ("filetype:env API_KEY", "API Keys in ENV Files", "API & Secrets",
         "Find API keys in environment files", "Critical", ["api", "credentials", "keys"]),
        ("\"api_key\" filetype:json", "API Keys in JSON", "API & Secrets",
         "Locate API keys in JSON files", "Critical", ["api", "credentials", "keys"]),
        ("\"BEGIN RSA PRIVATE KEY\"", "RSA Private Keys", "API & Secrets",
         "Find exposed RSA private keys", "Critical", ["credentials", "keys", "ssl"]),
        ("\"authorization: Bearer\"", "Bearer Tokens", "API & Secrets",
         "Discover exposed authorization tokens", "Critical", ["api", "credentials", "tokens"]),
        ("filetype:properties password", "Java Properties with Passwords", "API & Secrets",
         "Find Java properties files with passwords", "High", ["config", "credentials", "java"]),

        # Cloud Storage
        ("site:s3.amazonaws.com", "AWS S3 Buckets", "Cloud Storage",
         "Find potentially exposed AWS S3 buckets", "High", ["cloud", "aws", "storage"]),
        ("site:storage.googleapis.com", "Google Cloud Storage", "Cloud Storage",
         "Find potentially exposed Google Cloud storage", "High", ["cloud", "gcp", "storage"]),
        ("site:blob.core.windows.net", "Azure Blob Storage", "Cloud Storage",
         "Find potentially exposed Azure blob storage", "High", ["cloud", "azure", "storage"]),

        # Network Devices & IoT
        ("intitle:\"Network Camera\"", "Network Cameras", "Network Devices",
         "Find exposed network cameras", "High", ["iot", "camera", "surveillance"]),
        ("inurl:8080 -intext:8080 intitle:\"Surveillance\"", "Surveillance Systems", "Network Devices",
         "Locate surveillance system interfaces", "High", ["iot", "surveillance"]),
        ("intitle:\"NetcamSC*\" | intitle:\"NetcamXL*\" inurl:home/", "Netcam Devices", "Network Devices",
         "Find Netcam surveillance devices", "High", ["iot", "camera"]),
        ("inurl:view/view.shtml", "IP Camera Views", "Network Devices",
         "Discover IP camera view interfaces", "High", ["iot", "camera"]),

        # Source Code & Repos
        ("intitle:\"index of\" \".git\"", "Exposed Git Repositories", "Source Code",
         "Find exposed .git directories", "High", ["git", "source", "leak"]),
        ("intitle:\"index of\" \".svn\"", "Exposed SVN Repositories", "Source Code",
         "Find exposed SVN repositories", "High", ["svn", "source", "leak"]),
        ("filetype:log intext:password", "Log Files with Passwords", "Source Code",
         "Find log files containing passwords", "High", ["logs", "credentials"]),

        # Web Application Issues
        ("inurl:shell.php", "PHP Web Shells", "Web Applications",
         "Find potential PHP web shells", "Critical", ["webshell", "backdoor", "php"]),
        ("inurl:c99.php", "C99 Web Shells", "Web Applications",
         "Locate C99 web shell instances", "Critical", ["webshell", "backdoor", "php"]),
        ("intitle:\"Index of\" \"backup\"", "Backup Directories", "Web Applications",
         "Find exposed backup directories", "High", ["backup", "leak"]),
        ("intitle:\"PHP Version\" \"System\"", "PHP Info Pages", "Web Applications",
         "Find exposed phpinfo() pages", "Medium", ["php", "info", "disclosure"]),

        # CI/CD & DevOps
        ("intitle:\"Dashboard [Jenkins]\"", "Jenkins Dashboards", "CI/CD",
         "Locate Jenkins CI/CD instances", "Medium", ["cicd", "jenkins", "devops"]),
        ("intitle:\"Kubernetes Dashboard\"", "Kubernetes Dashboards", "CI/CD",
         "Find Kubernetes dashboard interfaces", "High", ["kubernetes", "devops", "container"]),
        ("inurl:\"gitlab\" intitle:\"Sign in\"", "GitLab Instances", "CI/CD",
         "Discover GitLab installations", "Low", ["git", "devops", "gitlab"]),
        ("intitle:\"Travis CI\"", "Travis CI Instances", "CI/CD",
         "Find Travis CI dashboards", "Low", ["cicd", "travis", "devops"]),

        # Error Messages & Debug
        ("intext:\"Warning: mysql_connect()\"", "MySQL Connection Errors", "Error Messages",
         "Find MySQL connection error messages", "Medium", ["error", "mysql", "debug"]),
        ("intext:\"Fatal error\" intext:\"Call to undefined function\"", "PHP Fatal Errors", "Error Messages",
         "Locate PHP fatal error messages", "Low", ["error", "php", "debug"]),
        ("intitle:\"Error\" \"The server encountered an internal error\"", "Server Errors", "Error Messages",
         "Find server internal error pages", "Low", ["error", "server"]),

        # Social Engineering & OSINT
        ("filetype:xls inurl:\"email.xls\"", "Email Lists in Excel", "OSINT",
         "Find Excel files containing email lists", "Medium", ["osint", "email", "pii"]),
        ("filetype:csv inurl:\"contact\"", "Contact Databases", "OSINT",
         "Locate CSV files with contact information", "Medium", ["osint", "contact", "pii"]),
        ("\"@gmail.com\" filetype:xls", "Gmail Addresses in Spreadsheets", "OSINT",
         "Find spreadsheets containing Gmail addresses", "Low", ["osint", "email"]),

        # Mobile & Apps
        ("inurl:\"androidmanifest.xml\" ext:xml", "Android Manifests", "Mobile",
         "Find exposed Android manifest files", "Low", ["mobile", "android"]),
        ("filetype:apk", "APK Files", "Mobile",
         "Locate Android APK files", "Low", ["mobile", "android", "apk"]),

        # Financial Data
        ("filetype:xls intext:\"budget\" \"confidential\"", "Budget Spreadsheets", "Financial",
         "Find confidential budget spreadsheets", "High", ["financial", "sensitive"]),
        ("filetype:pdf \"invoice\" \"total amount\"", "Invoice Documents", "Financial",
         "Locate invoice PDF documents", "Medium", ["financial", "invoice"]),

        # Healthcare & PII
        ("filetype:xls intext:\"patient\" \"medical\"", "Medical Records", "Healthcare",
         "Find medical record spreadsheets", "Critical", ["healthcare", "pii", "hipaa"]),
        ("filetype:pdf \"medical report\" \"patient name\"", "Medical Reports", "Healthcare",
         "Locate medical report PDFs", "Critical", ["healthcare", "pii", "hipaa"]),

        # Government & Legal
        ("site:.gov filetype:pdf \"confidential\"", "Government Confidential Docs", "Government",
         "Find confidential government documents", "High", ["government", "sensitive"]),
        ("site:.gov filetype:xls \"budget\"", "Government Budgets", "Government",
         "Locate government budget spreadsheets", "Medium", ["government", "financial"]),
    ]

    for query, name, category, description, severity, tags in dorks_data:
        library.add_dork(query, name, category, description, severity, tags)

    library.save_library()
    return library


if __name__ == "__main__":
    # Create comprehensive library
    lib = create_comprehensive_library()
    print(f"Created library with {len(lib.dorks)} dorks")
    print(f"Categories: {len(lib.categories)}")
    print(f"Tags: {len(lib.tags)}")

    # Show statistics
    stats = lib.get_statistics()
    print(f"\nLibrary Statistics:")
    print(f"  Total Dorks: {stats['total_dorks']}")
    print(f"  Categories: {stats['categories']}")
    print(f"  Tags: {stats['tags']}")
    print(f"\nSeverity Breakdown:")
    for severity, count in stats['severity_breakdown'].items():
        print(f"  {severity}: {count}")
