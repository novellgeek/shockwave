# SHOCKWAVE PLANNER v1.1

**Desktop Launch Operations Planning System**

## What's New in v1.1

### 🎯 Major Features

1. **Timeline/Gantt View**
   - Horizontal timeline showing launches across the month
   - Grouped by country (China, USA, Russia, Europe, Pacific, etc.)
   - Collapsible country groups (▶/▼)
   - Pad turnaround visualization (grey bars after launches)
   - Show only active sites option

2. **Enhanced List View with Date Filters**
   - **Previous 7 Days** - Last week's launches
   - **Previous 30 Days** - Last month's launches
   - **Current (Today)** - Today's launches only
   - **Next 30 Days** - Upcoming month
   - **Custom Range** - Pick any date range

3. **NOTAM Field**
   - Track Notice to Airmen references
   - Searchable in list view
   - Highlighted when present
   - Foundation for future NOTAM mapping

4. **Space Devs Integration Ready**
   - API importer included
   - Automatic launch data import
   - Chinese launch filtering
   - Rate limiting built-in

## Quick Start

```bash
# Install PyQt6 (if not already installed)
pip install PyQt6 --break-system-packages

# Run the application
python3 main.py
```

## Features

### Timeline View
- **Monthly calendar** with horizontal day layout
- **Country grouping** - click to expand/collapse
- **Color-coded status** - Yellow (Scheduled), Green (Success), etc.
- **Pad turnaround** - Grey bars show unavailable days
- **Smart filtering** - Hide sites without launches

### List View
- **Quick date filters** - Previous 7/30, Current, Next 30 days
- **Custom date range** - Pick any start/end dates
- **NOTAM tracking** - Yellow highlight for launches with NOTAMs
- **Real-time search** - Search mission, payload, rocket, NOTAM
- **Status display** - Shows X launches in current filter

### Launch Editor
- All fields from v1.0
- **NEW: NOTAM Reference** field
- Easy dropdown selection
- Date/time pickers
- Auto-save with validation

## Database Schema Changes

New fields in v1.1:
```sql
ALTER TABLE launches ADD COLUMN notam_reference TEXT;
ALTER TABLE launches ADD COLUMN data_source TEXT DEFAULT 'Manual';
ALTER TABLE launches ADD COLUMN external_id TEXT;
ALTER TABLE launches ADD COLUMN last_synced DATETIME;
```

## File Structure

```
shockwave_v1.1/
├── main.py                    # Application entry point
├── gui/
│   ├── main_window.py         # Main window with tabs
│   ├── timeline_view.py       # NEW - Gantt-style timeline
│   └── enhanced_list_view.py  # NEW - Enhanced with date filters
├── data/
│   ├── database.py            # Database layer (updated schema)
│   └── spacedevs_import.py    # Space Devs API importer
├── shockwave_planner.db       # SQLite database (updated)
└── populate_sample_data.py    # Sample data generator
```

## Keyboard Shortcuts

- `Ctrl+N` - New Launch
- `Ctrl+Q` - Exit
- `F5` - Refresh All Views

## Space Devs Integration

The Space Devs importer is included but not yet integrated into the UI.

To use it now:
```python
from data.database import LaunchDatabase
from data.spacedevs_import import SpaceDevsImporter

db = LaunchDatabase('shockwave_planner.db')
importer = SpaceDevsImporter(db)

# Import Chinese launches for December
launches = importer.fetch_chinese_launches('2025-12-01', '2025-12-31')
stats = importer.import_batch(launches)

print(f"Imported {stats['imported']} launches")
```

## Migration from v1.0

v1.1 is **fully backward compatible** with v1.0:
- Same database file works
- All v1.0 data preserved
- New fields added automatically
- No data migration needed

Simply run v1.1 with your existing database!

## Future Roadmap

### v1.1.1 - Space Devs UI
- Import dialog in GUI
- Scheduled auto-sync
- Data source tracking

### v1.1.2 - NOTAM Database
- Full NOTAM tracking tables
- Multiple NOTAMs per launch
- Geometry support

### v1.1.3 - NOTAM Mapping
- Interactive map visualization
- 2-day countdown view
- Airspace conflict detection

## Support

For questions or issues, contact Remix Astronautics.

---

**Version**: 1.1.0  
**Date**: November 29, 2025  
**Author**: Remix Astronautics
