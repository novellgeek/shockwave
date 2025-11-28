#!/usr/bin/env python3
"""
Populate sample launch data for SHOCKWAVE PLANNER
"""
import sys
sys.path.insert(0, '/home/claude/shockwave_planner')

from data.database import LaunchDatabase
from datetime import datetime, timedelta
import random

db = LaunchDatabase('/home/claude/shockwave_planner/shockwave_planner.db')

# Get references
sites = db.get_all_sites()
rockets = db.get_all_rockets()
statuses = db.get_all_statuses()

# Sample launch data for November 2025
sample_launches = [
    {
        'launch_date': '2025-11-05',
        'launch_time': '03:12:00',
        'site': ('Jiuquan', 'LS-130'),
        'rocket': 'Kinetica-1',
        'mission_name': 'Tianqi-27',
        'payload_name': 'Tianqi-27',
        'orbit_type': 'LEO',
        'status': 'Success',
        'remarks': 'IoT constellation satellite'
    },
    {
        'launch_date': '2025-11-13',
        'launch_time': '06:50:00',
        'site': ('Taiyuan', 'LA-9A'),
        'rocket': 'Long March 6C',
        'mission_name': 'Gaofen-12E',
        'payload_name': 'Gaofen-12E',
        'orbit_type': 'SSO',
        'status': 'Success',
        'remarks': 'High-resolution Earth observation'
    },
    {
        'launch_date': '2025-11-22',
        'launch_time': '14:30:00',
        'site': ('Jiuquan', 'SLS-2'),
        'rocket': 'Long March 2C',
        'mission_name': 'Tianhui-6B',
        'payload_name': 'Tianhui-6B',
        'orbit_type': 'SSO',
        'status': 'Scheduled',
        'remarks': 'Stereo mapping satellite'
    },
    {
        'launch_date': '2025-11-26',
        'launch_time': '09:00:00',
        'site': ('Xichang', 'LA-2'),
        'rocket': 'Long March 3B/E',
        'mission_name': 'Beidou-3 M26',
        'payload_name': 'Beidou-3 M26',
        'orbit_type': 'MEO',
        'status': 'Go',
        'remarks': 'Navigation satellite backup'
    },
    {
        'launch_date': '2025-11-28',
        'launch_time': '01:45:00',
        'site': ('Jiuquan', 'LS-95'),
        'rocket': 'Ceres-1',
        'mission_name': 'Jilin-1 GF06',
        'payload_name': 'Jilin-1 GF06A/B/C',
        'orbit_type': 'SSO',
        'status': 'NET',
        'remarks': 'Rideshare mission - 3 satellites'
    },
]

# Add December launches
december_launches = [
    {
        'launch_date': '2025-12-05',
        'launch_time': '11:20:00',
        'site': ('Wenchang', 'LC-101'),
        'rocket': 'Long March 7',
        'mission_name': 'Tianzhou-9',
        'payload_name': 'Tianzhou-9 cargo spacecraft',
        'orbit_type': 'LEO',
        'status': 'Scheduled',
        'remarks': 'ISS resupply mission'
    },
    {
        'launch_date': '2025-12-12',
        'launch_time': '04:30:00',
        'site': ('Taiyuan', 'LA-9'),
        'rocket': 'Long March 4C',
        'mission_name': 'Yaogan-41',
        'payload_name': 'Yaogan-41',
        'orbit_type': 'SSO',
        'status': 'Scheduled',
        'remarks': 'Remote sensing satellite'
    },
    {
        'launch_date': '2025-12-18',
        'launch_time': '15:00:00',
        'site': ('Jiuquan', 'SLS-1'),
        'rocket': 'Long March 2F/G',
        'mission_name': 'Shenzhou-20',
        'payload_name': 'Shenzhou-20 spacecraft',
        'orbit_type': 'LEO',
        'status': 'NET',
        'remarks': 'Crewed mission to Tiangong'
    },
]

# Combine all launches
all_launches = sample_launches + december_launches

print("Populating SHOCKWAVE PLANNER database with sample launches...")
print("=" * 60)

for launch_data in all_launches:
    # Find site_id
    site_location, site_pad = launch_data['site']
    site = next((s for s in sites if s['location'] == site_location and s['launch_pad'] == site_pad), None)
    
    # Find rocket_id
    rocket = next((r for r in rockets if r['name'] == launch_data['rocket']), None)
    
    # Find status_id
    status = next((st for st in statuses if st['status_name'] == launch_data['status']), None)
    
    if site and rocket and status:
        db_launch_data = {
            'launch_date': launch_data['launch_date'],
            'launch_time': launch_data['launch_time'],
            'site_id': site['site_id'],
            'rocket_id': rocket['rocket_id'],
            'mission_name': launch_data['mission_name'],
            'payload_name': launch_data['payload_name'],
            'orbit_type': launch_data['orbit_type'],
            'status_id': status['status_id'],
            'remarks': launch_data['remarks']
        }
        
        launch_id = db.add_launch(db_launch_data)
        print(f"✓ Added: {launch_data['launch_date']} - {launch_data['mission_name']} ({launch_data['rocket']})")
    else:
        print(f"✗ Skipped: {launch_data['mission_name']} (missing references)")

print("=" * 60)
print(f"Database populated successfully!")
print(f"Total launches added: {len(all_launches)}")

# Show statistics
stats = db.get_statistics()
print(f"\nDatabase Statistics:")
print(f"  Total launches: {stats['total_launches']}")
print(f"  Successful: {stats['successful']}")
print(f"  Pending: {stats['pending']}")

db.close()
