#!/usr/bin/env python3
"""
Nextcloud Apps Audit Script
Queries Nextcloud OCS API to inventory installed apps and their security status.

Usage:
    python nextcloud_apps_audit.py --url http://10.0.0.47:8080 --username admin --password <pass>
    python nextcloud_apps_audit.py --url http://10.0.0.47:8080 --env-file ../infra/docker/.env
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv


class NextcloudClient:
    """Client for interacting with Nextcloud OCS API."""

    def __init__(self, base_url, username, password):
        """
        Initialize Nextcloud API client.

        Args:
            base_url (str): Nextcloud base URL (e.g., http://10.0.0.47:8080)
            username (str): Admin username
            password (str): Admin password
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, password)
        self.session.headers.update({
            'OCS-APIRequest': 'true',
            'Accept': 'application/json'
        })

    def get_apps(self, app_filter='enabled'):
        """
        Fetch apps from Nextcloud.

        Args:
            app_filter (str): Filter for apps - 'enabled', 'disabled', or 'all'

        Returns:
            list: List of app IDs
        """
        url = f"{self.base_url}/ocs/v2.php/cloud/apps"
        params = {'format': 'json'}

        if app_filter != 'all':
            params['filter'] = app_filter

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # OCS API wraps response in ocs.data
            if 'ocs' in data and 'data' in data['ocs']:
                apps = data['ocs']['data'].get('apps', [])
                return apps if isinstance(apps, list) else []

            return []

        except requests.exceptions.RequestException as e:
            print(f"Error fetching apps (filter={app_filter}): {e}", file=sys.stderr)
            return []

    def get_app_info(self, app_id):
        """
        Get detailed information about a specific app.

        Args:
            app_id (str): App identifier

        Returns:
            dict: App information
        """
        url = f"{self.base_url}/ocs/v2.php/cloud/apps/{app_id}"
        params = {'format': 'json'}

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # OCS API wraps response in ocs.data
            if 'ocs' in data and 'data' in data['ocs']:
                return data['ocs']['data']

            return {}

        except requests.exceptions.RequestException as e:
            print(f"Error fetching app info for {app_id}: {e}", file=sys.stderr)
            return {}


def load_config(args):
    """
    Load configuration from CLI arguments or .env file.

    Args:
        args: Parsed command-line arguments

    Returns:
        dict: Configuration dictionary with url, username, password
    """
    config = {'url': args.url}

    if args.env_file:
        # Load from .env file
        if not os.path.exists(args.env_file):
            print(f"Error: .env file not found: {args.env_file}", file=sys.stderr)
            sys.exit(1)

        load_dotenv(args.env_file)
        config['username'] = os.getenv('NEXTCLOUD_ADMIN_USER')
        config['password'] = os.getenv('NEXTCLOUD_ADMIN_PASSWORD')

        if not config['username'] or not config['password']:
            print("Error: NEXTCLOUD_ADMIN_USER and NEXTCLOUD_ADMIN_PASSWORD must be set in .env file", file=sys.stderr)
            sys.exit(1)

        if args.verbose:
            print(f"Loaded credentials from {args.env_file}")

    elif args.credentials:
        # Use command-line credentials
        config['username'] = args.credentials[0]
        config['password'] = args.credentials[1]

        if args.verbose:
            print("Using credentials from command-line arguments")

    return config


def save_csv(apps_data, output_path):
    """
    Save apps inventory to CSV file.

    Args:
        apps_data (list): List of app dictionaries
        output_path (Path): Output file path
    """
    if not apps_data:
        print("Warning: No app data to save to CSV", file=sys.stderr)
        return

    fieldnames = ['app_id', 'name', 'version', 'enabled', 'category', 'description', 'author']

    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()

            for app in apps_data:
                writer.writerow(app)

        print(f"✓ CSV saved: {output_path}")

    except IOError as e:
        print(f"Error saving CSV: {e}", file=sys.stderr)


def save_json(apps_data, output_path):
    """
    Save apps inventory to JSON file.

    Args:
        apps_data (list): List of app dictionaries
        output_path (Path): Output file path
    """
    output_data = {
        'scan_timestamp': datetime.now().isoformat(),
        'total_apps': len(apps_data),
        'enabled_count': sum(1 for app in apps_data if app.get('enabled')),
        'disabled_count': sum(1 for app in apps_data if not app.get('enabled')),
        'apps': apps_data
    }

    try:
        with open(output_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(output_data, jsonfile, indent=2, ensure_ascii=False)

        print(f"✓ JSON saved: {output_path}")

    except IOError as e:
        print(f"Error saving JSON: {e}", file=sys.stderr)


def generate_summary(apps_data, output_path):
    """
    Generate human-readable summary report.

    Args:
        apps_data (list): List of app dictionaries
        output_path (Path): Output file path
    """
    enabled_apps = [app for app in apps_data if app.get('enabled')]
    disabled_apps = [app for app in apps_data if not app.get('enabled')]

    summary_lines = []
    summary_lines.append("=" * 70)
    summary_lines.append("Nextcloud Apps Audit Summary")
    summary_lines.append("=" * 70)
    summary_lines.append(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary_lines.append(f"Total Apps: {len(apps_data)}")
    summary_lines.append(f"Enabled Apps: {len(enabled_apps)}")
    summary_lines.append(f"Disabled Apps: {len(disabled_apps)}")
    summary_lines.append("")

    summary_lines.append("-" * 70)
    summary_lines.append("ENABLED APPS")
    summary_lines.append("-" * 70)
    for app in enabled_apps:
        summary_lines.append(f"  • {app.get('name', 'Unknown')} (v{app.get('version', 'N/A')})")
        if app.get('description'):
            summary_lines.append(f"    {app.get('description')[:100]}")
        summary_lines.append("")

    if disabled_apps:
        summary_lines.append("-" * 70)
        summary_lines.append("DISABLED APPS")
        summary_lines.append("-" * 70)
        for app in disabled_apps:
            summary_lines.append(f"  • {app.get('name', 'Unknown')} (v{app.get('version', 'N/A')})")
            summary_lines.append("")

    summary_lines.append("=" * 70)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(summary_lines))

        print(f"✓ Summary saved: {output_path}")

    except IOError as e:
        print(f"Error saving summary: {e}", file=sys.stderr)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Audit Nextcloud installed apps for security assessment',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Connection options
    parser.add_argument(
        '--url',
        required=True,
        help='Nextcloud base URL (e.g., http://10.0.0.47:8080)'
    )

    # Authentication options
    auth_group = parser.add_mutually_exclusive_group(required=True)
    auth_group.add_argument(
        '--env-file',
        help='Path to .env file containing NEXTCLOUD_ADMIN_USER and NEXTCLOUD_ADMIN_PASSWORD'
    )
    auth_group.add_argument(
        '--credentials',
        nargs=2,
        metavar=('USERNAME', 'PASSWORD'),
        help='Username and password as arguments'
    )

    # Output options
    parser.add_argument(
        '--output',
        '-o',
        default='../docs/evidence/week3/apps-audit/',
        help='Output directory for reports (default: ../docs/evidence/week3/apps-audit/)'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose output'
    )

    return parser.parse_args()


def main():
    """Main execution function."""
    args = parse_arguments()

    print("=" * 70)
    print("Nextcloud Apps Audit")
    print("=" * 70)

    # Load configuration
    if args.verbose:
        print("\n[1/5] Loading configuration...")
    config = load_config(args)

    # Create Nextcloud client
    if args.verbose:
        print(f"[2/5] Connecting to Nextcloud at {config['url']}...")
    client = NextcloudClient(
        base_url=config['url'],
        username=config['username'],
        password=config['password']
    )

    # Fetch apps data
    if args.verbose:
        print("[3/5] Fetching apps inventory...")

    enabled_app_ids = client.get_apps(app_filter='enabled')
    disabled_app_ids = client.get_apps(app_filter='disabled')

    if not enabled_app_ids and not disabled_app_ids:
        print("Error: No apps found. Check your connection and credentials.", file=sys.stderr)
        return 1

    if args.verbose:
        print(f"    Found {len(enabled_app_ids)} enabled apps")
        print(f"    Found {len(disabled_app_ids)} disabled apps")

    # Collect detailed app information
    if args.verbose:
        print("[4/5] Collecting detailed app information...")

    apps_data = []

    for app_id in enabled_app_ids:
        app_info = client.get_app_info(app_id)
        if app_info:
            apps_data.append({
                'app_id': app_info.get('id', app_id),
                'name': app_info.get('name', app_id),
                'version': app_info.get('version', 'N/A'),
                'enabled': True,
                'category': app_info.get('category', 'N/A'),
                'description': app_info.get('description', ''),
                'author': app_info.get('author', 'N/A')
            })

    for app_id in disabled_app_ids:
        app_info = client.get_app_info(app_id)
        if app_info:
            apps_data.append({
                'app_id': app_info.get('id', app_id),
                'name': app_info.get('name', app_id),
                'version': app_info.get('version', 'N/A'),
                'enabled': False,
                'category': app_info.get('category', 'N/A'),
                'description': app_info.get('description', ''),
                'author': app_info.get('author', 'N/A')
            })

    # Prepare output directory
    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate timestamped filenames
    timestamp = datetime.now().strftime('%Y%m%d-%H%M')
    csv_file = output_dir / f"{timestamp}_apps-audit_inventory.csv"
    json_file = output_dir / f"{timestamp}_apps-audit_inventory.json"
    summary_file = output_dir / f"{timestamp}_apps-audit_summary.txt"

    # Generate output files
    if args.verbose:
        print(f"[5/5] Generating reports in {output_dir}...")

    save_csv(apps_data, csv_file)
    save_json(apps_data, json_file)
    generate_summary(apps_data, summary_file)

    # Print summary to console
    print("\n" + "=" * 70)
    print(f"Audit Complete!")
    print("=" * 70)
    print(f"Total Apps:     {len(apps_data)}")
    print(f"Enabled:        {len(enabled_app_ids)}")
    print(f"Disabled:       {len(disabled_app_ids)}")
    print(f"\nReports saved to: {output_dir}")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
