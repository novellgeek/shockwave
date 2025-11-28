# SHOCKWAVE PLANNER - Project Structure

## Directory Structure

```
shockwave_planner/
│
├── main.py                          # Application entry point
├── __init__.py                      # Package initialization
│
├── gui/                             # User Interface Layer
│   ├── __init__.py
│   └── main_window.py              # Main window with all UI components
│       ├── MainWindow              # Primary application window
│       ├── CalendarView            # Monthly calendar widget
│       ├── LaunchListView          # Searchable launch table
│       └── LaunchEditorDialog      # Launch add/edit dialog
│
├── data/                            # Data Access Layer
│   ├── __init__.py
│   └── database.py                 # SQLite database interface
│       └── LaunchDatabase          # Database operations class
│
├── resources/                       # Assets (future use)
│   ├── icons/                      # Application icons
│   └── styles/                     # Custom stylesheets
│
├── shockwave_planner.db            # SQLite database file
│
├── populate_sample_data.py         # Sample data generation script
├── start_shockwave.sh              # Quick start launcher (Linux/macOS)
│
└── Documentation
    ├── README.md                   # Overview and quick start
    ├── INSTALL.md                  # Installation guide
    └── FEATURES.md                 # Feature documentation
```

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     SHOCKWAVE PLANNER                       │
│                    Desktop Application                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │          main.py (Entry Point)        │
        │  - Initialize QApplication            │
        │  - Create MainWindow                  │
        │  - Start event loop                   │
        └───────────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│                     GUI Layer (PyQt6)                         │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              MainWindow                              │    │
│  │  - Menu bar (File, View)                            │    │
│  │  - Tab widget container                             │    │
│  │  - Action buttons                                   │    │
│  │  - Status bar                                       │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                   │
│         ┌─────────────────┼─────────────────┐               │
│         ▼                 ▼                 ▼               │
│  ┌─────────────┐   ┌─────────────┐   ┌──────────────┐     │
│  │ CalendarView│   │ ListViews   │   │ Statistics   │     │
│  │  - Monthly  │   │  - Search   │   │  - Overview  │     │
│  │    grid     │   │  - Table    │   │  - Charts    │     │
│  │  - Color    │   │  - Filter   │   │  - Reports   │     │
│  │    coded    │   │             │   │              │     │
│  └─────────────┘   └─────────────┘   └──────────────┘     │
│         │                 │                                  │
│         └─────────────────┼──────────────────┐              │
│                           ▼                  │              │
│                  ┌──────────────────┐        │              │
│                  │ LaunchEditor     │        │              │
│                  │  Dialog          │        │              │
│                  │  - Form fields   │        │              │
│                  │  - Validation    │        │              │
│                  │  - Save/Cancel   │        │              │
│                  └──────────────────┘        │              │
│                                              │              │
└──────────────────────────────────────────────┼──────────────┘
                                               │
                                               ▼
┌───────────────────────────────────────────────────────────────┐
│                    Data Layer (SQLite)                        │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │           LaunchDatabase Class                       │    │
│  │  - init_database()                                  │    │
│  │  - add_launch()                                     │    │
│  │  - update_launch()                                  │    │
│  │  - delete_launch()                                  │    │
│  │  - get_launches_by_month()                         │    │
│  │  - get_launches_by_date_range()                    │    │
│  │  - search_launches()                               │    │
│  │  - get_statistics()                                │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                   │
│                           ▼                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │        SQLite Database (shockwave_planner.db)       │    │
│  │                                                     │    │
│  │  ┌──────────────┐  ┌──────────────┐               │    │
│  │  │ launch_sites │  │   rockets    │               │    │
│  │  │  - site_id   │  │  - rocket_id │               │    │
│  │  │  - location  │  │  - name      │               │    │
│  │  │  - pad       │  │  - family    │               │    │
│  │  │  - lat/lon   │  │  - specs     │               │    │
│  │  └──────────────┘  └──────────────┘               │    │
│  │                                                     │    │
│  │  ┌──────────────┐  ┌──────────────┐               │    │
│  │  │launch_status │  │   launches   │               │    │
│  │  │  - status_id │  │  - launch_id │               │    │
│  │  │  - name      │  │  - date/time │               │    │
│  │  │  - color     │  │  - site_id   │               │    │
│  │  └──────────────┘  │  - rocket_id │               │    │
│  │                    │  - mission   │               │    │
│  │  ┌──────────────┐  │  - payload   │               │    │
│  │  │ launch_tles  │  │  - orbit     │               │    │
│  │  │  - tle_id    │  │  - status_id │               │    │
│  │  │  - launch_id │  │  - remarks   │               │    │
│  │  │  - norad_id  │  └──────────────┘               │    │
│  │  │  - tle_lines │                                 │    │
│  │  └──────────────┘                                 │    │
│  │                                                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Data Flow

### Adding a New Launch

```
User Action (GUI)
    │
    ├─> Click "New Launch" button
    │
    ▼
LaunchEditorDialog opens
    │
    ├─> User fills form fields
    │   - Date/Time pickers
    │   - Site dropdown
    │   - Rocket dropdown
    │   - Mission text fields
    │   - Orbit selector
    │   - Status selector
    │
    ├─> Click "Save"
    │
    ▼
Data Validation
    │
    ├─> Check required fields
    ├─> Validate date/time formats
    ├─> Verify foreign keys exist
    │
    ▼
LaunchDatabase.add_launch()
    │
    ├─> Build INSERT SQL
    ├─> Execute query
    ├─> Commit transaction
    ├─> Return launch_id
    │
    ▼
SQLite Database
    │
    ├─> Store in launches table
    ├─> Update indexes
    ├─> Set timestamp
    │
    ▼
UI Refresh
    │
    ├─> Close dialog
    ├─> Refresh calendar view
    ├─> Refresh list view
    ├─> Show success message
    │
    ▼
Display Updated
```

### Searching for Launches

```
User Input (GUI)
    │
    ├─> Type in search box
    │
    ▼
Real-time Search
    │
    ├─> textChanged signal
    │
    ▼
LaunchDatabase.search_launches(term)
    │
    ├─> Build LIKE query
    ├─> Search mission_name
    ├─> Search payload_name
    ├─> Search rocket name
    ├─> JOIN related tables
    │
    ▼
SQLite Query Execution
    │
    ├─> Full-text search
    ├─> Case-insensitive matching
    ├─> Return matching rows
    │
    ▼
Results Display
    │
    ├─> Update table widget
    ├─> Populate rows
    ├─> Apply color coding
    │
    ▼
User Sees Results
```

### Monthly Calendar Update

```
User Navigation
    │
    ├─> Click Previous/Next month
    │
    ▼
Update Month Variables
    │
    ├─> Increment/decrement month
    ├─> Handle year rollover
    │
    ▼
LaunchDatabase.get_launches_by_month(year, month)
    │
    ├─> Build date range query
    ├─> Filter by YYYY-MM
    ├─> JOIN all related tables
    ├─> ORDER BY date, time
    │
    ▼
Build Calendar Grid
    │
    ├─> Calculate month calendar
    ├─> Create table rows/columns
    ├─> Map days to cells
    │
    ▼
Populate Launch Data
    │
    ├─> For each day:
    │   ├─> Find matching launches
    │   ├─> Format display text
    │   ├─> Apply status colors
    │   └─> Add to cell
    │
    ▼
Render Calendar
    │
    ├─> Update table widget
    ├─> Adjust row heights
    ├─> Show month/year label
    │
    ▼
Display to User
```

## Database Schema Relationships

```
launch_sites (1) ─────── (*) launches
    │                         │
    │                         │
    site_id ←────────── site_id
                             
rockets (1) ──────────── (*) launches
    │                         │
    │                         │
    rocket_id ←────────── rocket_id

launch_status (1) ───── (*) launches
    │                         │
    │                         │
    status_id ←────────── status_id

launches (1) ─────────── (*) launch_tles
    │                         │
    │                         │
    launch_id ←────────── launch_id

launches (1) ─────────── (*) launch_predictions
    │                         │
    │                         │
    launch_id ←────────── launch_id
```

## Module Dependencies

```
main.py
  └─> gui/main_window.py
        ├─> PyQt6.QtWidgets
        ├─> PyQt6.QtCore
        ├─> PyQt6.QtGui
        └─> data/database.py
              └─> sqlite3
```

## Event Flow

```
Application Startup
  │
  ├─> Initialize QApplication
  ├─> Set application metadata
  ├─> Apply Fusion style
  │
  ├─> Create MainWindow
  │     ├─> Initialize database
  │     ├─> Build menu bar
  │     ├─> Create tab widget
  │     ├─> Create CalendarView
  │     ├─> Create ListViews
  │     ├─> Create Statistics
  │     └─> Connect signals
  │
  ├─> Show window
  └─> Start event loop (app.exec())

User Interactions
  │
  ├─> Menu actions → Trigger handlers
  ├─> Button clicks → Execute functions
  ├─> Table selections → Emit signals
  ├─> Dialog inputs → Update database
  └─> Tab switches → Refresh views

Background Operations
  │
  ├─> Database queries (synchronous)
  ├─> UI updates (event-driven)
  └─> Signal/slot connections
```

## Signal/Slot Architecture

```
CalendarView.launch_selected
  └─> MainWindow.edit_launch()
        └─> LaunchEditorDialog.exec()
              └─> LaunchDatabase.update_launch()

ListViews.launch_selected
  └─> MainWindow.edit_launch()

LaunchEditorDialog.accepted
  └─> MainWindow.refresh_all()
        ├─> CalendarView.update_calendar()
        └─> ListViews.load_launches()
```

---

**Last Updated**: November 29, 2025  
**Version**: 1.0.0
