# SHOCKWAVE PLANNER v1.1 - Upgrade Specification

**Based on Team Feedback - November 29, 2025**

## Overview

The team at REMIX has requested an enhanced interface that more closely resembles a Gantt-chart timeline view, with collapsible country groupings and launch pad turnaround visualization.

## Key Changes Requested

### 1. Timeline View (Primary Change)
**Replace the calendar grid with horizontal timeline**

**Current (v1.0)**:
- Calendar month grid (Mon-Sun)
- Each cell shows day number
- Launches listed within cells

**New (v1.1)**:
- Horizontal timeline with days 1-31 across top
- Rows for each launch site/pad
- Launch bars span across dates
- Grey bars show pad unavailability after launch

**Visual Layout**:
```
┌─────────────┬────────────┬───────────┬─1─┬─2─┬─3─┬───┬─30─┬─31─┐
│ LOCATION    │ LAUNCH PAD │ ROCKET    │   │   │   │...│    │    │
├─────────────┼────────────┼───────────┼───┼───┼───┼───┼────┼────┤
│ ▼ China     │            │           │   │   │   │   │    │    │ ← Collapsible group
├─────────────┼────────────┼───────────┼───┼───┼───┼───┼────┼────┤
│   Jiuquan   │ SLS-1      │ LM-2F/G   │   │ █ │░░░│   │    │    │ █=launch, ░=turnaround
│   Jiuquan   │ LS-95      │ Ceres-1   │   │   │   │ █ │░░░░│    │
│   Taiyuan   │ LA-9A      │ LM-6C     │   │   │   │   │ █  │░░░ │
├─────────────┼────────────┼───────────┼───┼───┼───┼───┼────┼────┤
│ ▶ USA       │            │           │   │   │   │   │    │    │ ← Collapsed group
└─────────────┴────────────┴───────────┴───┴───┴───┴───┴────┴────┘
```

### 2. Grouped Launch Sites by Nation/Region

**Country Groups**:
- **China**: Jiuquan, Taiyuan, Xichang, Wenchang
- **USA**: Cape Canaveral, Vandenberg, Kennedy, Wallops
- **Russia**: Baikonur, Plesetsk, Vostochny
- **Europe**: Kourou (French Guiana)
- **Pacific**: Mahia (Rocket Lab), others
- **India**: Satish Dhawan
- **Japan**: Tanegashima, Uchinoura

**Behavior**:
- Click country header to expand/collapse
- Only show expanded countries' sites
- Icon changes: ▶ (collapsed) / ▼ (expanded)

### 3. List View Date Range Filters

**Quick Date Range Options**:
- **Previous 7 days** - Last week's launches
- **Previous 30 days** - Last month's launches  
- **Current** - Today's launches
- **Next 30 days** - Upcoming month of launches

**UI Layout**:
```
┌─────────────────────────────────────────────────────┐
│ List View                                           │
├─────────────────────────────────────────────────────┤
│ Date Range: [Previous 7 Days ▼] [Apply]            │
│                                                     │
│ Options: ○ Previous 7 Days                          │
│          ○ Previous 30 Days                         │
│          ● Current                                  │
│          ○ Next 30 Days                             │
│          ○ Custom Range...                          │
└─────────────────────────────────────────────────────┘
```

**Benefits**:
- Quick access to relevant time periods
- Common operational queries (past week, upcoming month)
- Easy comparison of historical vs upcoming
- Custom range option for flexibility

### 4. Show Only Active Sites

**Filter Option**:
- Checkbox: "Show only sites with launches"
- When checked: Hide rows with no launches in current month
- When unchecked: Show all sites regardless

**Benefits**:
- Cleaner view focused on actual activity
- Easier to track busy periods
- Option to see all infrastructure when needed

### 5. NOTAM (Notice to Airmen) Integration

**Purpose**: Track airspace restrictions around launch sites

**NOTAM Field Addition**:
- Add to launches table: `notam_reference TEXT`
- Track official NOTAM numbers/references
- Link to NOTAM documents/URLs

**Future: 2-Day NOTAM Mapping** (v1.2+)

**Concept**: Visual map showing NOTAM areas for T-2 days to launch

**Features**:
- Geographic visualization of restricted airspace
- Time-based NOTAM activation
- Multiple NOTAM zones per launch
- Integration with launch hazard areas

**Example NOTAM Data**:
```
NOTAM: A1234/25
Location: Jiuquan SLC
Radius: 100 NM from 40°58'N 100°17'E
Altitude: Surface to FL600
Active: 2025-12-05 06:00Z to 2025-12-05 10:00Z
Purpose: Space launch operations
```

**Visual Representation**:
```
┌─────────────────────────────────────────────────┐
│ NOTAM Map - 2 Days to Launch                   │
├─────────────────────────────────────────────────┤
│                                                 │
│         [Interactive Map View]                  │
│                                                 │
│    ╔═══════════════╗                           │
│    ║  Jiuquan SLC  ║ ← Launch Site             │
│    ╚═══════════════╝                           │
│         ⊙ ⊙ ⊙  ← NOTAM zones (concentric)      │
│       ⊙ ⊙ ⊙ ⊙                                  │
│     ⊙ ⊙ ⊙ ⊙ ⊙                                 │
│                                                 │
│ Active NOTAMs:                                  │
│  • A1234/25 - 100NM radius - SFC/FL600         │
│  • A1235/25 - Sea zone - Launch corridor       │
│                                                 │
│ Activation: T-2h to T+4h                        │
└─────────────────────────────────────────────────┘
```

**Database Schema for NOTAMs**:
```sql
CREATE TABLE launch_notams (
    notam_id INTEGER PRIMARY KEY AUTOINCREMENT,
    launch_id INTEGER,
    notam_reference TEXT NOT NULL,
    notam_type TEXT,  -- 'Airspace', 'Maritime', 'Hazard Area'
    center_lat REAL,
    center_lon REAL,
    radius_nm REAL,  -- Nautical miles
    altitude_min INTEGER,  -- Feet
    altitude_max INTEGER,  -- Feet
    active_start DATETIME,
    active_end DATETIME,
    description TEXT,
    source_url TEXT,
    FOREIGN KEY (launch_id) REFERENCES launches(launch_id)
);

CREATE TABLE notam_polygons (
    polygon_id INTEGER PRIMARY KEY AUTOINCREMENT,
    notam_id INTEGER,
    point_order INTEGER,
    latitude REAL,
    longitude REAL,
    FOREIGN KEY (notam_id) REFERENCES launch_notams(notam_id)
);
```

**Implementation Phases**:

**Phase 1 (v1.1)**: Basic NOTAM field
- Add `notam_reference` field to launches
- Manual entry in launch editor
- Display in launch details

**Phase 2 (v1.2)**: NOTAM database
- Full NOTAM tracking table
- Multiple NOTAMs per launch
- Geometry storage (circles, polygons)

**Phase 3 (v1.3)**: NOTAM mapping
- Interactive map display
- 2-day countdown view
- Airspace conflict detection
- Integration with flight tracking

**Data Sources for NOTAMs**:
- **Manual Entry**: From official NOTAM bulletins
- **China CAAC**: Civil Aviation Administration of China
- **ICAO**: International Civil Aviation Organization
- **FAA** (for US launches): Federal Aviation Administration
- **Future**: Automated NOTAM scraping/parsing

**NOTAM Types**:
- **Airspace Closure**: Restricted flight zones
- **Maritime Hazard**: Sea exclusion zones (for coastal launches)
- **Launch Corridor**: Trajectory hazard areas
- **Debris Field**: Predicted impact zones for spent stages

**Integration with Timeline View**:
```
Day:  1  2  3  4  5  6  7  8  9  10
      █  ░  ░  ░  ░  ░  ░  ░
      🚫 ← NOTAM active (shown as overlay)
```

**Use Cases**:
1. **Pre-launch Planning**: Visualize airspace impacts
2. **Coordination**: Share NOTAM info with aviation authorities
3. **Analysis**: Study NOTAM patterns and durations
4. **Safety**: Ensure proper airspace management
5. **TAWHIRI Integration**: Conjunction screening + airspace conflicts

### 6. Launch Pad Turnaround Time

**Gray Bar Visualization**:
- After each launch, show grey cells for N days
- Configurable turnaround period (default: 7 days)
- Represents pad being unavailable for next launch

**Example**:
```
Day:  1  2  3  4  5  6  7  8  9  10
      █  ░  ░  ░  ░  ░  ░  ░
      ^  ^-----------^
   Launch  Turnaround (7 days)
```

**Configuration**:
- Spinner control: "Pad turnaround (days): [7]"
- Range: 0-30 days
- Updates view immediately

### 5. Schema Extension Tool (Future Enhancement)

**Purpose**: Dynamically add fields to track rocket performance data

**Capabilities**:
- Add columns to existing tables
- Create extension tables linked to base tables
- Track schema change history
- Suggest common extensions (rocket performance)

**Use Case**: Add rocket construction/performance fields
```
Examples:
- thrust_vacuum (REAL)
- isp_vacuum (REAL)  
- propellant_type (TEXT)
- propellant_mass (REAL)
- burn_time (REAL)
- reusable (BOOLEAN)
- stage_count (INTEGER)
```

**UI Integration** (planned):
- Tools menu → "Extend Schema"
- Select table to extend
- Choose from suggested fields or add custom
- Apply changes with automatic migration

## Implementation Details

### Timeline View Widget

**File**: `gui/timeline_view.py`

**Key Features**:
```python
class TimelineView(QWidget):
    - update_timeline()       # Build the view
    - create_controls()       # Navigation & filters
    - cell_clicked()          # Handle interactions
    - toggle_active_only()    # Filter sites
    - update_turnaround()     # Adjust grey bars
```

**Data Structure**:
```python
rows = [
    {'type': 'group', 'country': 'China', 'expanded': True},
    {'type': 'site', 'location': 'Jiuquan', 'pad': 'SLS-1', 'launches': [...]},
    {'type': 'site', 'location': 'Jiuquan', 'pad': 'LS-95', 'launches': [...]},
    ...
]
```

### Schema Extension Tool

**File**: `data/schema_extension.py`

**Key Methods**:
```python
class SchemaExtension:
    - add_column(table, column, type, default)
    - create_extension_table(base_table, fields)
    - get_table_schema(table)
    - suggest_rocket_performance_schema()
    - apply_rocket_performance_schema()
```

**Example Usage**:
```python
# Add a single field
ext = SchemaExtension('shockwave_planner.db')
ext.add_column('rockets', 'thrust_vacuum', 'REAL')

# Apply suggested rocket performance schema
ext.apply_rocket_performance_schema()
```

## Updated Main Window

**Changes to `gui/main_window.py`**:

1. **Import TimelineView**:
```python
from gui.timeline_view import TimelineView
```

2. **Replace CalendarView with TimelineView**:
```python
# OLD:
self.calendar_view = CalendarView(self.db)

# NEW:
self.timeline_view = TimelineView(self.db)
self.tab_widget.addTab(self.timeline_view, "Timeline View")
```

3. **Add Schema Extension Menu**:
```python
tools_menu = menubar.addMenu('Tools')
schema_action = QAction('Extend Schema...', self)
schema_action.triggered.connect(self.open_schema_tool)
tools_menu.addAction(schema_action)
```

4. **Add Data Import Menu**:
```python
data_menu = menubar.addMenu('Data')
import_spacedevs_action = QAction('Import from Space Devs...', self)
import_spacedevs_action.triggered.connect(self.import_from_spacedevs)
data_menu.addAction(import_spacedevs_action)
```

5. **Schema Tool Dialog** (future):
```python
def open_schema_tool(self):
    dialog = SchemaExtensionDialog(self.db, parent=self)
    dialog.exec()
```

## Space Devs API Integration

### Overview

**The Space Devs** (https://ll.thespacedevs.com) provides a comprehensive, free API for launch data covering all space-faring nations.

**Benefits**:
- ✅ Comprehensive global launch data
- ✅ Real-time updates
- ✅ Historical data available
- ✅ Free tier available
- ✅ Well-documented API
- ✅ Includes Chinese, US, Russian, European launches
- ✅ Launch sites, rockets, missions all included

### API Endpoints

**Base URL**: `https://ll.thespacedevs.com/2.2.0/`

**Key Endpoints**:
```
/launch/                    # List launches
/launch/{id}/              # Launch details
/launch/upcoming/          # Upcoming launches
/launch/previous/          # Past launches
/location/                 # Launch sites
/launcher/                 # Rocket types
/pad/                      # Launch pads
```

### Data Mapping

**Space Devs → SHOCKWAVE Database**:

```python
# Launch mapping
{
    'name': 'mission_name',
    'net': 'launch_date + launch_time',
    'window_start': 'launch_window_start',
    'window_end': 'launch_window_end',
    'status.name': 'status_id',  # Map to our status types
    'pad.name': 'site_id',       # Match to launch_sites
    'rocket.configuration.name': 'rocket_id',  # Match to rockets
    'mission.name': 'payload_name',
    'mission.orbit.name': 'orbit_type',
}
```

### Implementation

**File**: `data/spacedevs_import.py`

**Key Features**:
```python
class SpaceDevsImporter:
    def __init__(self, db_path, api_key=None):
        """Initialize with optional API key for higher rate limits"""
        self.base_url = "https://ll.thespacedevs.com/2.2.0"
        self.db = LaunchDatabase(db_path)
        self.api_key = api_key
    
    def fetch_upcoming_launches(self, limit=100):
        """Fetch upcoming launches"""
        
    def fetch_launches_by_date_range(self, start_date, end_date):
        """Fetch launches in date range"""
        
    def import_launch(self, spacedevs_data):
        """Import single launch from Space Devs format"""
        
    def import_batch(self, launches):
        """Import multiple launches"""
        
    def update_existing_launches(self):
        """Update status of existing launches"""
        
    def sync_launch_sites(self):
        """Sync launch sites from Space Devs"""
        
    def sync_rockets(self):
        """Sync rocket types from Space Devs"""
```

**Example Usage**:
```python
importer = SpaceDevsImporter('shockwave_planner.db')

# Import next 50 upcoming launches
launches = importer.fetch_upcoming_launches(limit=50)
importer.import_batch(launches)

# Import launches for specific date range
launches = importer.fetch_launches_by_date_range(
    '2025-12-01', 
    '2025-12-31'
)
importer.import_batch(launches)

# Daily update - sync status changes
importer.update_existing_launches()
```

### UI Integration

**Import Dialog**:
```
┌─────────────────────────────────────────────┐
│ Import from Space Devs                      │
├─────────────────────────────────────────────┤
│                                             │
│ Import Type:                                │
│  ( ) Upcoming launches                      │
│      Number to import: [50  ▼]             │
│                                             │
│  (•) Date range                             │
│      From: [2025-12-01 📅]                 │
│      To:   [2025-12-31 📅]                 │
│                                             │
│  ( ) Update existing launches               │
│      (Refresh status of tracked launches)   │
│                                             │
│ Options:                                    │
│  ☑ Import launch sites if missing          │
│  ☑ Import rockets if missing               │
│  ☑ Skip duplicates (match by date+rocket)  │
│  ☐ Overwrite existing data                 │
│                                             │
│ Data Source Tracking:                       │
│  Tag imported launches: [Space Devs ▼]     │
│                                             │
│         [Cancel]  [Preview]  [Import]       │
└─────────────────────────────────────────────┘
```

### Database Schema Extension

**Add data source tracking**:
```sql
ALTER TABLE launches ADD COLUMN data_source TEXT DEFAULT 'Manual';
ALTER TABLE launches ADD COLUMN external_id TEXT;
ALTER TABLE launches ADD COLUMN last_synced DATETIME;
```

**Track import history**:
```sql
CREATE TABLE data_imports (
    import_id INTEGER PRIMARY KEY AUTOINCREMENT,
    import_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    source TEXT NOT NULL,
    import_type TEXT,  -- 'upcoming', 'date_range', 'update'
    records_imported INTEGER,
    records_updated INTEGER,
    records_skipped INTEGER,
    parameters TEXT,   -- JSON of import parameters
    notes TEXT
);
```

### Status Mapping

**Space Devs Status → SHOCKWAVE Status**:
```python
STATUS_MAPPING = {
    'Go for Launch': 'Go',
    'To Be Determined': 'Scheduled',
    'To Be Confirmed': 'NET',
    'Launch Successful': 'Success',
    'Launch Failure': 'Failure',
    'On Hold': 'Scrubbed',
    'In Flight': 'Success',
}
```

### Rate Limiting

**Free Tier**: 15 requests/hour
**With API Key**: 300 requests/hour (free registration)

**Implementation**:
```python
class RateLimiter:
    def __init__(self, max_requests=15, time_window=3600):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
```

### Error Handling

**Network Issues**:
- Retry with exponential backoff
- Cache responses locally
- Continue on individual failures

**Data Issues**:
- Validate before import
- Log conflicts
- Provide manual resolution UI

### Automatic Updates

**Scheduled Sync**:
```python
class AutoSync:
    def __init__(self, db_path, schedule='daily'):
        """
        Schedule options:
        - 'hourly': Every hour
        - 'daily': Once per day (8am local)
        - 'weekly': Once per week (Monday)
        """
        
    def start_background_sync(self):
        """Start background thread for auto-sync"""
        
    def stop_background_sync(self):
        """Stop background sync"""
```

**UI Control**:
```
Settings → Auto-Update
  ☑ Enable automatic updates
  Schedule: [Daily ▼]
  Time: [08:00]
  
  Last update: 2025-11-29 08:00
  Next update: 2025-11-30 08:00
  
  [Update Now]  [Configure]
```

### Filtering Chinese Launches

**Focus on Chinese launches**:
```python
def fetch_chinese_launches(self, start_date, end_date):
    """
    Fetch only Chinese launches
    Filter by launch sites or rocket families
    """
    chinese_sites = [
        'Jiuquan Satellite Launch Center',
        'Taiyuan Satellite Launch Center',
        'Xichang Satellite Launch Center',
        'Wenchang Space Launch Site'
    ]
    
    chinese_rockets = [
        'Long March',  # All variants
        'Kuaizhou',
        'Ceres',
        # etc.
    ]
```

### Data Quality

**Validation**:
- Check for required fields
- Validate date formats
- Verify rocket/site exists in DB
- Flag suspicious data for review

**Conflict Resolution**:
- Manual entry takes precedence
- Show diff dialog for conflicts
- Option to merge or replace

### Benefits for TAWHIRI Integration

**Launch → TLE Correlation**:
- Space Devs provides NORAD IDs
- Link launches to satellite tracking
- Automatic TLE fetching for new satellites

**Example**:
```python
# After importing launch
if launch.successful and launch.payload_norad_id:
    # Fetch TLE for this satellite
    tle = fetch_tle(launch.payload_norad_id)
    db.add_launch_tle(launch_id, tle)
```

## Color Coding

**Launch Status Colors** (same as v1.0):
- Yellow (#FFFF00): Scheduled
- Green (#00FF00): Go
- Dark Green (#00AA00): Success
- Orange (#FF6600): Scrubbed
- Red (#FF0000): Failure
- Light Orange (#FFCC00): NET
- Grey (#CCCCCC): Unknown

**New Colors**:
- Grey (#C8C8C8): Pad turnaround period
- Light Blue (#E8F4FF): Site row background

## Database Changes

**No schema changes required for timeline view**

**For Schema Extension Feature**:
- New table: `schema_changes` (tracks modifications)
- Suggested extensions: `rockets_stage_performance`

## User Workflow

### Viewing Launches

1. Open SHOCKWAVE PLANNER
2. Timeline view shows current month
3. See launches as colored bars
4. Grey bars show pad downtime
5. Click country headers to expand/collapse
6. Check "Show only sites with launches" for cleaner view

### Adding Launch

1. Click "New Launch" button
2. Fill form (same as v1.0)
3. Launch appears as colored bar in timeline
4. Turnaround period automatically shown

### Adjusting Turnaround

1. Change "Pad turnaround (days)" spinner
2. View updates immediately
3. See how pad availability changes

### Future: Extending Schema

1. Tools → Extend Schema
2. Select "rockets" table
3. Choose "Apply Rocket Performance Fields"
4. Fields added automatically
5. Edit rocket entries to add performance data

## Migration from v1.0 to v1.1

**Backward Compatible**:
- Same database format
- v1.0 database works in v1.1
- No data migration needed

**New Features Optional**:
- Timeline view is new default
- Old calendar view available as tab
- Schema extension tool separate

## File Structure

```
shockwave_v1.1/
├── main.py
├── gui/
│   ├── main_window.py         # Updated with TimelineView
│   ├── timeline_view.py       # NEW - Gantt-style timeline
│   ├── schema_dialog.py       # NEW - Schema extension UI (future)
│   └── import_dialog.py       # NEW - Space Devs import UI
├── data/
│   ├── database.py            # Updated with source tracking
│   ├── schema_extension.py    # NEW - Schema modification tool
│   └── spacedevs_import.py    # NEW - Space Devs API integration
├── utils/
│   └── rate_limiter.py        # NEW - API rate limiting
└── shockwave_planner.db       # Extended schema
```

## Testing Plan

### Timeline View
- ✓ Displays current month correctly
- ✓ Shows launches as colored bars
- ✓ Grey bars appear after launches
- ✓ Country groups expand/collapse
- ✓ Filter hides empty sites
- ✓ Turnaround days adjustable
- ✓ Click launch to edit
- ✓ Month navigation works

### Schema Extension
- ✓ Can view current schema
- ✓ Add column works
- ✓ Extension table created correctly
- ✓ Changes logged
- ✓ Rocket performance fields apply
- ✓ No data loss

## Deployment

**Installation**:
Same as v1.0 - no new dependencies

**Upgrade**:
1. Backup current database
2. Replace application files
3. Run v1.1
4. Database migrates automatically

## Next Steps

### Immediate (v1.1.0)
1. Implement TimelineView widget
2. Update main window
3. Test with sample data
4. Package for distribution

### Short-term (v1.1.1)
1. Add schema extension dialog UI
2. Implement rocket performance fields
3. Add data entry forms for new fields
4. Documentation updates

### Short-term (v1.1.2)
1. Space Devs API integration
2. Automatic launch data import
3. Scheduled updates (daily/weekly)
4. Data source tracking per launch

### Medium-term (v1.2.0)
1. Multiple month view
2. Zoom in/out timeline
3. Export timeline as image
4. Import launch manifests (multiple sources)
5. Auto-update from web sources

## Questions for Team

1. **Default Turnaround**: Is 7 days correct for most pads?
2. **Country Groups**: Any additions/changes needed?
3. **Schema Fields**: Which rocket performance fields are priority?
4. **View Preference**: Keep old calendar view as option?
5. **Export**: Need timeline export to Excel/PNG?
6. **Space Devs**: 
   - Should auto-import be enabled by default?
   - How often to sync? (daily/weekly?)
   - Import all nations or focus on specific ones?
   - Prefer Space Devs data or manual entry when conflict?

## Summary

This v1.1 upgrade transforms SHOCKWAVE from a calendar-based tracker to a professional timeline/Gantt view that matches operational planning workflows. The grouped, collapsible structure and pad turnaround visualization directly address the team's feedback.

The schema extension tool future-proofs the platform for expanding data requirements, particularly around rocket construction and performance characteristics.

---

**Status**: Specification Complete
**Next**: Implement Timeline View
**Priority**: High
**Effort**: ~8-12 hours development + testing
