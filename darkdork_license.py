#!/usr/bin/env python3
"""
DarkDork License Management System
For commercial distribution with license validation
"""

import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import uuid


class License:
    """Represents a software license"""

    LICENSE_TYPES = {
        'trial': {
            'duration_days': 14,
            'features': ['basic'],
            'max_searches_per_day': 50
        },
        'individual': {
            'duration_days': 365,
            'features': ['basic', 'export', 'history'],
            'max_searches_per_day': -1  # Unlimited
        },
        'team': {
            'duration_days': 365,
            'features': ['basic', 'export', 'history', 'collaboration', 'api'],
            'max_seats': 5,
            'max_searches_per_day': -1
        },
        'enterprise': {
            'duration_days': 365,
            'features': ['all'],
            'max_seats': -1,  # Unlimited
            'max_searches_per_day': -1,
            'custom_branding': True,
            'priority_support': True
        }
    }

    def __init__(self, license_type: str, customer_name: str,
                 customer_email: str, issued_date: datetime = None,
                 license_key: str = None):
        self.license_type = license_type
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.issued_date = issued_date or datetime.now()
        self.license_key = license_key or self._generate_license_key()
        self.machine_id = self._get_machine_id()

    def _generate_license_key(self) -> str:
        """Generate a unique license key"""
        data = f"{self.customer_email}{self.issued_date.isoformat()}{uuid.uuid4()}"
        hash_value = hashlib.sha256(data.encode()).hexdigest()[:32].upper()

        # Format as XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX
        return '-'.join([hash_value[i:i+4] for i in range(0, 32, 4)])

    def _get_machine_id(self) -> str:
        """Get unique machine identifier"""
        try:
            if os.name == 'nt':  # Windows
                import subprocess
                output = subprocess.check_output('wmic csproduct get uuid').decode()
                machine_id = output.split('\n')[1].strip()
            else:  # Linux/Mac
                import subprocess
                try:
                    machine_id = subprocess.check_output(['cat', '/etc/machine-id']).decode().strip()
                except:
                    machine_id = subprocess.check_output(['cat', '/var/lib/dbus/machine-id']).decode().strip()

            return hashlib.sha256(machine_id.encode()).hexdigest()[:16].upper()

        except:
            # Fallback to a generated ID
            return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:16].upper()

    def get_expiration_date(self) -> datetime:
        """Get license expiration date"""
        license_info = self.LICENSE_TYPES[self.license_type]
        duration_days = license_info['duration_days']
        return self.issued_date + timedelta(days=duration_days)

    def is_valid(self) -> Tuple[bool, str]:
        """Check if license is valid"""
        now = datetime.now()

        # Check if license type exists
        if self.license_type not in self.LICENSE_TYPES:
            return False, "Invalid license type"

        # Check expiration
        expiration = self.get_expiration_date()
        if now > expiration:
            return False, f"License expired on {expiration.strftime('%Y-%m-%d')}"

        # Check license key format
        if len(self.license_key.replace('-', '')) != 32:
            return False, "Invalid license key format"

        return True, "Valid"

    def get_features(self) -> list:
        """Get enabled features for this license"""
        license_info = self.LICENSE_TYPES[self.license_type]
        features = license_info['features']

        if 'all' in features:
            return ['basic', 'export', 'history', 'collaboration', 'api',
                   'automation', 'integrations', 'custom_branding', 'priority_support']

        return features

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'license_key': self.license_key,
            'license_type': self.license_type,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'issued_date': self.issued_date.isoformat(),
            'expiration_date': self.get_expiration_date().isoformat(),
            'machine_id': self.machine_id,
            'features': self.get_features()
        }

    def to_file(self, filename: str = "license.json"):
        """Save license to file"""
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def from_file(cls, filename: str = "license.json") -> Optional['License']:
        """Load license from file"""
        if not os.path.exists(filename):
            return None

        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            license_obj = cls(
                data['license_type'],
                data['customer_name'],
                data['customer_email'],
                datetime.fromisoformat(data['issued_date']),
                data['license_key']
            )

            return license_obj

        except Exception as e:
            print(f"Error loading license: {e}")
            return None


class LicenseValidator:
    """Validate and manage licenses"""

    def __init__(self, license_file: str = "license.json"):
        self.license_file = license_file
        self.license = None
        self.load_license()

    def load_license(self):
        """Load license from file"""
        self.license = License.from_file(self.license_file)

    def is_licensed(self) -> bool:
        """Check if application is licensed"""
        if not self.license:
            return False

        is_valid, _ = self.license.is_valid()
        return is_valid

    def get_license_info(self) -> Dict:
        """Get license information"""
        if not self.license:
            return {
                'licensed': False,
                'type': 'none',
                'message': 'No license found'
            }

        is_valid, message = self.license.is_valid()

        return {
            'licensed': is_valid,
            'type': self.license.license_type,
            'customer': self.license.customer_name,
            'expires': self.license.get_expiration_date().strftime('%Y-%m-%d'),
            'features': self.license.get_features(),
            'message': message
        }

    def has_feature(self, feature: str) -> bool:
        """Check if license has a specific feature"""
        if not self.is_licensed():
            return False

        return feature in self.license.get_features()

    def get_days_remaining(self) -> int:
        """Get days remaining on license"""
        if not self.license:
            return 0

        is_valid, _ = self.license.is_valid()
        if not is_valid:
            return 0

        expiration = self.license.get_expiration_date()
        remaining = (expiration - datetime.now()).days

        return max(0, remaining)

    def activate_license(self, license_key: str, customer_name: str,
                        customer_email: str) -> Tuple[bool, str]:
        """Activate a license key"""
        # In a real implementation, this would contact a license server
        # to validate the key. For now, we'll create a basic validation

        try:
            # Mock validation - in production, verify with license server
            if len(license_key.replace('-', '')) != 32:
                return False, "Invalid license key format"

            # Determine license type from key prefix (mock implementation)
            # In production, this would be determined by the license server
            license_type = 'individual'  # Default

            # Create and save license
            license_obj = License(license_type, customer_name, customer_email)
            license_obj.license_key = license_key
            license_obj.to_file(self.license_file)

            self.license = license_obj

            return True, f"License activated successfully. Type: {license_type}"

        except Exception as e:
            return False, f"Activation failed: {str(e)}"


class UsageTracker:
    """Track usage for license compliance"""

    def __init__(self, usage_file: str = "usage.json"):
        self.usage_file = usage_file
        self.usage_data = self.load_usage()

    def load_usage(self) -> Dict:
        """Load usage data"""
        if os.path.exists(self.usage_file):
            try:
                with open(self.usage_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        return {
            'searches_today': 0,
            'last_reset': datetime.now().strftime('%Y-%m-%d'),
            'total_searches': 0
        }

    def save_usage(self):
        """Save usage data"""
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage_data, f, indent=2)

    def record_search(self):
        """Record a search"""
        today = datetime.now().strftime('%Y-%m-%d')

        # Reset counter if it's a new day
        if self.usage_data['last_reset'] != today:
            self.usage_data['searches_today'] = 0
            self.usage_data['last_reset'] = today

        self.usage_data['searches_today'] += 1
        self.usage_data['total_searches'] = self.usage_data.get('total_searches', 0) + 1

        self.save_usage()

    def can_search(self, license_validator: LicenseValidator) -> Tuple[bool, str]:
        """Check if user can perform another search"""
        if not license_validator.is_licensed():
            return False, "No valid license"

        license_info = license_validator.get_license_info()
        license_type = License.LICENSE_TYPES[license_info['type']]

        max_searches = license_type.get('max_searches_per_day', -1)

        if max_searches == -1:  # Unlimited
            return True, "OK"

        if self.usage_data['searches_today'] >= max_searches:
            return False, f"Daily search limit reached ({max_searches} searches)"

        remaining = max_searches - self.usage_data['searches_today']
        return True, f"{remaining} searches remaining today"


class LicenseGenerator:
    """Generate licenses (for vendors)"""

    def __init__(self, vendor_secret: str):
        self.vendor_secret = vendor_secret

    def generate_license(self, license_type: str, customer_name: str,
                        customer_email: str, duration_days: int = None) -> License:
        """Generate a new license"""
        license_obj = License(license_type, customer_name, customer_email)

        # Optionally override duration
        if duration_days:
            # This would require modifying the License class to support custom durations
            pass

        return license_obj

    def generate_trial_license(self, customer_name: str, customer_email: str) -> License:
        """Generate a trial license"""
        return self.generate_license('trial', customer_name, customer_email)

    def batch_generate_licenses(self, license_type: str,
                                customers: list) -> list:
        """Generate multiple licenses"""
        licenses = []

        for customer in customers:
            license_obj = self.generate_license(
                license_type,
                customer['name'],
                customer['email']
            )
            licenses.append(license_obj)

        return licenses


# Example usage
def example_license_management():
    """Example license management"""

    print("DarkDork License Management System")
    print("="*50)

    # Generate a license (vendor side)
    print("\n1. Generating Enterprise License...")
    generator = LicenseGenerator("vendor_secret_key")
    license_obj = generator.generate_license(
        'enterprise',
        'Acme Security Corp',
        'security@acme.com'
    )
    license_obj.to_file('example_license.json')
    print(f"   License Key: {license_obj.license_key}")
    print(f"   Expires: {license_obj.get_expiration_date().strftime('%Y-%m-%d')}")
    print(f"   Features: {', '.join(license_obj.get_features())}")

    # Validate license (customer side)
    print("\n2. Validating License...")
    validator = LicenseValidator('example_license.json')
    license_info = validator.get_license_info()
    print(f"   Licensed: {license_info['licensed']}")
    print(f"   Type: {license_info['type']}")
    print(f"   Customer: {license_info['customer']}")
    print(f"   Expires: {license_info['expires']}")

    # Check features
    print("\n3. Checking Features...")
    features_to_check = ['export', 'api', 'custom_branding']
    for feature in features_to_check:
        has_feature = validator.has_feature(feature)
        print(f"   {feature}: {'✓ Available' if has_feature else '✗ Not available'}")

    # Track usage
    print("\n4. Tracking Usage...")
    tracker = UsageTracker('example_usage.json')
    tracker.record_search()
    can_search, message = tracker.can_search(validator)
    print(f"   Can search: {can_search}")
    print(f"   Message: {message}")

    print("\n✓ License management example complete!")


if __name__ == '__main__':
    example_license_management()
