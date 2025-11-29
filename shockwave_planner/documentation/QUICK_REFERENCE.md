# SHOCKWAVE PLANNER - Quick Reference

## Installation (1 Minute)

```bash
pip install PyQt6 --break-system-packages
cd shockwave_planner
python3 main.py
```

## Interface Overview

```
┌─────────────────────────────────────────────────────────────┐
│ File  View                         SHOCKWAVE PLANNER v1.0   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────┬──────────────┬──────────────┐              │
│  │ Calendar   │  List View   │  Statistics  │ ◄── Tabs    │
│  └────────────┴──────────────┴──────────────┘              │
│                                                             │
│  ┌───────────────────────────────────────────────────┐     │
│  │  ◀ Previous   November 2025          Next ▶       │     │
│  ├───┬───┬───┬───┬───┬───┬───────────────────────────┤     │
│  │Mon│Tue│Wed│Thu│Fri│Sat│Sun                        │     │
│  ├───┼───┼───┼───┼───┼───┼───┬───┬───┬───┬───┬───┬───┤     │
│  │   │   │   │   │   │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │     │
│  │   │   │   │   │   │   │   │   │   │03:│   │   │   │     │
│  │   │   │   │   │   │   │   │   │   │12 │   │   │   │     │
│  │   │   │   │   │   │   │   │   │   │Kin│   │   │   │     │
│  │   │   │   │   │   │   │   │   │   │eti│   │   │   │     │
│  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤     │
│  │ 9 │10 │11 │12 │13 │14 │15 │16 │17 │18 │19 │20 │21 │     │
│  │   │   │   │   │06:│   │   │   │   │   │   │   │   │     │
│  │   │   │   │   │50 │   │   │   │   │   │   │   │   │     │
│  │   │   │   │   │LM-│   │   │   │   │   │   │   │   │     │
│  │   │   │   │   │6C │   │   │   │   │   │   │   │   │     │
│  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘     │
│                                                             │
│  [➕ New Launch]  [🔄 Refresh]                              │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ Ready                                                        │
└─────────────────────────────────────────────────────────────┘
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New Launch |
| `Ctrl+Q` | Exit |
| `F5` | Refresh All Views |

## Status Colors

| Color | Meaning |
|-------|---------|
| 🟨 Yellow | Scheduled |
| 🟩 Green | Go (confirmed) |
| 🟧 Orange | Scrubbed/Delayed |
| 🟩 Dark Green | Success |
| 🟥 Red | Failure |
| ⬜ Gray | Unknown |
| 🟧 Light Orange | NET (No Earlier Than) |

## Common Tasks

### Add a New Launch
1. Click **➕ New Launch** (or `Ctrl+N`)
2. Select **Date** from calendar picker
3. Enter **Time** (HH:MM:SS)
4. Choose **Launch Site** from dropdown
5. Select **Rocket** type
6. Enter **Mission Name**
7. Enter **Payload Name**
8. Select **Orbit Type** (LEO, SSO, GTO, etc.)
9. Choose **Status**
10. Add **Remarks** (optional)
11. Click **Save**

### Edit Existing Launch
**From Calendar View:**
- Click on the day containing the launch

**From List View:**
- Double-click the launch row

**Then:**
- Modify any fields
- Click **Save**

### Search for Launches
1. Go to **List View** tab
2. Type in the search box
3. Results filter automatically
4. Search matches: mission names, payloads, rocket types

### Navigate Calendar
- Click **◀ Previous** to go back one month
- Click **Next ▶** to advance one month
- Click any day to view launches

### View Statistics
1. Click **Statistics** tab
2. View overview, top rockets, site usage

## Pre-loaded Data

### Launch Sites (15 total)
- **Jiuquan**: SLS-1, SLS-2, LS-95, LS-96, LS-120, LS-130
- **Taiyuan**: LA-9, LA-9A, Mobile
- **Xichang**: LA-2, LA-3
- **Wenchang**: LC-101, LC-201

### Rockets (25+ types)
- Long March 2C, 2D, 2F/G
- Long March 3B/E
- Long March 4B, 4C
- Long March 6, 6A, 6C
- Long March 7, 7A, 8, 11
- Ceres-1, Kuaizhou-1A/11
- Tianlong-2, Zhuque-2
- Kinetica-1, Hyperbola-1
- More...

## File Locations

```
shockwave_planner/
├── main.py                   ← Start here
├── shockwave_planner.db     ← Your data
├── start_shockwave.sh       ← Quick launcher
└── populate_sample_data.py  ← Reset sample data
```

## Database Management

### Backup
```bash
cp shockwave_planner.db backup_$(date +%Y%m%d).db
```

### Reset to Samples
```bash
rm shockwave_planner.db
python3 populate_sample_data.py
```

### Check Database
```bash
sqlite3 shockwave_planner.db "SELECT COUNT(*) FROM launches;"
```

## Troubleshooting

### Won't Start?
```bash
# Check Python
python3 --version  # Need 3.9+

# Install PyQt6
pip install PyQt6 --break-system-packages

# Run from correct directory
cd shockwave_planner
python3 main.py
```

### Database Locked?
```bash
# Close all instances, then:
rm shockwave_planner.db-journal
```

### Need Fresh Start?
```bash
# Backup first!
cp shockwave_planner.db backup.db

# Remove and restart
rm shockwave_planner.db
python3 main.py

# Repopulate samples
python3 populate_sample_data.py
```

## Integration with TAWHIRI

### Same Database
Point both apps to same `.db` file:
```python
# In TAWHIRI config
db_path = "/path/to/shockwave_planner.db"
```

### Export Data
```bash
sqlite3 shockwave_planner.db ".dump launches" > launches.sql
```

### Query from Code
```python
import sqlite3
conn = sqlite3.connect('shockwave_planner.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM launches WHERE launch_date >= '2025-11-01'")
launches = cursor.fetchall()
```

## Sample Data Included

```
November 2025:
  05 Nov - Tianqi-27 (Kinetica-1) - Success
  13 Nov - Gaofen-12E (LM-6C) - Success
  22 Nov - Tianhui-6B (LM-2C) - Scheduled
  26 Nov - Beidou-3 M26 (LM-3B/E) - Go
  28 Nov - Jilin-1 GF06 (Ceres-1) - NET

December 2025:
  05 Dec - Tianzhou-9 (LM-7) - Scheduled
  12 Dec - Yaogan-41 (LM-4C) - Scheduled
  18 Dec - Shenzhou-20 (LM-2F/G) - NET
```

## Tips

✅ Keep the app open during operations  
✅ Update status as launches occur  
✅ Use remarks field for detailed notes  
✅ Backup database before major changes  
✅ Search is case-insensitive  
✅ Calendar shows up to current month + future  
✅ Double-click launches to edit quickly  

## Need More Help?

- **README.md** - Getting started guide
- **INSTALL.md** - Detailed installation
- **FEATURES.md** - Complete feature list
- **ARCHITECTURE.md** - Technical details
- **PROJECT_SUMMARY.md** - Overview

---

**SHOCKWAVE PLANNER v1.0**  
Remix Astronautics - November 2025
