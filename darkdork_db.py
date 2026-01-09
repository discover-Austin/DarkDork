#!/usr/bin/env python3
"""
DarkDork Database System
SQLite database for persistent storage of searches, results, and analytics
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os


class DarkDorkDatabase:
    """Database management for DarkDork"""

    def __init__(self, db_path: str = "darkdork.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Create database tables"""

        # Projects table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                target_domain TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active',
                metadata TEXT
            )
        ''')

        # Searches table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                dork_query TEXT NOT NULL,
                target_domain TEXT,
                search_url TEXT,
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'executed',
                user_notes TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        ''')

        # Results table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_id INTEGER,
                url TEXT,
                title TEXT,
                snippet TEXT,
                found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                verified BOOLEAN DEFAULT 0,
                severity TEXT,
                notes TEXT,
                metadata TEXT,
                FOREIGN KEY (search_id) REFERENCES searches (id)
            )
        ''')

        # Tags table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Search-Tags relationship
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_tags (
                search_id INTEGER,
                tag_id INTEGER,
                PRIMARY KEY (search_id, tag_id),
                FOREIGN KEY (search_id) REFERENCES searches (id),
                FOREIGN KEY (tag_id) REFERENCES tags (id)
            )
        ''')

        # Analytics table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                event_data TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Findings table (for verified vulnerabilities)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                result_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                severity TEXT NOT NULL,
                cvss_score REAL,
                status TEXT DEFAULT 'open',
                reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                remediated_at TIMESTAMP,
                metadata TEXT,
                FOREIGN KEY (result_id) REFERENCES results (id)
            )
        ''')

        # Export history table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS exports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                format TEXT NOT NULL,
                filename TEXT NOT NULL,
                exported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                record_count INTEGER,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        ''')

        self.conn.commit()

        # Create indexes for performance
        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_searches_project
            ON searches(project_id)
        ''')

        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_results_search
            ON results(search_id)
        ''')

        self.cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_findings_severity
            ON findings(severity)
        ''')

        self.conn.commit()

    # Project Management
    def create_project(self, name: str, description: str = None,
                      target_domain: str = None, metadata: Dict = None) -> int:
        """Create a new project"""

        self.cursor.execute('''
            INSERT INTO projects (name, description, target_domain, metadata)
            VALUES (?, ?, ?, ?)
        ''', (name, description, target_domain, json.dumps(metadata or {})))

        self.conn.commit()
        return self.cursor.lastrowid

    def get_project(self, project_id: int) -> Optional[Dict]:
        """Get project by ID"""

        self.cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        row = self.cursor.fetchone()

        if row:
            return dict(row)
        return None

    def list_projects(self, status: str = None) -> List[Dict]:
        """List all projects"""

        if status:
            self.cursor.execute('SELECT * FROM projects WHERE status = ?', (status,))
        else:
            self.cursor.execute('SELECT * FROM projects')

        return [dict(row) for row in self.cursor.fetchall()]

    def update_project(self, project_id: int, **kwargs):
        """Update project fields"""

        allowed_fields = ['name', 'description', 'target_domain', 'status', 'metadata']
        updates = []
        values = []

        for key, value in kwargs.items():
            if key in allowed_fields:
                if key == 'metadata' and isinstance(value, dict):
                    value = json.dumps(value)
                updates.append(f"{key} = ?")
                values.append(value)

        if updates:
            values.append(project_id)
            query = f"UPDATE projects SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
            self.cursor.execute(query, values)
            self.conn.commit()

    # Search Management
    def record_search(self, dork_query: str, project_id: int = None,
                     target_domain: str = None, search_url: str = None,
                     user_notes: str = None) -> int:
        """Record a search"""

        self.cursor.execute('''
            INSERT INTO searches (project_id, dork_query, target_domain, search_url, user_notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (project_id, dork_query, target_domain, search_url, user_notes))

        self.conn.commit()
        return self.cursor.lastrowid

    def get_search(self, search_id: int) -> Optional[Dict]:
        """Get search by ID"""

        self.cursor.execute('SELECT * FROM searches WHERE id = ?', (search_id,))
        row = self.cursor.fetchone()

        if row:
            return dict(row)
        return None

    def list_searches(self, project_id: int = None, limit: int = 100) -> List[Dict]:
        """List searches"""

        if project_id:
            self.cursor.execute('''
                SELECT * FROM searches WHERE project_id = ?
                ORDER BY executed_at DESC LIMIT ?
            ''', (project_id, limit))
        else:
            self.cursor.execute('''
                SELECT * FROM searches ORDER BY executed_at DESC LIMIT ?
            ''', (limit,))

        return [dict(row) for row in self.cursor.fetchall()]

    # Result Management
    def add_result(self, search_id: int, url: str, title: str = None,
                   snippet: str = None, severity: str = None,
                   notes: str = None, metadata: Dict = None) -> int:
        """Add a search result"""

        self.cursor.execute('''
            INSERT INTO results (search_id, url, title, snippet, severity, notes, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (search_id, url, title, snippet, severity, notes, json.dumps(metadata or {})))

        self.conn.commit()
        return self.cursor.lastrowid

    def get_results(self, search_id: int) -> List[Dict]:
        """Get results for a search"""

        self.cursor.execute('''
            SELECT * FROM results WHERE search_id = ?
            ORDER BY found_at DESC
        ''', (search_id,))

        return [dict(row) for row in self.cursor.fetchall()]

    def verify_result(self, result_id: int, verified: bool = True, notes: str = None):
        """Mark a result as verified"""

        if notes:
            self.cursor.execute('''
                UPDATE results SET verified = ?, notes = ? WHERE id = ?
            ''', (verified, notes, result_id))
        else:
            self.cursor.execute('''
                UPDATE results SET verified = ? WHERE id = ?
            ''', (verified, result_id))

        self.conn.commit()

    # Findings Management (Verified Vulnerabilities)
    def create_finding(self, result_id: int, title: str, description: str,
                      severity: str, cvss_score: float = None,
                      metadata: Dict = None) -> int:
        """Create a verified finding"""

        self.cursor.execute('''
            INSERT INTO findings (result_id, title, description, severity, cvss_score, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (result_id, title, description, severity, cvss_score, json.dumps(metadata or {})))

        self.conn.commit()
        return self.cursor.lastrowid

    def list_findings(self, severity: str = None, status: str = None) -> List[Dict]:
        """List findings"""

        query = 'SELECT * FROM findings WHERE 1=1'
        params = []

        if severity:
            query += ' AND severity = ?'
            params.append(severity)

        if status:
            query += ' AND status = ?'
            params.append(status)

        query += ' ORDER BY reported_at DESC'

        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]

    def remediate_finding(self, finding_id: int):
        """Mark finding as remediated"""

        self.cursor.execute('''
            UPDATE findings
            SET status = 'remediated', remediated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (finding_id,))

        self.conn.commit()

    # Tag Management
    def create_tag(self, name: str, color: str = None) -> int:
        """Create a tag"""

        try:
            self.cursor.execute('''
                INSERT INTO tags (name, color) VALUES (?, ?)
            ''', (name, color))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            # Tag already exists
            self.cursor.execute('SELECT id FROM tags WHERE name = ?', (name,))
            return self.cursor.fetchone()[0]

    def tag_search(self, search_id: int, tag_name: str):
        """Tag a search"""

        tag_id = self.create_tag(tag_name)

        try:
            self.cursor.execute('''
                INSERT INTO search_tags (search_id, tag_id) VALUES (?, ?)
            ''', (search_id, tag_id))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass  # Already tagged

    def get_search_tags(self, search_id: int) -> List[str]:
        """Get tags for a search"""

        self.cursor.execute('''
            SELECT t.name FROM tags t
            JOIN search_tags st ON t.id = st.tag_id
            WHERE st.search_id = ?
        ''', (search_id,))

        return [row[0] for row in self.cursor.fetchall()]

    # Analytics
    def record_analytics(self, event_type: str, event_data: Dict = None):
        """Record analytics event"""

        self.cursor.execute('''
            INSERT INTO analytics (event_type, event_data)
            VALUES (?, ?)
        ''', (event_type, json.dumps(event_data or {})))

        self.conn.commit()

    def get_analytics_summary(self, days: int = 30) -> Dict:
        """Get analytics summary"""

        # Total searches
        self.cursor.execute('''
            SELECT COUNT(*) FROM searches
            WHERE executed_at >= datetime('now', '-' || ? || ' days')
        ''', (days,))
        total_searches = self.cursor.fetchone()[0]

        # Searches by day
        self.cursor.execute('''
            SELECT DATE(executed_at) as date, COUNT(*) as count
            FROM searches
            WHERE executed_at >= datetime('now', '-' || ? || ' days')
            GROUP BY DATE(executed_at)
            ORDER BY date
        ''', (days,))
        searches_by_day = [dict(row) for row in self.cursor.fetchall()]

        # Top dorks
        self.cursor.execute('''
            SELECT dork_query, COUNT(*) as count
            FROM searches
            WHERE executed_at >= datetime('now', '-' || ? || ' days')
            GROUP BY dork_query
            ORDER BY count DESC
            LIMIT 10
        ''', (days,))
        top_dorks = [dict(row) for row in self.cursor.fetchall()]

        # Findings by severity
        self.cursor.execute('''
            SELECT severity, COUNT(*) as count
            FROM findings
            WHERE status = 'open'
            GROUP BY severity
        ''')
        findings_by_severity = {row[0]: row[1] for row in self.cursor.fetchall()}

        return {
            'total_searches': total_searches,
            'searches_by_day': searches_by_day,
            'top_dorks': top_dorks,
            'findings_by_severity': findings_by_severity
        }

    # Export History
    def record_export(self, project_id: int, format: str,
                     filename: str, record_count: int):
        """Record an export"""

        self.cursor.execute('''
            INSERT INTO exports (project_id, format, filename, record_count)
            VALUES (?, ?, ?, ?)
        ''', (project_id, format, filename, record_count))

        self.conn.commit()

    # Statistics
    def get_statistics(self) -> Dict:
        """Get overall statistics"""

        stats = {}

        # Total counts
        self.cursor.execute('SELECT COUNT(*) FROM projects')
        stats['total_projects'] = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT COUNT(*) FROM searches')
        stats['total_searches'] = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT COUNT(*) FROM results')
        stats['total_results'] = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT COUNT(*) FROM findings WHERE status = "open"')
        stats['open_findings'] = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT COUNT(*) FROM findings WHERE status = "remediated"')
        stats['remediated_findings'] = self.cursor.fetchone()[0]

        # Recent activity
        self.cursor.execute('''
            SELECT COUNT(*) FROM searches
            WHERE executed_at >= datetime('now', '-7 days')
        ''')
        stats['searches_last_7_days'] = self.cursor.fetchone()[0]

        return stats

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


def test_database():
    """Test database functionality"""

    with DarkDorkDatabase('test_darkdork.db') as db:
        # Create a project
        project_id = db.create_project(
            "Test Security Assessment",
            "Testing the database system",
            "example.com"
        )
        print(f"Created project: {project_id}")

        # Record a search
        search_id = db.record_search(
            "filetype:pdf confidential",
            project_id=project_id,
            target_domain="example.com"
        )
        print(f"Recorded search: {search_id}")

        # Add results
        result_id = db.add_result(
            search_id,
            "https://example.com/confidential.pdf",
            "Confidential Document",
            "This is a confidential document...",
            severity="High"
        )
        print(f"Added result: {result_id}")

        # Verify result
        db.verify_result(result_id, True, "Confirmed exposure")
        print("Verified result")

        # Create finding
        finding_id = db.create_finding(
            result_id,
            "Exposed Confidential Document",
            "Confidential PDF is publicly accessible",
            "High",
            cvss_score=7.5
        )
        print(f"Created finding: {finding_id}")

        # Tag search
        db.tag_search(search_id, "documents")
        db.tag_search(search_id, "high-priority")
        print("Tagged search")

        # Get statistics
        stats = db.get_statistics()
        print(f"\nStatistics: {stats}")


if __name__ == '__main__':
    test_database()
