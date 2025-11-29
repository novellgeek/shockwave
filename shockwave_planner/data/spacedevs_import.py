"""
SHOCKWAVE PLANNER - Space Devs API Integration
Import launch data from The Space Devs Launch Library 2 API
https://ll.thespacedevs.com
"""
import requests
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json


class RateLimiter:
    """Simple rate limiter for API requests"""
    
    def __init__(self, max_requests=15, time_window=3600):
        self.max_requests = max_requests
        self.time_window = time_window  # seconds
        self.requests = []
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        
        # Remove old requests outside time window
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time < self.time_window]
        
        if len(self.requests) >= self.max_requests:
            # Need to wait
            oldest = min(self.requests)
            wait_time = self.time_window - (now - oldest) + 1
            print(f"Rate limit reached. Waiting {wait_time:.0f} seconds...")
            time.sleep(wait_time)
        
        self.requests.append(now)


class SpaceDevsImporter:
    """
    Import launch data from The Space Devs API
    """
    
    BASE_URL = "https://ll.thespacedevs.com/2.2.0"
    
    # Status mapping from Space Devs to SHOCKWAVE
    STATUS_MAP = {
        'Go for Launch': 'Go',
        'To Be Determined': 'Scheduled',
        'To Be Confirmed': 'NET',
        'Launch Successful': 'Success',
        'Launch Failure': 'Failure',
        'On Hold': 'Scrubbed',
        'In Flight': 'Success',
        'Partial Failure': 'Failure',
    }
    
    def __init__(self, db, api_key=None):
        """
        Initialize Space Devs importer
        
        Args:
            db: LaunchDatabase instance
            api_key: Optional API key for higher rate limits
        """
        self.db = db
        self.api_key = api_key
        self.rate_limiter = RateLimiter(
            max_requests=300 if api_key else 15,
            time_window=3600
        )
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({'Authorization': f'Token {api_key}'})
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make API request with rate limiting"""
        self.rate_limiter.wait_if_needed()
        
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
    
    def fetch_upcoming_launches(self, limit=100, offset=0) -> List[Dict]:
        """
        Fetch upcoming launches
        
        Args:
            limit: Number of launches to fetch (max 100 per request)
            offset: Pagination offset
        
        Returns:
            List of launch data dictionaries
        """
        params = {
            'limit': min(limit, 100),
            'offset': offset
        }
        
        data = self._make_request('launch/upcoming/', params)
        if data and 'results' in data:
            return data['results']
        return []
    
    def fetch_launches_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Fetch launches in date range
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        
        Returns:
            List of launch data dictionaries
        """
        params = {
            'net__gte': f"{start_date}T00:00:00Z",
            'net__lte': f"{end_date}T23:59:59Z",
            'limit': 100
        }
        
        all_launches = []
        offset = 0
        
        while True:
            params['offset'] = offset
            data = self._make_request('launch/', params)
            
            if not data or 'results' not in data:
                break
            
            results = data['results']
            if not results:
                break
            
            all_launches.extend(results)
            
            if not data.get('next'):
                break
            
            offset += len(results)
        
        return all_launches
    
    def fetch_chinese_launches(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Fetch only Chinese launches
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        
        Returns:
            List of Chinese launch data dictionaries
        """
        all_launches = self.fetch_launches_by_date_range(start_date, end_date)
        
        chinese_locations = [
            'Jiuquan', 'Taiyuan', 'Xichang', 'Wenchang',
            'People\'s Republic of China'
        ]
        
        chinese_rockets = [
            'Long March', 'Kuaizhou', 'Ceres', 'Hyperbola',
            'Zhuque', 'Tianlong', 'Kinetica', 'Gushenxing'
        ]
        
        chinese_launches = []
        for launch in all_launches:
            # Check launch location
            pad_location = launch.get('pad', {}).get('location', {}).get('name', '')
            
            # Check rocket name
            rocket_name = launch.get('rocket', {}).get('configuration', {}).get('name', '')
            
            is_chinese = (
                any(loc in pad_location for loc in chinese_locations) or
                any(rocket in rocket_name for rocket in chinese_rockets)
            )
            
            if is_chinese:
                chinese_launches.append(launch)
        
        return chinese_launches
    
    def parse_launch_data(self, spacedevs_launch: Dict) -> Dict:
        """
        Convert Space Devs launch format to SHOCKWAVE format
        
        Args:
            spacedevs_launch: Launch data from Space Devs API
        
        Returns:
            Dictionary in SHOCKWAVE database format
        """
        # Parse NET (No Earlier Than) datetime
        net = spacedevs_launch.get('net', '')
        if net:
            try:
                net_dt = datetime.fromisoformat(net.replace('Z', '+00:00'))
                launch_date = net_dt.strftime('%Y-%m-%d')
                launch_time = net_dt.strftime('%H:%M:%S')
            except:
                launch_date = None
                launch_time = None
        else:
            launch_date = None
            launch_time = None
        
        # Parse window
        window_start = spacedevs_launch.get('window_start', '')
        window_end = spacedevs_launch.get('window_end', '')
        
        # Extract location and pad
        pad_data = spacedevs_launch.get('pad', {})
        location_name = pad_data.get('location', {}).get('name', '')
        pad_name = pad_data.get('name', '')
        
        # Find matching site in database
        sites = self.db.get_all_sites()
        site_id = None
        for site in sites:
            if site['location'] in location_name or location_name in site['location']:
                if site['launch_pad'] in pad_name or pad_name in site['launch_pad']:
                    site_id = site['site_id']
                    break
        
        # Extract rocket
        rocket_data = spacedevs_launch.get('rocket', {}).get('configuration', {})
        rocket_name = rocket_data.get('name', '')
        
        # Find matching rocket in database
        rockets = self.db.get_all_rockets()
        rocket_id = None
        for rocket in rockets:
            if rocket['name'] in rocket_name or rocket_name in rocket['name']:
                rocket_id = rocket['rocket_id']
                break
        
        # Extract mission data
        mission_data = spacedevs_launch.get('mission', {})
        mission_name = spacedevs_launch.get('name', '')
        payload_name = mission_data.get('name', mission_name)
        orbit_name = mission_data.get('orbit', {}).get('name', '')
        
        # Map orbit name to standard types
        orbit_type = self._map_orbit_type(orbit_name)
        
        # Map status
        status_name = spacedevs_launch.get('status', {}).get('name', '')
        mapped_status = self.STATUS_MAP.get(status_name, 'Unknown')
        
        # Find status_id
        statuses = self.db.get_all_statuses()
        status_id = None
        for status in statuses:
            if status['status_name'] == mapped_status:
                status_id = status['status_id']
                break
        
        # Build SHOCKWAVE launch data
        launch_data = {
            'launch_date': launch_date,
            'launch_time': launch_time,
            'launch_window_start': window_start if window_start else None,
            'launch_window_end': window_end if window_end else None,
            'site_id': site_id,
            'rocket_id': rocket_id,
            'mission_name': mission_name,
            'payload_name': payload_name,
            'orbit_type': orbit_type,
            'status_id': status_id,
            'remarks': f"Imported from Space Devs on {datetime.now().strftime('%Y-%m-%d')}",
            'source_url': spacedevs_launch.get('url', ''),
            'data_source': 'Space Devs',
            'external_id': spacedevs_launch.get('id', ''),
        }
        
        return launch_data
    
    def _map_orbit_type(self, orbit_name: str) -> str:
        """Map Space Devs orbit name to SHOCKWAVE orbit type"""
        orbit_name_lower = orbit_name.lower()
        
        if 'leo' in orbit_name_lower or 'low earth' in orbit_name_lower:
            return 'LEO'
        elif 'sso' in orbit_name_lower or 'sun-synchronous' in orbit_name_lower:
            return 'SSO'
        elif 'gto' in orbit_name_lower or 'geosynchronous transfer' in orbit_name_lower:
            return 'GTO'
        elif 'geo' in orbit_name_lower or 'geosynchronous' in orbit_name_lower:
            return 'GEO'
        elif 'meo' in orbit_name_lower or 'medium earth' in orbit_name_lower:
            return 'MEO'
        elif 'heo' in orbit_name_lower or 'highly elliptical' in orbit_name_lower:
            return 'HEO'
        elif 'lunar' in orbit_name_lower or 'moon' in orbit_name_lower:
            return 'Lunar'
        else:
            return 'Other'
    
    def import_launch(self, spacedevs_launch: Dict, skip_duplicates=True) -> Optional[int]:
        """
        Import a single launch from Space Devs data
        
        Args:
            spacedevs_launch: Launch data from Space Devs API
            skip_duplicates: Skip if similar launch exists
        
        Returns:
            launch_id if imported, None if skipped
        """
        launch_data = self.parse_launch_data(spacedevs_launch)
        
        # Check for required fields
        if not launch_data['launch_date']:
            print(f"Skipping launch {launch_data['mission_name']} - no date")
            return None
        
        if skip_duplicates:
            # Check if launch already exists
            existing = self.db.search_launches(launch_data['mission_name'])
            if existing:
                for ex_launch in existing:
                    if ex_launch['launch_date'] == launch_data['launch_date']:
                        print(f"Skipping duplicate: {launch_data['mission_name']}")
                        return None
        
        # Add the launch
        try:
            launch_id = self.db.add_launch(launch_data)
            print(f"Imported: {launch_data['mission_name']} ({launch_data['launch_date']})")
            return launch_id
        except Exception as e:
            print(f"Error importing {launch_data['mission_name']}: {e}")
            return None
    
    def import_batch(self, launches: List[Dict], skip_duplicates=True) -> Dict:
        """
        Import multiple launches
        
        Args:
            launches: List of Space Devs launch data
            skip_duplicates: Skip duplicates
        
        Returns:
            Statistics dictionary
        """
        stats = {
            'imported': 0,
            'skipped': 0,
            'failed': 0
        }
        
        for launch in launches:
            result = self.import_launch(launch, skip_duplicates)
            if result:
                stats['imported'] += 1
            elif result is None:
                stats['skipped'] += 1
            else:
                stats['failed'] += 1
        
        return stats
    
    def update_existing_launches(self) -> int:
        """
        Update status of existing Space Devs launches
        
        Returns:
            Number of launches updated
        """
        # Get all launches from Space Devs in database
        all_launches = self.db.get_launches_by_date_range('2020-01-01', '2030-12-31')
        spacedevs_launches = [l for l in all_launches if l.get('data_source') == 'Space Devs']
        
        updated = 0
        for launch in spacedevs_launches:
            external_id = launch.get('external_id')
            if external_id:
                # Fetch current data from Space Devs
                data = self._make_request(f'launch/{external_id}/')
                if data:
                    # Update status
                    updated_data = self.parse_launch_data(data)
                    if updated_data['status_id'] != launch['status_id']:
                        self.db.update_launch(launch['launch_id'], {
                            'status_id': updated_data['status_id'],
                            'last_synced': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        updated += 1
        
        return updated


# Example usage
if __name__ == '__main__':
    from database import LaunchDatabase
    
    db = LaunchDatabase('../shockwave_planner.db')
    importer = SpaceDevsImporter(db)
    
    # Import upcoming Chinese launches
    print("Fetching Chinese launches...")
    launches = importer.fetch_chinese_launches('2025-11-01', '2025-12-31')
    print(f"Found {len(launches)} Chinese launches")
    
    # Import them
    stats = importer.import_batch(launches)
    print(f"\nImport complete:")
    print(f"  Imported: {stats['imported']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Failed: {stats['failed']}")
    
    db.close()
