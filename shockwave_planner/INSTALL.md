# SHOCKWAVE PLANNER - Installation & Setup Guide

## System Requirements

### Minimum Requirements
- **OS**: Linux, macOS, or Windows
- **Python**: 3.9 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 100MB for application + database
- **Display**: 1280x720 minimum resolution

### Recommended Setup
- **OS**: Ubuntu 22.04+ / macOS 12+ / Windows 10+
- **Python**: 3.11+
- **RAM**: 8GB
- **Storage**: 500MB (allows for growth)
- **Display**: 1920x1080 or higher

## Installation

### Step 1: Verify Python Installation

Open a terminal/command prompt and run:
```bash
python3 --version
```

You should see Python 3.9 or higher. If not, install Python from:
- Linux: `sudo apt install python3 python3-pip`
- macOS: Download from python.org or use Homebrew: `brew install python3`
- Windows: Download from python.org

### Step 2: Install PyQt6

```bash
pip install PyQt6
```

Or on Linux with system restrictions:
```bash
pip install PyQt6 --break-system-packages
```

### Step 3: Extract Application

Extract the shockwave_planner directory to your desired location:
```bash
# Example for Linux/macOS
cd ~/Documents
unzip shockwave_planner.zip

# Or if you have the directory already
cd path/to/shockwave_planner
```

### Step 4: Verify Installation

```bash
cd shockwave_planner
ls -la
```

You should see:
- `main.py` - Main application file
- `gui/` - GUI components
- `data/` - Database layer
- `README.md` - Documentation
- `shockwave_planner.db` - SQLite database (with sample data)

## Running the Application

### Method 1: Quick Start Script (Linux/macOS)

```bash
./start_shockwave.sh
```

### Method 2: Direct Python Execution

```bash
python3 main.py
```

### Method 3: From Anywhere (Linux/macOS)

Create an alias in your `.bashrc` or `.zshrc`:
```bash
alias shockwave='cd /path/to/shockwave_planner && python3 main.py'
```

Then just run:
```bash
shockwave
```

## First-Time Setup

### 1. Launch the Application
The application comes pre-populated with:
- Chinese launch sites (Jiuquan, Taiyuan, Xichang, Wenchang)
- Common rocket types (Long March series, commercial launchers)
- Sample launches for November-December 2025

### 2. Explore the Interface

**Calendar View Tab**:
- Shows launches in a monthly calendar format
- Color-coded by status
- Navigate with Previous/Next buttons
- Click on days to view/edit launches

**List View Tab**:
- Searchable table of all launches
- Double-click to edit
- Search by mission, payload, or rocket type

**Statistics Tab**:
- Overview of launch statistics
- Success rates
- Top rockets and launch sites

### 3. Add Your First Launch

1. Click "➕ New Launch" button (or press Ctrl+N)
2. Fill in the form:
   - **Launch Date**: Select from calendar
   - **Launch Time**: Enter time (24-hour format)
   - **Launch Site**: Choose from dropdown
   - **Rocket**: Select rocket type
   - **Mission Name**: Enter mission designation
   - **Payload**: Satellite or spacecraft name
   - **Orbit Type**: LEO, SSO, GTO, etc.
   - **Status**: Scheduled, Go, Success, etc.
   - **Remarks**: Optional notes
3. Click "Save"

## Database Management

### Backup Database

The database is stored in `shockwave_planner.db`. To backup:

```bash
# Create backup with timestamp
cp shockwave_planner.db shockwave_planner_backup_$(date +%Y%m%d).db
```

### Reset to Sample Data

If you want to start fresh with sample data:

```bash
# Backup current database first!
cp shockwave_planner.db shockwave_planner_backup.db

# Remove current database
rm shockwave_planner.db

# Re-populate with sample data
python3 populate_sample_data.py

# Restart application
python3 main.py
```

### Database Location

By default, the database is created in the application directory. To use a different location, modify the database path in `gui/main_window.py`:

```python
# Change this line in MainWindow.__init__
self.db = LaunchDatabase("/path/to/your/database.db")
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'PyQt6'"

Solution:
```bash
pip install PyQt6 --break-system-packages
```

### Application Window is Too Small/Large

The application uses system DPI settings. To adjust:
- **Windows**: Change display scaling in Settings
- **Linux**: Adjust Qt scaling environment variable:
  ```bash
  export QT_SCALE_FACTOR=1.5
  python3 main.py
  ```
- **macOS**: Use system display preferences

### Database is Locked

If you see "database is locked" errors:
1. Close all instances of SHOCKWAVE PLANNER
2. Wait a few seconds
3. Restart the application

If the problem persists:
```bash
# Check for lock file
ls -la shockwave_planner.db*

# Remove lock file if it exists
rm shockwave_planner.db-journal
```

### Application Won't Start

1. Check Python version: `python3 --version`
2. Verify PyQt6 installation: `python3 -c "import PyQt6; print('OK')"`
3. Check for error messages in terminal
4. Ensure you're in the correct directory: `pwd`

### Missing Sample Data

If the database has no launch sites or rockets:

```bash
python3 populate_sample_data.py
```

## Advanced Configuration

### Custom Launch Sites

To add custom launch sites, edit the database directly or use the GUI (planned feature).

### Integration with TAWHIRI

SHOCKWAVE PLANNER shares the same database format as TAWHIRI. To integrate:

1. Use the same database file for both applications
2. Set the database path to point to your TAWHIRI database
3. Both systems can read/write simultaneously (SQLite handles concurrency)

### Export Data

Currently, data export is via direct database queries. Future versions will include:
- Excel export
- CSV export
- PDF reports
- JSON API

## Getting Help

### Common Tasks

**View all launches for a specific month**:
- Use Calendar View tab
- Navigate to desired month with Previous/Next

**Search for a specific mission**:
- Go to List View tab
- Type mission name in search box

**Update launch status**:
- Double-click launch in List View
- Or click day in Calendar View
- Change status dropdown
- Click Save

**View statistics**:
- Click Statistics tab
- View success rates and trends

### Log Files

Application logs are printed to the terminal. To save logs:

```bash
python3 main.py 2>&1 | tee shockwave_planner.log
```

## Next Steps

1. Explore the sample data
2. Add real launch data from your sources
3. Customize rocket and site lists as needed
4. Set up regular backups
5. Integrate with TAWHIRI if applicable

## Support

For technical support or feature requests, contact Remix Astronautics.

---

**Last Updated**: November 29, 2025
**Version**: 1.0.0
