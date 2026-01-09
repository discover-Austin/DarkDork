#!/usr/bin/env python3
"""
DarkDork API Integrations
Integration with external security tools and APIs
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class IntegrationConfig:
    """Manage API keys and configuration for integrations"""

    def __init__(self, config_file: str = "integrations_config.json"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> Dict:
        """Load integration configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_config(self):
        """Save integration configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def set_api_key(self, service: str, api_key: str):
        """Set API key for a service"""
        if 'api_keys' not in self.config:
            self.config['api_keys'] = {}
        self.config['api_keys'][service] = api_key
        self.save_config()

    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a service"""
        return self.config.get('api_keys', {}).get(service)

    def is_configured(self, service: str) -> bool:
        """Check if service is configured"""
        return bool(self.get_api_key(service))


class ShodanIntegration:
    """Integration with Shodan API"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://api.shodan.io"

    def search(self, query: str) -> Dict:
        """
        Search Shodan for hosts
        Note: Requires 'shodan' package: pip install shodan
        """
        try:
            import shodan
            api = shodan.Shodan(self.api_key)
            results = api.search(query)
            return {
                'total': results['total'],
                'matches': results['matches']
            }
        except ImportError:
            return {'error': 'shodan package not installed'}
        except Exception as e:
            return {'error': str(e)}

    def host_info(self, ip: str) -> Dict:
        """Get information about a specific host"""
        try:
            import shodan
            api = shodan.Shodan(self.api_key)
            host = api.host(ip)
            return host
        except ImportError:
            return {'error': 'shodan package not installed'}
        except Exception as e:
            return {'error': str(e)}

    def generate_dorks_from_shodan(self, shodan_query: str) -> List[str]:
        """Generate Google dorks based on Shodan findings"""
        dorks = []

        # Map Shodan filters to Google dorks
        if 'port:' in shodan_query:
            port = shodan_query.split('port:')[1].split()[0]
            dorks.append(f'inurl:{port}')

        if 'product:' in shodan_query:
            product = shodan_query.split('product:')[1].split()[0]
            dorks.append(f'intitle:"{product}"')

        return dorks


class VirusTotalIntegration:
    """Integration with VirusTotal API"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://www.virustotal.com/api/v3"

    def check_url(self, url: str) -> Dict:
        """
        Check URL reputation on VirusTotal
        Note: Requires 'requests' package
        """
        try:
            import requests
            import base64

            url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
            headers = {'x-apikey': self.api_key}

            response = requests.get(
                f"{self.base_url}/urls/{url_id}",
                headers=headers
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f'API returned {response.status_code}'}

        except ImportError:
            return {'error': 'requests package not installed'}
        except Exception as e:
            return {'error': str(e)}

    def check_domain(self, domain: str) -> Dict:
        """Check domain reputation"""
        try:
            import requests

            headers = {'x-apikey': self.api_key}
            response = requests.get(
                f"{self.base_url}/domains/{domain}",
                headers=headers
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f'API returned {response.status_code}'}

        except ImportError:
            return {'error': 'requests package not installed'}
        except Exception as e:
            return {'error': str(e)}


class BurpSuiteIntegration:
    """Integration with Burp Suite"""

    def __init__(self, burp_host: str = "localhost", burp_port: int = 8080):
        self.burp_host = burp_host
        self.burp_port = burp_port
        self.burp_url = f"http://{burp_host}:{burp_port}"

    def send_to_burp(self, url: str, method: str = "GET") -> bool:
        """
        Send discovered URL to Burp Suite for scanning
        Note: Requires Burp Suite REST API extension
        """
        try:
            import requests

            data = {
                'url': url,
                'method': method
            }

            response = requests.post(
                f"{self.burp_url}/v1/scan",
                json=data
            )

            return response.status_code == 200

        except ImportError:
            print("requests package not installed")
            return False
        except Exception as e:
            print(f"Error sending to Burp: {e}")
            return False

    def export_burp_results(self, output_file: str) -> bool:
        """Export Burp Suite scan results"""
        try:
            import requests

            response = requests.get(f"{self.burp_url}/v1/scan/results")

            if response.status_code == 200:
                with open(output_file, 'w') as f:
                    json.dump(response.json(), f, indent=2)
                return True

            return False

        except Exception as e:
            print(f"Error exporting Burp results: {e}")
            return False


class OWASPZAPIntegration:
    """Integration with OWASP ZAP"""

    def __init__(self, zap_host: str = "localhost", zap_port: int = 8080,
                 api_key: str = None):
        self.zap_host = zap_host
        self.zap_port = zap_port
        self.api_key = api_key
        self.zap_url = f"http://{zap_host}:{zap_port}"

    def spider_url(self, url: str) -> Dict:
        """Spider a discovered URL with ZAP"""
        try:
            from zapv2 import ZAPv2

            zap = ZAPv2(apikey=self.api_key,
                       proxies={'http': self.zap_url,
                               'https': self.zap_url})

            scan_id = zap.spider.scan(url)

            return {
                'scan_id': scan_id,
                'status': 'started',
                'url': url
            }

        except ImportError:
            return {'error': 'python-owasp-zap-v2.4 package not installed'}
        except Exception as e:
            return {'error': str(e)}

    def active_scan(self, url: str) -> Dict:
        """Run active scan on URL"""
        try:
            from zapv2 import ZAPv2

            zap = ZAPv2(apikey=self.api_key,
                       proxies={'http': self.zap_url,
                               'https': self.zap_url})

            scan_id = zap.ascan.scan(url)

            return {
                'scan_id': scan_id,
                'status': 'started',
                'url': url
            }

        except ImportError:
            return {'error': 'python-owasp-zap-v2.4 package not installed'}
        except Exception as e:
            return {'error': str(e)}


class NmapIntegration:
    """Integration with Nmap"""

    def __init__(self):
        self.nmap_path = self._find_nmap()

    def _find_nmap(self) -> Optional[str]:
        """Find nmap executable"""
        import shutil
        return shutil.which('nmap')

    def scan_host(self, host: str, ports: str = "1-1000") -> Dict:
        """
        Scan host with Nmap
        Note: Requires nmap installed and python-nmap package
        """
        try:
            import nmap

            nm = nmap.PortScanner()
            nm.scan(host, ports)

            return {
                'host': host,
                'scan_info': nm.scaninfo(),
                'results': nm[host] if host in nm.all_hosts() else {}
            }

        except ImportError:
            return {'error': 'python-nmap package not installed'}
        except Exception as e:
            return {'error': str(e)}


class MetasploitIntegration:
    """Integration with Metasploit"""

    def __init__(self, msf_host: str = "localhost", msf_port: int = 55553,
                 username: str = "msf", password: str = "password"):
        self.msf_host = msf_host
        self.msf_port = msf_port
        self.username = username
        self.password = password

    def search_exploits(self, query: str) -> List[Dict]:
        """
        Search for exploits in Metasploit
        Note: Requires pymetasploit3 package
        """
        try:
            from pymetasploit3.msfrpc import MsfRpcClient

            client = MsfRpcClient(
                self.password,
                server=self.msf_host,
                port=self.msf_port,
                username=self.username
            )

            modules = client.modules.exploits
            results = [m for m in modules if query.lower() in m.lower()]

            return results

        except ImportError:
            return [{'error': 'pymetasploit3 package not installed'}]
        except Exception as e:
            return [{'error': str(e)}]


class SlackIntegration:
    """Integration with Slack for notifications"""

    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url

    def send_notification(self, message: str, title: str = "DarkDork Alert",
                         severity: str = "info") -> bool:
        """Send notification to Slack"""
        try:
            import requests

            color_map = {
                'critical': '#ff0000',
                'high': '#ff6600',
                'medium': '#ffcc00',
                'low': '#00ff00',
                'info': '#0066ff'
            }

            payload = {
                'text': title,
                'attachments': [{
                    'color': color_map.get(severity.lower(), '#0066ff'),
                    'text': message,
                    'footer': 'DarkDork',
                    'ts': int(datetime.now().timestamp())
                }]
            }

            response = requests.post(self.webhook_url, json=payload)
            return response.status_code == 200

        except ImportError:
            print("requests package not installed")
            return False
        except Exception as e:
            print(f"Error sending Slack notification: {e}")
            return False


class DiscordIntegration:
    """Integration with Discord for notifications"""

    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url

    def send_notification(self, message: str, title: str = "DarkDork Alert",
                         severity: str = "info") -> bool:
        """Send notification to Discord"""
        try:
            import requests

            color_map = {
                'critical': 16711680,  # Red
                'high': 16737792,       # Orange
                'medium': 16776960,     # Yellow
                'low': 65280,           # Green
                'info': 26367           # Blue
            }

            payload = {
                'embeds': [{
                    'title': title,
                    'description': message,
                    'color': color_map.get(severity.lower(), 26367),
                    'footer': {'text': 'DarkDork'},
                    'timestamp': datetime.now().isoformat()
                }]
            }

            response = requests.post(self.webhook_url, json=payload)
            return response.status_code in [200, 204]

        except ImportError:
            print("requests package not installed")
            return False
        except Exception as e:
            print(f"Error sending Discord notification: {e}")
            return False


class IntegrationManager:
    """Manage all integrations"""

    def __init__(self):
        self.config = IntegrationConfig()
        self.integrations = {}

    def setup_shodan(self, api_key: str):
        """Setup Shodan integration"""
        self.config.set_api_key('shodan', api_key)
        self.integrations['shodan'] = ShodanIntegration(api_key)

    def setup_virustotal(self, api_key: str):
        """Setup VirusTotal integration"""
        self.config.set_api_key('virustotal', api_key)
        self.integrations['virustotal'] = VirusTotalIntegration(api_key)

    def setup_burp(self, host: str = "localhost", port: int = 8080):
        """Setup Burp Suite integration"""
        self.integrations['burp'] = BurpSuiteIntegration(host, port)

    def setup_zap(self, host: str = "localhost", port: int = 8080,
                  api_key: str = None):
        """Setup OWASP ZAP integration"""
        self.integrations['zap'] = OWASPZAPIntegration(host, port, api_key)

    def setup_slack(self, webhook_url: str):
        """Setup Slack integration"""
        self.config.set_api_key('slack_webhook', webhook_url)
        self.integrations['slack'] = SlackIntegration(webhook_url)

    def setup_discord(self, webhook_url: str):
        """Setup Discord integration"""
        self.config.set_api_key('discord_webhook', webhook_url)
        self.integrations['discord'] = DiscordIntegration(webhook_url)

    def get_integration(self, name: str):
        """Get integration by name"""
        return self.integrations.get(name)

    def list_integrations(self) -> List[str]:
        """List configured integrations"""
        return list(self.integrations.keys())

    def notify_finding(self, title: str, message: str, severity: str = "info"):
        """Send notification about a finding to all configured channels"""
        results = {}

        if 'slack' in self.integrations:
            results['slack'] = self.integrations['slack'].send_notification(
                message, title, severity
            )

        if 'discord' in self.integrations:
            results['discord'] = self.integrations['discord'].send_notification(
                message, title, severity
            )

        return results


# Example usage
def example_usage():
    """Example integration usage"""

    # Initialize integration manager
    manager = IntegrationManager()

    # Setup integrations
    manager.setup_slack("https://hooks.slack.com/services/YOUR/WEBHOOK/URL")
    manager.setup_discord("https://discord.com/api/webhooks/YOUR/WEBHOOK/URL")

    # Send notification about finding
    manager.notify_finding(
        "Critical Finding Discovered",
        "Found exposed database file at example.com/db.sql",
        "critical"
    )

    # Use Shodan integration
    if manager.config.is_configured('shodan'):
        shodan = manager.get_integration('shodan')
        results = shodan.search('apache')
        print(f"Shodan results: {results.get('total', 0)} hosts found")


if __name__ == '__main__':
    print("DarkDork Integrations System")
    print("="*50)
    print("\nAvailable Integrations:")
    print("  - Shodan API")
    print("  - VirusTotal API")
    print("  - Burp Suite")
    print("  - OWASP ZAP")
    print("  - Nmap")
    print("  - Metasploit")
    print("  - Slack")
    print("  - Discord")
    print("\nSee example_usage() for usage examples")
