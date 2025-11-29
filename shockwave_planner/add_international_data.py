#!/usr/bin/env python3
"""Add sample launches from USA and Russia"""
import sqlite3

def add_international_sample_data():
    conn = sqlite3.connect('shockwave_planner.db')
    cursor = conn.cursor()
    
    # Add USA launch sites
    usa_sites = [
        ('Cape Canaveral', 'LC-39A', 28.6083, -80.6041, 'Florida, USA - SpaceX'),
        ('Cape Canaveral', 'SLC-40', 28.5618, -80.5771, 'Florida, USA - SpaceX'),
        ('Vandenberg', 'SLC-4E', 34.6332, -120.6156, 'California, USA - SpaceX'),
        ('Kennedy', 'LC-39B', 28.6273, -80.6209, 'Florida, USA - NASA/ULA'),
    ]
    
    print("Adding USA launch sites...")
    for location, pad, lat, lon, notes in usa_sites:
        cursor.execute("""
            INSERT OR IGNORE INTO launch_sites (location, launch_pad, latitude, longitude, active, notes)
            VALUES (?, ?, ?, ?, 1, ?)
        """, (location, pad, lat, lon, notes))
    
    # Add Russia launch sites
    russia_sites = [
        ('Baikonur', 'Site 1/5', 45.9200, 63.3421, 'Kazakhstan - Soyuz'),
        ('Baikonur', 'Site 31/6', 45.9960, 63.5649, 'Kazakhstan - Soyuz'),
        ('Plesetsk', 'Site 43/4', 62.9275, 40.5772, 'Russia - Soyuz'),
        ('Vostochny', 'Site 1S', 51.8844, 128.3347, 'Russia - Soyuz/Angara'),
    ]
    
    print("Adding Russia launch sites...")
    for location, pad, lat, lon, notes in russia_sites:
        cursor.execute("""
            INSERT OR IGNORE INTO launch_sites (location, launch_pad, latitude, longitude, active, notes)
            VALUES (?, ?, ?, ?, 1, ?)
        """, (location, pad, lat, lon, notes))
    
    # Add USA rockets
    usa_rockets = [
        ('Falcon 9 Block 5', 'Falcon', 2, 22800, 8300, 70.0, 3.7, 549000, 'SpaceX reusable'),
        ('Falcon Heavy', 'Falcon', 2, 63800, 26700, 70.0, 12.2, 1420000, 'SpaceX heavy-lift'),
        ('Atlas V 541', 'Atlas', 2, 18850, 8900, 62.2, 3.8, 334500, 'ULA'),
        ('Vulcan Centaur', 'Vulcan', 2, 27200, 15000, 61.6, 5.4, 546000, 'ULA next-gen'),
    ]
    
    print("Adding USA rockets...")
    for name, family, stages, leo, gto, height, diam, mass, notes in usa_rockets:
        cursor.execute("""
            INSERT OR IGNORE INTO rockets (name, family, stages, payload_capacity_leo, 
                                          payload_capacity_gto, height, diameter, mass, active, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
        """, (name, family, stages, leo, gto, height, diam, mass, notes))
    
    # Add Russia rockets
    russia_rockets = [
        ('Soyuz-2.1a', 'Soyuz', 3, 7020, 2810, 46.3, 2.95, 312000, 'Roscosmos workhorse'),
        ('Soyuz-2.1b', 'Soyuz', 3, 8200, 3250, 46.3, 2.95, 312000, 'Enhanced Soyuz'),
        ('Proton-M', 'Proton', 3, 23000, 6920, 58.2, 7.4, 705000, 'Heavy-lift'),
        ('Angara A5', 'Angara', 3, 24500, 7500, 64.0, 2.9, 773000, 'Modern heavy-lift'),
    ]
    
    print("Adding Russia rockets...")
    for name, family, stages, leo, gto, height, diam, mass, notes in russia_rockets:
        cursor.execute("""
            INSERT OR IGNORE INTO rockets (name, family, stages, payload_capacity_leo,
                                          payload_capacity_gto, height, diameter, mass, active, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
        """, (name, family, stages, leo, gto, height, diam, mass, notes))
    
    conn.commit()
    
    # Helper functions
    def get_site_id(location, pad):
        cursor.execute("SELECT site_id FROM launch_sites WHERE location=? AND launch_pad=?", (location, pad))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def get_rocket_id(name):
        cursor.execute("SELECT rocket_id FROM rockets WHERE name=?", (name,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def get_status_id(name):
        cursor.execute("SELECT status_id FROM launch_status WHERE status_name=?", (name,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    # USA sample launches
    usa_launches = [
        ('2025-11-30', '03:15:00', 'Cape Canaveral', 'LC-39A', 'Falcon 9 Block 5',
         'Starlink Group 6-72', '23 Starlink satellites', 'LEO', 'Success', 'A2156/25',
         'Successful landing on ASDS drone ship'),
        ('2025-12-03', '22:45:00', 'Vandenberg', 'SLC-4E', 'Falcon 9 Block 5',
         'NROL-126', 'Classified NRO payload', 'SSO', 'Scheduled', 'A2187/25',
         'National Reconnaissance Office mission'),
        ('2025-12-08', '10:30:00', 'Cape Canaveral', 'SLC-40', 'Falcon 9 Block 5',
         'GPS III SV09', 'GPS III navigation satellite', 'MEO', 'Go', 'A2201/25',
         'US Space Force GPS constellation'),
        ('2025-12-15', '16:20:00', 'Kennedy', 'LC-39B', 'Vulcan Centaur',
         'Dream Chaser EAC-1', 'Dream Chaser cargo spacecraft', 'LEO', 'NET', 'A2234/25',
         'First Dream Chaser ISS cargo mission'),
        ('2025-12-20', '14:00:00', 'Cape Canaveral', 'LC-39A', 'Falcon Heavy',
         'Europa Clipper Deployment', 'Europa science probe', 'Other', 'Scheduled', 'A2267/25',
         'Jupiter system exploration'),
    ]
    
    print("\nAdding USA sample launches...")
    for launch_data in usa_launches:
        date, time, loc, pad, rocket, mission, payload, orbit, status, notam, remarks = launch_data
        site_id = get_site_id(loc, pad)
        rocket_id = get_rocket_id(rocket)
        status_id = get_status_id(status)
        
        if site_id and rocket_id and status_id:
            cursor.execute("""
                INSERT INTO launches (launch_date, launch_time, site_id, rocket_id,
                                     mission_name, payload_name, orbit_type, status_id,
                                     notam_reference, remarks, data_source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Manual')
            """, (date, time, site_id, rocket_id, mission, payload, orbit, status_id, notam, remarks))
            print(f"  ✓ Added: {mission} - {date}")
    
    # Russia sample launches
    russia_launches = [
        ('2025-11-29', '08:45:00', 'Baikonur', 'Site 31/6', 'Soyuz-2.1a',
         'Progress MS-29', 'ISS cargo resupply', 'LEO', 'Success', 'R1145/25',
         'Successful ISS docking'),
        ('2025-12-05', '12:30:00', 'Plesetsk', 'Site 43/4', 'Soyuz-2.1b',
         'Meteor-M N2-4', 'Weather satellite', 'SSO', 'Scheduled', 'R1178/25',
         'Polar meteorological satellite'),
        ('2025-12-10', '21:15:00', 'Baikonur', 'Site 1/5', 'Proton-M',
         'Yamal-601', 'Communications satellite', 'GTO', 'Go', 'R1203/25',
         'Gazprom Space Systems comsat'),
        ('2025-12-18', '05:00:00', 'Vostochny', 'Site 1S', 'Angara A5',
         'Arktika-M N3', 'Arctic monitoring satellite', 'HEO', 'Scheduled', 'R1256/25',
         'Highly elliptical orbit for Arctic coverage'),
    ]
    
    print("\nAdding Russia sample launches...")
    for launch_data in russia_launches:
        date, time, loc, pad, rocket, mission, payload, orbit, status, notam, remarks = launch_data
        site_id = get_site_id(loc, pad)
        rocket_id = get_rocket_id(rocket)
        status_id = get_status_id(status)
        
        if site_id and rocket_id and status_id:
            cursor.execute("""
                INSERT INTO launches (launch_date, launch_time, site_id, rocket_id,
                                     mission_name, payload_name, orbit_type, status_id,
                                     notam_reference, remarks, data_source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Manual')
            """, (date, time, site_id, rocket_id, mission, payload, orbit, status_id, notam, remarks))
            print(f"  ✓ Added: {mission} - {date}")
    
    conn.commit()
    conn.close()
    
    # Print summary
    print("\n" + "="*50)
    print("INTERNATIONAL SAMPLE DATA ADDED!")
    print("="*50)
    
    conn = sqlite3.connect('shockwave_planner.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM launch_sites")
    sites_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM rockets")
    rockets_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM launches")
    launches_count = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT location, COUNT(*) 
        FROM launches l
        JOIN launch_sites s ON l.site_id = s.site_id
        GROUP BY location
        ORDER BY COUNT(*) DESC
    """)
    by_location = cursor.fetchall()
    
    print(f"\nDatabase Statistics:")
    print(f"  Launch Sites: {sites_count}")
    print(f"  Rockets: {rockets_count}")
    print(f"  Total Launches: {launches_count}")
    print(f"\nLaunches by Location:")
    for loc, count in by_location:
        print(f"  {loc}: {count}")
    
    conn.close()
    
    print("\n✅ Ready to view in Timeline!")
    print("   - Expand ▶ USA to see Falcon 9, Falcon Heavy, etc.")
    print("   - Expand ▶ Russia to see Soyuz, Proton, Angara")
    print("   - Expand ▶ China to see Long March family")
    print("\n🚀 Run: python3 main.py")

if __name__ == '__main__':
    add_international_sample_data()
