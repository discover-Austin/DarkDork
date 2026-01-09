#!/usr/bin/env python3
"""
DarkDork Automatic Update System
Check for updates, download, and install new versions
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import hashlib


class Version:
    """Version handling"""

    def __init__(self, version_string: str):
        parts = version_string.split('.')
        self.major = int(parts[0]) if len(parts) > 0 else 0
        self.minor = int(parts[1]) if len(parts) > 1 else 0
        self.patch = int(parts[2]) if len(parts) > 2 else 0

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __eq__(self, other):
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)

    def __lt__(self, other):
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

    def __gt__(self, other):
        return (self.major, self.minor, self.patch) > (other.major, other.minor, other.patch)


class UpdateChecker:
    """Check for software updates"""

    def __init__(self, current_version: str, update_url: str = None):
        self.current_version = Version(current_version)
        self.update_url = update_url or "https://api.darkdork.com/updates"
        self.config_file = "update_config.json"
        self.config = self.load_config()

    def load_config(self) -> Dict:
        """Load update configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        return {
            'auto_check': True,
            'last_check': None,
            'check_interval_days': 7,
            'update_channel': 'stable'  # stable, beta, nightly
        }

    def save_config(self):
        """Save update configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def should_check_for_updates(self) -> bool:
        """Determine if we should check for updates"""
        if not self.config.get('auto_check', True):
            return False

        last_check = self.config.get('last_check')
        if not last_check:
            return True

        last_check_date = datetime.fromisoformat(last_check)
        check_interval = timedelta(days=self.config.get('check_interval_days', 7))

        return datetime.now() - last_check_date > check_interval

    def check_for_updates(self) -> Optional[Dict]:
        """
        Check for available updates
        Note: Requires 'requests' package for actual HTTP requests
        """
        try:
            # In production, this would make an HTTP request
            # For now, return mock update info
            import requests

            params = {
                'current_version': str(self.current_version),
                'channel': self.config.get('update_channel', 'stable')
            }

            response = requests.get(self.update_url, params=params, timeout=10)

            if response.status_code == 200:
                update_info = response.json()

                # Update last check time
                self.config['last_check'] = datetime.now().isoformat()
                self.save_config()

                return update_info

        except ImportError:
            # requests not installed, return mock data
            print("Note: requests package not installed, using mock data")
            return self._get_mock_update_info()

        except Exception as e:
            print(f"Error checking for updates: {e}")

        return None

    def _get_mock_update_info(self) -> Dict:
        """Get mock update info for testing"""
        latest_version = Version("1.1.0")

        if latest_version > self.current_version:
            return {
                'update_available': True,
                'latest_version': str(latest_version),
                'current_version': str(self.current_version),
                'release_date': '2026-01-15',
                'download_url': 'https://downloads.darkdork.com/DarkDork-1.1.0.exe',
                'changelog': [
                    'Added new dork categories',
                    'Improved export functionality',
                    'Bug fixes and performance improvements'
                ],
                'is_critical': False,
                'file_size': '25.3 MB',
                'checksum': 'sha256:abcd1234...'
            }
        else:
            return {
                'update_available': False,
                'latest_version': str(self.current_version),
                'current_version': str(self.current_version),
                'message': 'You are running the latest version'
            }

    def download_update(self, download_url: str, save_path: str,
                       checksum: str = None) -> bool:
        """
        Download update file
        Note: Requires 'requests' package
        """
        try:
            import requests

            print(f"Downloading update from {download_url}...")

            response = requests.get(download_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))

            with open(save_path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)

                    # Show progress
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\rProgress: {percent:.1f}%", end='')

            print("\nDownload complete!")

            # Verify checksum if provided
            if checksum:
                if self._verify_checksum(save_path, checksum):
                    print("✓ Checksum verified")
                    return True
                else:
                    print("✗ Checksum verification failed!")
                    os.remove(save_path)
                    return False

            return True

        except ImportError:
            print("Error: requests package not installed")
            return False

        except Exception as e:
            print(f"Error downloading update: {e}")
            return False

    def _verify_checksum(self, filepath: str, expected_checksum: str) -> bool:
        """Verify file checksum"""
        try:
            # Extract algorithm and hash
            algorithm, expected_hash = expected_checksum.split(':', 1)

            # Calculate file hash
            hash_func = hashlib.new(algorithm)

            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_func.update(chunk)

            calculated_hash = hash_func.hexdigest()

            return calculated_hash == expected_hash

        except Exception as e:
            print(f"Error verifying checksum: {e}")
            return False

    def get_update_notification(self) -> Optional[str]:
        """Get user-friendly update notification"""
        if not self.should_check_for_updates():
            return None

        update_info = self.check_for_updates()

        if not update_info:
            return None

        if not update_info.get('update_available'):
            return None

        message = f"Update Available: v{update_info['latest_version']}\n\n"

        if update_info.get('is_critical'):
            message += "⚠️ This is a critical security update!\n\n"

        message += "What's New:\n"
        for change in update_info.get('changelog', []):
            message += f"  • {change}\n"

        message += f"\nSize: {update_info.get('file_size', 'Unknown')}\n"
        message += f"Released: {update_info.get('release_date')}\n"

        return message


class AutoUpdater:
    """Automatic update system"""

    def __init__(self, current_version: str):
        self.checker = UpdateChecker(current_version)
        self.update_log = []

    def check_and_notify(self) -> Tuple[bool, Optional[str]]:
        """Check for updates and return notification"""
        notification = self.checker.get_update_notification()

        if notification:
            return True, notification

        return False, None

    def install_update(self, update_info: Dict, install_path: str) -> bool:
        """Download and install update"""
        try:
            download_url = update_info.get('download_url')
            checksum = update_info.get('checksum')

            if not download_url:
                return False

            # Download update
            temp_file = f"darkdork_update_{update_info['latest_version']}.exe"

            if not self.checker.download_update(download_url, temp_file, checksum):
                return False

            # Log update
            self.log_update(update_info, 'downloaded')

            print(f"\n✓ Update downloaded to: {temp_file}")
            print("\nTo install:")
            print(f"  1. Close DarkDork")
            print(f"  2. Run: {temp_file}")
            print(f"  3. Follow installation wizard")

            return True

        except Exception as e:
            print(f"Error installing update: {e}")
            return False

    def log_update(self, update_info: Dict, action: str):
        """Log update action"""
        self.update_log.append({
            'timestamp': datetime.now().isoformat(),
            'version': update_info.get('latest_version'),
            'action': action
        })


class ReleaseNotesManager:
    """Manage release notes"""

    def __init__(self):
        self.releases = []

    def add_release(self, version: str, date: str, changes: List[str],
                   breaking_changes: List[str] = None):
        """Add a release"""
        self.releases.append({
            'version': version,
            'date': date,
            'changes': changes,
            'breaking_changes': breaking_changes or []
        })

    def get_release_notes(self, version: str) -> Optional[Dict]:
        """Get release notes for specific version"""
        for release in self.releases:
            if release['version'] == version:
                return release
        return None

    def get_all_releases(self) -> List[Dict]:
        """Get all releases"""
        return sorted(self.releases, key=lambda r: r['date'], reverse=True)

    def generate_changelog_text(self) -> str:
        """Generate full changelog"""
        lines = []
        lines.append("# DarkDork Changelog\n")

        for release in self.get_all_releases():
            lines.append(f"## Version {release['version']} - {release['date']}\n")

            if release.get('breaking_changes'):
                lines.append("### Breaking Changes")
                for change in release['breaking_changes']:
                    lines.append(f"- ⚠️ {change}")
                lines.append("")

            lines.append("### Changes")
            for change in release['changes']:
                lines.append(f"- {change}")

            lines.append("\n")

        return '\n'.join(lines)


# Example usage
def example_updater():
    """Example update system usage"""

    print("DarkDork Update System")
    print("="*50)

    # Initialize updater
    updater = AutoUpdater('1.0.0')

    # Check for updates
    print("\n1. Checking for updates...")
    has_update, notification = updater.check_and_notify()

    if has_update:
        print("\n" + notification)
    else:
        print("   No updates available")

    # Simulate update check
    print("\n2. Getting update info...")
    update_info = updater.checker.check_for_updates()

    if update_info and update_info.get('update_available'):
        print(f"   Update available: v{update_info['latest_version']}")
        print(f"   Current version: v{update_info['current_version']}")
        print("\n   Changelog:")
        for change in update_info.get('changelog', []):
            print(f"     • {change}")

    # Release notes
    print("\n3. Managing release notes...")
    notes_manager = ReleaseNotesManager()

    notes_manager.add_release(
        '1.0.0',
        '2026-01-09',
        [
            'Initial release',
            '10 pre-built dork categories',
            'Export to multiple formats'
        ]
    )

    notes_manager.add_release(
        '1.1.0',
        '2026-01-15',
        [
            'Added 5 new dork categories',
            'Improved search performance',
            'New PDF export functionality'
        ]
    )

    print("   Release notes available for:")
    for release in notes_manager.get_all_releases():
        print(f"     - v{release['version']} ({release['date']})")

    print("\n✓ Update system example complete!")


if __name__ == '__main__':
    example_updater()
