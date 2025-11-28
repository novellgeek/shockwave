"""
SHOCKWAVE PLANNER - Database Layer
Handles all database operations for launch tracking
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import json


class LaunchDatabase:
    """Database interface for launch tracking system"""
    
    def __init__(self, db_path: str = "shockwave_planner.db"):
        self.db_path = db_path
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
        # Launch Sites table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS launch_sites (
                site_id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                launch_pad TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                active BOOLEAN DEFAULT 1,
                notes TEXT,
                UNIQUE(location, launch_pad)
            )
        """)
        
        # Rockets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rockets (
                rocket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                family TEXT,
                stages INTEGER,
                payload_capacity_leo REAL,
                payload_capacity_gto REAL,
                height REAL,
                diameter REAL,
                mass REAL,
                active BOOLEAN DEFAULT 1,
                notes TEXT
            )
        """)
        
        # Launch Vehicles (specific configurations)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS launch_vehicles (
                vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                rocket_id INTEGER,
                serial_number TEXT,
                configuration TEXT,
                notes TEXT,
                FOREIGN KEY (rocket_id) REFERENCES rockets(rocket_id)
            )
        """)
        
        # Launch Status types
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS launch_status (
                status_id INTEGER PRIMARY KEY AUTOINCREMENT,
                status_name TEXT NOT NULL UNIQUE,
                color TEXT,
                description TEXT
            )
        """)
        
        # Main Launches table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS launches (
                launch_id INTEGER PRIMARY KEY AUTOINCREMENT,
                launch_date DATE,
                launch_time TIME,
                launch_window_start DATETIME,
                launch_window_end DATETIME,
                site_id INTEGER,
                rocket_id INTEGER,
                vehicle_id INTEGER,
                mission_name TEXT,
                payload_name TEXT,
                payload_mass REAL,
                orbit_type TEXT,
                orbit_altitude REAL,
                inclination REAL,
                status_id INTEGER,
                success BOOLEAN,
                failure_reason TEXT,
                remarks TEXT,
                source_url TEXT,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (site_id) REFERENCES launch_sites(site_id),
                FOREIGN KEY (rocket_id) REFERENCES rockets(rocket_id),
                FOREIGN KEY (vehicle_id) REFERENCES launch_vehicles(vehicle_id),
                FOREIGN KEY (status_id) REFERENCES launch_status(status_id)
            )
        """)
        
        # TLE Data associated with launches
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS launch_tles (
                tle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                launch_id INTEGER,
                norad_id INTEGER,
                satellite_name TEXT,
                epoch DATETIME,
                tle_line1 TEXT,
                tle_line2 TEXT,
                source TEXT,
                retrieved_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (launch_id) REFERENCES launches(launch_id)
            )
        """)
        
        # Predicted vs Actual tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS launch_predictions (
                prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                launch_id INTEGER,
                predicted_date DATE,
                predicted_time TIME,
                prediction_source TEXT,
                confidence TEXT,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (launch_id) REFERENCES launches(launch_id)
            )
        """)
        
        # Initialize default status values
        default_statuses = [
            ('Scheduled', '#FFFF00', 'Launch is scheduled'),
            ('Go', '#00FF00', 'Launch confirmed go'),
            ('Scrubbed', '#FF6600', 'Launch scrubbed/delayed'),
            ('Success', '#00AA00', 'Launch successful'),
            ('Failure', '#FF0000', 'Launch failure'),
            ('Unknown', '#CCCCCC', 'Status unknown'),
            ('NET', '#FFCC00', 'No Earlier Than - tentative'),
        ]
        
        for status_name, color, description in default_statuses:
            cursor.execute("""
                INSERT OR IGNORE INTO launch_status (status_name, color, description)
                VALUES (?, ?, ?)
            """, (status_name, color, description))
        
        self.conn.commit()
        self._populate_initial_data()
    
    def _populate_initial_data(self):
        """Populate initial launch sites and rockets from common Chinese launch infrastructure"""
        cursor = self.conn.cursor()
        
        # Chinese Launch Sites
        sites = [
            ('Jiuquan', 'SLS-1', 40.96, 100.29, 'Gobi Desert, Inner Mongolia'),
            ('Jiuquan', 'SLS-2', 40.96, 100.29, 'Gobi Desert, Inner Mongolia'),
            ('Jiuquan', 'LS-95', 40.96, 100.29, 'Gobi Desert, Inner Mongolia'),
            ('Jiuquan', 'LS-96', 40.96, 100.29, 'Gobi Desert, Inner Mongolia'),
            ('Jiuquan', 'LS-120', 40.96, 100.29, 'Gobi Desert, Inner Mongolia'),
            ('Jiuquan', 'LS-130', 40.96, 100.29, 'Gobi Desert, Inner Mongolia'),
            ('Taiyuan', 'LA-9', 37.85, 112.55, 'Shanxi Province'),
            ('Taiyuan', 'LA-9A', 37.85, 112.55, 'Shanxi Province'),
            ('Taiyuan', 'Mobile', 37.85, 112.55, 'Shanxi Province'),
            ('Xichang', 'LA-2', 28.25, 102.03, 'Sichuan Province'),
            ('Xichang', 'LA-3', 28.25, 102.03, 'Sichuan Province'),
            ('Wenchang', 'LC-101', 19.61, 110.95, 'Hainan Island'),
            ('Wenchang', 'LC-201', 19.61, 110.95, 'Hainan Island'),
            ('Dong feng', 'JIQUAN', 40.96, 100.29, 'Alternative name'),
            ('LOP NOR', 'JIQUAN', 40.96, 100.29, 'Historical test site'),
        ]
        
        for location, pad, lat, lon, notes in sites:
            cursor.execute("""
                INSERT OR IGNORE INTO launch_sites (location, launch_pad, latitude, longitude, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (location, pad, lat, lon, notes))
        
        # Common Chinese Rockets
        rockets = [
            ('Long March 2C', 'LM-2', 2, 3850, 1250, 43.0, 3.35, 233, 'LEO/SSO workhorse'),
            ('Long March 2D', 'LM-2', 2, 3500, 1200, 41.0, 3.35, 232, 'LEO workhorse'),
            ('Long March 2F/G', 'LM-2', 2, 8600, None, 62.0, 3.35, 480, 'Crewed launches'),
            ('Long March 3B/E', 'LM-3', 3, 11500, 5500, 56.3, 3.35, 458, 'GTO heavy lifter'),
            ('Long March 4B', 'LM-4', 3, 4200, 1500, 45.8, 3.35, 249, 'SSO specialist'),
            ('Long March 4C', 'LM-4', 3, 4200, 1500, 45.8, 3.35, 250, 'SSO specialist'),
            ('Long March 6', 'LM-6', 3, 1500, None, 29.3, 3.35, 103, 'Small sat launcher'),
            ('Long March 6C', 'LM-6', 3, 2000, None, 43.0, 3.35, 215, 'Upgraded LM-6'),
            ('Long March 6A', 'LM-6', 3, 4000, None, 50.3, 3.35, 530, 'Solid boosters'),
            ('Long March 7', 'LM-7', 2, 13500, 5500, 53.1, 3.35, 594, 'Modern medium-lift'),
            ('Long March 7A', 'LM-7', 3, 7000, 5000, 60.1, 3.35, 573, 'GTO capable'),
            ('Long March 8', 'LM-8', 2, 8100, 2800, 50.3, 3.35, 356, 'Commercial launcher'),
            ('Long March 11', 'LM-11', 4, 700, None, 20.8, 2.0, 58, 'Solid fuel, mobile'),
            ('ShenLong', 'Spaceplane', 1, None, None, None, None, None, 'Reusable spaceplane'),
            ('Tianzhou', 'CZ-7', 2, None, None, 53.1, 3.35, 594, 'Cargo spacecraft'),
            ('Shenzhou', 'CZ-2F', 2, None, None, 62.0, 3.35, 480, 'Crewed spacecraft'),
            ('Ceres-1', 'Commercial', 4, 350, None, 19.5, 1.4, 33, 'Galactic Energy'),
            ('Kuaizhou-1A', 'Commercial', 4, 300, None, 25.0, 1.4, 30, 'CASIC commercial'),
            ('Kuaizhou-11', 'Commercial', 4, 1000, None, 25.0, 2.2, 78, 'CASIC commercial'),
            ('Gushenxing-1', 'Commercial', 4, 300, None, 20.0, 1.4, 23, 'Orienspace'),
            ('Hyperbola-1', 'Commercial', 4, 300, None, 20.8, 1.4, 31, 'i-Space'),
            ('Tianlong-2', 'Commercial', 2, 1500, None, 32.8, 3.35, 153, 'Landspace'),
            ('Zhuque-2', 'Commercial', 2, 6000, None, 49.5, 3.35, 219, 'Landspace methane'),
            ('Kinetica-1', 'Commercial', 4, 500, None, 30.0, 2.65, 135, 'Space Pioneer'),
            ('Shuangquxian-1', 'Commercial', 2, None, None, None, None, None, 'Space Pioneer'),
        ]
        
        for name, family, stages, leo, gto, height, diameter, mass, notes in rockets:
            cursor.execute("""
                INSERT OR IGNORE INTO rockets (name, family, stages, payload_capacity_leo, 
                                              payload_capacity_gto, height, diameter, mass, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, family, stages, leo, gto, height, diameter, mass, notes))
        
        self.conn.commit()
    
    def add_launch(self, launch_data: Dict) -> int:
        """Add a new launch to the database"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO launches (
                launch_date, launch_time, launch_window_start, launch_window_end,
                site_id, rocket_id, vehicle_id, mission_name, payload_name,
                payload_mass, orbit_type, orbit_altitude, inclination,
                status_id, success, failure_reason, remarks, source_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            launch_data.get('launch_date'),
            launch_data.get('launch_time'),
            launch_data.get('launch_window_start'),
            launch_data.get('launch_window_end'),
            launch_data.get('site_id'),
            launch_data.get('rocket_id'),
            launch_data.get('vehicle_id'),
            launch_data.get('mission_name'),
            launch_data.get('payload_name'),
            launch_data.get('payload_mass'),
            launch_data.get('orbit_type'),
            launch_data.get('orbit_altitude'),
            launch_data.get('inclination'),
            launch_data.get('status_id', 1),  # Default to 'Scheduled'
            launch_data.get('success'),
            launch_data.get('failure_reason'),
            launch_data.get('remarks'),
            launch_data.get('source_url')
        ))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_launches_by_month(self, year: int, month: int) -> List[Dict]:
        """Get all launches for a specific month"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT 
                l.*,
                ls.location,
                ls.launch_pad,
                r.name as rocket_name,
                r.family as rocket_family,
                st.status_name,
                st.color as status_color
            FROM launches l
            LEFT JOIN launch_sites ls ON l.site_id = ls.site_id
            LEFT JOIN rockets r ON l.rocket_id = r.rocket_id
            LEFT JOIN launch_status st ON l.status_id = st.status_id
            WHERE strftime('%Y', l.launch_date) = ? 
            AND strftime('%m', l.launch_date) = ?
            ORDER BY l.launch_date, l.launch_time
        """, (str(year), f"{month:02d}"))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_launches_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get launches within a date range"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT 
                l.*,
                ls.location,
                ls.launch_pad,
                r.name as rocket_name,
                r.family as rocket_family,
                st.status_name,
                st.color as status_color
            FROM launches l
            LEFT JOIN launch_sites ls ON l.site_id = ls.site_id
            LEFT JOIN rockets r ON l.rocket_id = r.rocket_id
            LEFT JOIN launch_status st ON l.status_id = st.status_id
            WHERE l.launch_date BETWEEN ? AND ?
            ORDER BY l.launch_date, l.launch_time
        """, (start_date, end_date))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_sites(self) -> List[Dict]:
        """Get all launch sites"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM launch_sites WHERE active = 1 ORDER BY location, launch_pad")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_rockets(self) -> List[Dict]:
        """Get all rocket types"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM rockets WHERE active = 1 ORDER BY family, name")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_statuses(self) -> List[Dict]:
        """Get all launch statuses"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM launch_status ORDER BY status_id")
        return [dict(row) for row in cursor.fetchall()]
    
    def update_launch(self, launch_id: int, launch_data: Dict):
        """Update an existing launch"""
        cursor = self.conn.cursor()
        
        # Build dynamic UPDATE query based on provided fields
        fields = []
        values = []
        
        for key, value in launch_data.items():
            if key != 'launch_id':
                fields.append(f"{key} = ?")
                values.append(value)
        
        if fields:
            values.append(launch_id)
            query = f"UPDATE launches SET {', '.join(fields)}, last_updated = CURRENT_TIMESTAMP WHERE launch_id = ?"
            cursor.execute(query, values)
            self.conn.commit()
    
    def delete_launch(self, launch_id: int):
        """Delete a launch"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM launches WHERE launch_id = ?", (launch_id,))
        self.conn.commit()
    
    def search_launches(self, search_term: str) -> List[Dict]:
        """Search launches by mission name, payload, or rocket"""
        cursor = self.conn.cursor()
        
        search_pattern = f"%{search_term}%"
        cursor.execute("""
            SELECT 
                l.*,
                ls.location,
                ls.launch_pad,
                r.name as rocket_name,
                st.status_name,
                st.color as status_color
            FROM launches l
            LEFT JOIN launch_sites ls ON l.site_id = ls.site_id
            LEFT JOIN rockets r ON l.rocket_id = r.rocket_id
            LEFT JOIN launch_status st ON l.status_id = st.status_id
            WHERE l.mission_name LIKE ? 
            OR l.payload_name LIKE ?
            OR r.name LIKE ?
            ORDER BY l.launch_date DESC
        """, (search_pattern, search_pattern, search_pattern))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict:
        """Get launch statistics"""
        cursor = self.conn.cursor()
        
        stats = {}
        
        # Total launches
        cursor.execute("SELECT COUNT(*) as total FROM launches")
        stats['total_launches'] = cursor.fetchone()['total']
        
        # Success rate
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN success = 1 THEN 1 END) as successful,
                COUNT(CASE WHEN success = 0 THEN 1 END) as failed,
                COUNT(CASE WHEN success IS NULL THEN 1 END) as pending
            FROM launches
        """)
        row = cursor.fetchone()
        stats['successful'] = row['successful']
        stats['failed'] = row['failed']
        stats['pending'] = row['pending']
        
        # By rocket type
        cursor.execute("""
            SELECT r.name, COUNT(*) as count
            FROM launches l
            JOIN rockets r ON l.rocket_id = r.rocket_id
            GROUP BY r.name
            ORDER BY count DESC
            LIMIT 10
        """)
        stats['by_rocket'] = [dict(row) for row in cursor.fetchall()]
        
        # By launch site
        cursor.execute("""
            SELECT ls.location, COUNT(*) as count
            FROM launches l
            JOIN launch_sites ls ON l.site_id = ls.site_id
            GROUP BY ls.location
            ORDER BY count DESC
        """)
        stats['by_site'] = [dict(row) for row in cursor.fetchall()]
        
        return stats
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
