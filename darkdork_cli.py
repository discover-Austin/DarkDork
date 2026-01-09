#!/usr/bin/env python3
"""
DarkDork Command-Line Interface
For automation, scripting, and headless operation
"""

import argparse
import sys
import json
import csv
import time
import webbrowser
from datetime import datetime
from typing import List, Dict
import urllib.parse

try:
    from darkdork_library import DorkLibrary
except ImportError:
    print("Warning: darkdork_library.py not found. Limited functionality.")
    DorkLibrary = None


class DarkDorkCLI:
    """Command-line interface for DarkDork"""

    def __init__(self):
        self.library = DorkLibrary() if DorkLibrary else None
        self.results = []
        self.config = self.load_config()

    def load_config(self) -> Dict:
        """Load configuration"""
        try:
            with open('darkdork_config.json', 'r') as f:
                return json.load(f)
        except:
            return {
                'rate_limit_seconds': 2,
                'default_export_format': 'json'
            }

    def build_search_url(self, dork: str, target: str = None) -> str:
        """Build Google search URL"""
        if target:
            dork = f"site:{target} {dork}"

        encoded = urllib.parse.quote(dork)
        return f"https://www.google.com/search?q={encoded}"

    def execute_dork(self, dork: str, target: str = None,
                    open_browser: bool = False, record: bool = True):
        """Execute a single dork"""

        url = self.build_search_url(dork, target)
        timestamp = datetime.now().isoformat()

        result = {
            'timestamp': timestamp,
            'dork': dork,
            'target': target,
            'url': url,
            'status': 'executed'
        }

        if open_browser:
            webbrowser.open(url)

        if record:
            self.results.append(result)

        print(f"[{timestamp}] Executed: {dork}")
        print(f"  URL: {url}")

        return result

    def execute_batch(self, dorks: List[str], target: str = None,
                     open_browser: bool = False, delay: float = None):
        """Execute multiple dorks with rate limiting"""

        if delay is None:
            delay = self.config.get('rate_limit_seconds', 2)

        print(f"Executing {len(dorks)} dorks with {delay}s delay...")

        for i, dork in enumerate(dorks, 1):
            print(f"\n[{i}/{len(dorks)}]")
            self.execute_dork(dork, target, open_browser)

            if i < len(dorks):
                time.sleep(delay)

        print(f"\nCompleted {len(dorks)} dorks")

    def execute_category(self, category: str, target: str = None,
                        open_browser: bool = False):
        """Execute all dorks in a category"""

        if not self.library:
            print("Error: Library system not available")
            return

        dorks = self.library.search_dorks(category=category)

        if not dorks:
            print(f"No dorks found in category: {category}")
            return

        print(f"Found {len(dorks)} dorks in category '{category}'")

        queries = [d['query'] for d in dorks]
        self.execute_batch(queries, target, open_browser)

    def execute_file(self, filename: str, target: str = None,
                    open_browser: bool = False):
        """Execute dorks from a file"""

        try:
            with open(filename, 'r') as f:
                dorks = [line.strip() for line in f if line.strip()
                        and not line.strip().startswith('#')]

            print(f"Loaded {len(dorks)} dorks from {filename}")
            self.execute_batch(dorks, target, open_browser)

        except Exception as e:
            print(f"Error reading file: {e}")

    def search_library(self, query: str = None, category: str = None,
                      tags: List[str] = None, severity: str = None):
        """Search the dork library"""

        if not self.library:
            print("Error: Library system not available")
            return

        results = self.library.search_dorks(query, category, tags, severity)

        if not results:
            print("No dorks found matching criteria")
            return

        print(f"\nFound {len(results)} dorks:\n")

        for dork in results:
            print(f"[{dork['id']}] {dork['name']}")
            print(f"  Category: {dork['category']} | Severity: {dork['severity']}")
            print(f"  Query: {dork['query']}")
            print(f"  Tags: {', '.join(dork.get('tags', []))}")
            print()

    def list_categories(self):
        """List all available categories"""

        if not self.library:
            print("Error: Library system not available")
            return

        print("\nAvailable Categories:\n")
        for i, category in enumerate(sorted(self.library.categories), 1):
            count = len([d for d in self.library.dorks
                        if d['category'] == category])
            print(f"{i}. {category} ({count} dorks)")

    def show_statistics(self):
        """Show library statistics"""

        if not self.library:
            print("Error: Library system not available")
            return

        stats = self.library.get_statistics()

        print("\n=== DarkDork Library Statistics ===\n")
        print(f"Total Dorks: {stats['total_dorks']}")
        print(f"Categories: {stats['categories']}")
        print(f"Tags: {stats['tags']}")
        print(f"Average Usage: {stats['average_usage']:.2f}")

        print("\nSeverity Breakdown:")
        for severity, count in stats['severity_breakdown'].items():
            print(f"  {severity}: {count}")

        if 'most_popular' in stats and stats['most_popular']:
            print("\nMost Popular Dorks:")
            for dork in stats['most_popular']:
                print(f"  - {dork['name']} (used {dork.get('usage_count', 0)} times)")

    def export_results(self, filename: str, format: str = None):
        """Export results to file"""

        if not self.results:
            print("No results to export")
            return

        if format is None:
            if filename.endswith('.csv'):
                format = 'csv'
            elif filename.endswith('.json'):
                format = 'json'
            else:
                format = self.config.get('default_export_format', 'json')

        try:
            if format == 'json':
                with open(filename, 'w') as f:
                    json.dump(self.results, f, indent=2)

            elif format == 'csv':
                with open(filename, 'w', newline='') as f:
                    if self.results:
                        writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
                        writer.writeheader()
                        writer.writerows(self.results)

            else:
                with open(filename, 'w') as f:
                    for result in self.results:
                        f.write(f"[{result['timestamp']}] {result['dork']}\n")
                        f.write(f"  URL: {result['url']}\n\n")

            print(f"Exported {len(self.results)} results to {filename}")

        except Exception as e:
            print(f"Error exporting results: {e}")


def main():
    """Main CLI entry point"""

    parser = argparse.ArgumentParser(
        description='DarkDork - Professional Google Dorking Tool (CLI)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Execute a single dork
  %(prog)s -d "filetype:pdf confidential" -t example.com

  # Execute multiple dorks from file
  %(prog)s -f dorks.txt -t example.com

  # Execute all dorks in a category
  %(prog)s -c "Exposed Documents" -t example.com

  # Search the library
  %(prog)s --search "password" --severity Critical

  # List all categories
  %(prog)s --list-categories

  # Show statistics
  %(prog)s --stats

  # Execute and export results
  %(prog)s -d "filetype:sql" -t example.com -e results.json
        """
    )

    # Execution options
    exec_group = parser.add_argument_group('Execution Options')
    exec_group.add_argument('-d', '--dork', type=str,
                           help='Execute a single dork query')
    exec_group.add_argument('-f', '--file', type=str,
                           help='Execute dorks from file (one per line)')
    exec_group.add_argument('-c', '--category', type=str,
                           help='Execute all dorks in category')
    exec_group.add_argument('-t', '--target', type=str,
                           help='Target domain to search')
    exec_group.add_argument('-b', '--browser', action='store_true',
                           help='Open results in browser')
    exec_group.add_argument('--delay', type=float,
                           help='Delay between searches (seconds)')

    # Search options
    search_group = parser.add_argument_group('Library Search Options')
    search_group.add_argument('--search', type=str,
                             help='Search library by keyword')
    search_group.add_argument('--severity', type=str,
                             choices=['Critical', 'High', 'Medium', 'Low', 'Info'],
                             help='Filter by severity')
    search_group.add_argument('--tags', type=str, nargs='+',
                             help='Filter by tags')

    # Info options
    info_group = parser.add_argument_group('Information Options')
    info_group.add_argument('--list-categories', action='store_true',
                           help='List all available categories')
    info_group.add_argument('--stats', action='store_true',
                           help='Show library statistics')

    # Export options
    export_group = parser.add_argument_group('Export Options')
    export_group.add_argument('-e', '--export', type=str,
                             help='Export results to file')
    export_group.add_argument('--format', type=str,
                             choices=['json', 'csv', 'txt'],
                             help='Export format (default: auto-detect)')

    # Other options
    parser.add_argument('--version', action='version', version='DarkDork CLI 1.0.0')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    # Create CLI instance
    cli = DarkDorkCLI()

    # Handle info options
    if args.list_categories:
        cli.list_categories()
        return

    if args.stats:
        cli.show_statistics()
        return

    # Handle search
    if args.search or args.severity or args.tags:
        cli.search_library(args.search, None, args.tags, args.severity)
        return

    # Handle execution
    executed = False

    if args.dork:
        cli.execute_dork(args.dork, args.target, args.browser)
        executed = True

    elif args.file:
        cli.execute_file(args.file, args.target, args.browser)
        executed = True

    elif args.category:
        cli.execute_category(args.category, args.target, args.browser)
        executed = True

    # Export if requested
    if executed and args.export:
        cli.export_results(args.export, args.format)

    # Show help if nothing was done
    if not executed and not any([args.list_categories, args.stats,
                                 args.search, args.severity, args.tags]):
        parser.print_help()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
