# SHOCKWAVE PLANNER - Feature Guide

## Overview

SHOCKWAVE PLANNER v1.0 provides comprehensive launch tracking and planning capabilities with an intuitive desktop interface.

## Core Features

### 1. Calendar View

**Visual Monthly Calendar**
- Grid layout showing entire month at a glance
- Each day displays scheduled launches
- Color-coded by launch status
- Quick navigation between months

**Launch Information Display**
- Launch time (HH:MM format)
- Rocket type
- Payload name
- Multiple launches per day supported

**Interactive Navigation**
- Previous/Next month buttons
- Current month highlighted in header
- Click any day to view/edit launches

**Status Color Coding**
```
Yellow  (#FFFF00) - Scheduled
Green   (#00FF00) - Go (confirmed)
Orange  (#FF6600) - Scrubbed/Delayed
Dark Green (#00AA00) - Success
Red     (#FF0000) - Failure
Gray    (#CCCCCC) - Unknown
Light Orange (#FFCC00) - NET (No Earlier Than)
```

### 2. List View

**Searchable Launch Table**
- Real-time search as you type
- Search across:
  - Mission names
  - Payload names
  - Rocket types
- Results filter dynamically

**Table Columns**
1. Date - Launch date (YYYY-MM-DD)
2. Time - Launch time (HH:MM)
3. Site - Launch location and pad
4. Rocket - Vehicle type
5. Mission - Mission designation
6. Payload - Satellite/spacecraft name
7. Status - Current status (color-coded)

**Interactions**
- Double-click any row to edit
- Select row to highlight
- Sortable columns (planned)
- Export selection (planned)

### 3. Statistics Dashboard

**Launch Overview**
- Total launches tracked
- Successful launches count
- Failed launches count
- Pending launches count
- Overall success rate percentage

**Top Rockets Analysis**
- Top 10 most-used rockets
- Launch count per rocket type
- Family grouping

**Launch Sites Usage**
- Launches per site
- Site activity tracking
- Geographic distribution (planned)

### 4. Launch Editor

**Comprehensive Data Entry**
- **Date/Time Selection**
  - Calendar picker for dates
  - Time picker (24-hour format)
  - Launch window support (planned)

- **Site Selection**
  - Dropdown of all active sites
  - Location + Pad identification
  - Pre-populated Chinese launch sites:
    - Jiuquan (6 pads)
    - Taiyuan (3 pads)
    - Xichang (2 pads)
    - Wenchang (2 pads)
    - Historical sites

- **Rocket Selection**
  - Dropdown of all rocket types
  - Pre-populated with:
    - Long March family (LM-2, 3, 4, 6, 7, 8, 11)
    - Commercial launchers
    - Experimental vehicles
  - Includes specifications

- **Mission Details**
  - Mission name field
  - Payload name field
  - Payload mass (planned)

- **Orbit Parameters**
  - Orbit type selector (LEO, SSO, GTO, GEO, MEO, HEO, Lunar, Other)
  - Altitude (planned)
  - Inclination (planned)

- **Status Management**
  - Status dropdown (Scheduled, Go, Scrubbed, Success, Failure, Unknown, NET)
  - Success/failure tracking
  - Failure reason field (planned)

- **Additional Information**
  - Remarks text area
  - Source URL tracking (planned)
  - Last updated timestamp

### 5. Database Features

**SQLite Backend**
- Single-file database
- ACID compliance
- Concurrent access support
- Portable format

**Data Integrity**
- Foreign key constraints
- Unique constraints
- Data validation
- Timestamp tracking

**Schema Design**
```
launch_sites       - Launch facility data
rockets            - Rocket type specifications
launch_vehicles    - Specific vehicle configurations
launch_status      - Status type definitions
launches           - Main launch records
launch_tles        - Associated TLE data
launch_predictions - Predicted vs actual tracking
```

**Query Performance**
- Indexed searches
- Optimized date range queries
- Efficient month views

## Pre-populated Data

### Chinese Launch Sites (15 total)

**Jiuquan Satellite Launch Center**
- SLS-1, SLS-2 (Long March)
- LS-95, LS-96, LS-120, LS-130 (Various)
- Location: Gobi Desert, Inner Mongolia
- Coordinates: 40.96°N, 100.29°E

**Taiyuan Satellite Launch Center**
- LA-9, LA-9A (Long March)
- Mobile platform
- Location: Shanxi Province
- Coordinates: 37.85°N, 112.55°E

**Xichang Satellite Launch Center**
- LA-2, LA-3 (Long March)
- Location: Sichuan Province
- Coordinates: 28.25°N, 102.03°E

**Wenchang Space Launch Site**
- LC-101, LC-201 (Long March 5/7)
- Location: Hainan Island
- Coordinates: 19.61°N, 110.95°E

### Rocket Types (25+ configurations)

**Long March Family**
- LM-2C, 2D, 2F/G (LEO workhorses, crewed)
- LM-3B/E (GTO heavy lifter)
- LM-4B, 4C (SSO specialists)
- LM-6, 6A, 6C (Small/medium launchers)
- LM-7, 7A (Modern medium/heavy)
- LM-8 (Commercial)
- LM-11 (Solid fuel, mobile)

**Commercial Launchers**
- Ceres-1 (Galactic Energy)
- Kuaizhou-1A, 11 (CASIC)
- Gushenxing-1 (Orienspace)
- Hyperbola-1 (i-Space)
- Tianlong-2 (Landspace)
- Zhuque-2 (Landspace methane)
- Kinetica-1, Shuangquxian-1 (Space Pioneer)

**Spacecraft**
- Shenzhou (crewed)
- Tianzhou (cargo)
- ShenLong (spaceplane)

### Specifications Included
- Payload capacity (LEO/GTO)
- Height, diameter, mass
- Number of stages
- Propellant type (where applicable)
- Active/inactive status

## User Interface Features

### Menu Bar

**File Menu**
- New Launch (Ctrl+N) - Create new launch entry
- Exit (Ctrl+Q) - Close application

**View Menu**
- Refresh (F5) - Reload all data

### Keyboard Shortcuts
```
Ctrl+N  - New Launch
Ctrl+Q  - Exit Application
F5      - Refresh All Views
```

### Status Bar
- Real-time status messages
- Action confirmations
- Error notifications

### Window Management
- Resizable main window
- Minimum size: 1400x900
- Tab-based view switching
- Splitters for adjustable panels (planned)

## Data Management

### Adding Launches
1. Click "New Launch" button or Ctrl+N
2. Fill required fields (date, site, rocket)
3. Add optional details (mission, payload, orbit)
4. Select status
5. Save

### Editing Launches
1. Double-click in List View, or
2. Click day in Calendar View
3. Modify any fields
4. Save changes

### Deleting Launches
- Currently via database management (planned GUI feature)

### Searching Launches
- Type in search box (List View)
- Matches mission, payload, rocket names
- Case-insensitive
- Instant results

### Filtering
- By date range (automatic in Calendar View)
- By status (planned)
- By site (planned)
- By rocket (planned)

## Data Import/Export

### Current Capabilities
- SQLite database can be queried directly
- Compatible with standard SQL tools

### Planned Features
- CSV import/export
- Excel export
- JSON export
- PDF reports
- Web API endpoint

## Integration Features

### TAWHIRI Integration
- Shared database format
- TLE data structure
- Compatible nomenclature
- Synchronized updates

### Future Integrations (Planned)
- Space-Track.org TLE import
- Launch manifest scrapers
- Space weather data correlation
- Orbital conjunction screening
- Re-entry prediction integration

## Performance

### Optimizations
- Efficient monthly queries
- Cached rocket/site lists
- Indexed database searches
- Minimal memory footprint

### Scalability
- Handles 1000+ launches efficiently
- Fast calendar rendering
- Quick search results
- Smooth UI interactions

## Customization

### Current Options
- Database location configurable
- Window size remembers position (planned)

### Future Options (Planned)
- Custom color schemes
- Configurable table columns
- User-defined fields
- Custom reports
- Export templates

## Data Validation

### Automatic Validation
- Date format checking
- Time format validation
- Required field enforcement
- Foreign key integrity

### User Feedback
- Error messages for invalid input
- Success confirmations
- Warning dialogs
- Status bar updates

## Backup & Recovery

### Manual Backup
```bash
cp shockwave_planner.db backup_$(date +%Y%m%d).db
```

### Automatic Backup (Planned)
- Daily backups
- Configurable retention
- One-click restore

### Database Recovery
- SQLite VACUUM command
- Integrity checking
- Journal rollback

## Future Enhancements

### Version 1.1 (Planned)
- Delete launch function in GUI
- Advanced filtering options
- Column sorting in tables
- Export to Excel/CSV
- Import from CSV
- Launch window calculations

### Version 1.2 (Planned)
- TLE auto-fetch integration
- Orbital element display
- Conjunction screening
- Space weather correlation
- Launch manifest import

### Version 2.0 (Planned)
- Multi-user support
- Cloud database option
- Real-time collaboration
- Mobile companion app
- API endpoints
- Automated web scraping

## Technical Specifications

### Technology Stack
- **Language**: Python 3.9+
- **GUI**: PyQt6
- **Database**: SQLite 3
- **Architecture**: MVC pattern

### System Requirements
- **RAM**: 2GB minimum
- **Storage**: 100MB
- **Display**: 1280x720 minimum
- **OS**: Linux, macOS, Windows

### Database Size
- Empty: ~100KB
- With sample data: ~50KB
- Estimated growth: ~1KB per launch

---

**Version**: 1.0.0  
**Last Updated**: November 29, 2025  
**Author**: Remix Astronautics
