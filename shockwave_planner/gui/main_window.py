"""
SHOCKWAVE PLANNER v1.1 - Main Window
Enhanced with Timeline View, Date Filters, and NOTAM support
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel, QTabWidget, QGroupBox,
                              QDialog, QFormLayout, QDialogButtonBox, QLineEdit,
                              QComboBox, QDateEdit, QTimeEdit, QTextEdit,
                              QMessageBox)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QAction, QFont
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.database import LaunchDatabase
from gui.timeline_view import TimelineView
from gui.enhanced_list_view import EnhancedListView


class LaunchEditorDialog(QDialog):
    """Dialog for adding/editing launch records with NOTAM support"""
    
    def __init__(self, db: LaunchDatabase, launch_id: int = None, parent=None):
        super().__init__(parent)
        self.db = db
        self.launch_id = launch_id
        self.init_ui()
        
        if launch_id:
            self.load_launch_data()
    
    def init_ui(self):
        self.setWindowTitle("Launch Editor" if not self.launch_id else "Edit Launch")
        self.setMinimumWidth(600)
        
        layout = QFormLayout()
        
        # Date and Time
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        layout.addRow("Launch Date:", self.date_edit)
        
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm:ss")
        layout.addRow("Launch Time:", self.time_edit)
        
        # Launch Site
        self.site_combo = QComboBox()
        sites = self.db.get_all_sites()
        for site in sites:
            self.site_combo.addItem(f"{site['location']} - {site['launch_pad']}", site['site_id'])
        layout.addRow("Launch Site:", self.site_combo)
        
        # Rocket
        self.rocket_combo = QComboBox()
        rockets = self.db.get_all_rockets()
        for rocket in rockets:
            self.rocket_combo.addItem(rocket['name'], rocket['rocket_id'])
        layout.addRow("Rocket:", self.rocket_combo)
        
        # Mission Details
        self.mission_edit = QLineEdit()
        layout.addRow("Mission Name:", self.mission_edit)
        
        self.payload_edit = QLineEdit()
        layout.addRow("Payload:", self.payload_edit)
        
        # Orbit
        self.orbit_combo = QComboBox()
        self.orbit_combo.addItems(['LEO', 'SSO', 'GTO', 'GEO', 'MEO', 'HEO', 'Lunar', 'Other'])
        layout.addRow("Orbit Type:", self.orbit_combo)
        
        # NOTAM - NEW in v1.1
        self.notam_edit = QLineEdit()
        self.notam_edit.setPlaceholderText("e.g., A1234/25")
        layout.addRow("NOTAM Reference:", self.notam_edit)
        
        # Status
        self.status_combo = QComboBox()
        statuses = self.db.get_all_statuses()
        for status in statuses:
            self.status_combo.addItem(status['status_name'], status['status_id'])
        layout.addRow("Status:", self.status_combo)
        
        # Remarks
        self.remarks_edit = QTextEdit()
        self.remarks_edit.setMaximumHeight(100)
        layout.addRow("Remarks:", self.remarks_edit)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.save_launch)
        button_box.rejected.connect(self.reject)
        
        layout.addRow(button_box)
        self.setLayout(layout)
    
    def load_launch_data(self):
        """Load existing launch data"""
        launches = self.db.get_launches_by_date_range('1900-01-01', '2100-01-01')
        launch = next((l for l in launches if l['launch_id'] == self.launch_id), None)
        
        if launch:
            if launch['launch_date']:
                date_obj = datetime.strptime(launch['launch_date'], '%Y-%m-%d')
                self.date_edit.setDate(QDate(date_obj.year, date_obj.month, date_obj.day))
            
            if launch['launch_time']:
                time_obj = datetime.strptime(launch['launch_time'], '%H:%M:%S').time()
                self.time_edit.setTime(QTime(time_obj.hour, time_obj.minute, time_obj.second))
            
            if launch['site_id']:
                index = self.site_combo.findData(launch['site_id'])
                if index >= 0:
                    self.site_combo.setCurrentIndex(index)
            
            if launch['rocket_id']:
                index = self.rocket_combo.findData(launch['rocket_id'])
                if index >= 0:
                    self.rocket_combo.setCurrentIndex(index)
            
            if launch['status_id']:
                index = self.status_combo.findData(launch['status_id'])
                if index >= 0:
                    self.status_combo.setCurrentIndex(index)
            
            self.mission_edit.setText(launch.get('mission_name') or '')
            self.payload_edit.setText(launch.get('payload_name') or '')
            self.notam_edit.setText(launch.get('notam_reference') or '')
            
            if launch.get('orbit_type'):
                index = self.orbit_combo.findText(launch['orbit_type'])
                if index >= 0:
                    self.orbit_combo.setCurrentIndex(index)
            
            self.remarks_edit.setPlainText(launch.get('remarks') or '')
    
    def save_launch(self):
        """Save launch data"""
        launch_data = {
            'launch_date': self.date_edit.date().toString('yyyy-MM-dd'),
            'launch_time': self.time_edit.time().toString('HH:mm:ss'),
            'site_id': self.site_combo.currentData(),
            'rocket_id': self.rocket_combo.currentData(),
            'mission_name': self.mission_edit.text(),
            'payload_name': self.payload_edit.text(),
            'orbit_type': self.orbit_combo.currentText(),
            'status_id': self.status_combo.currentData(),
            'notam_reference': self.notam_edit.text(),
            'remarks': self.remarks_edit.toPlainText()
        }
        
        if self.launch_id:
            self.db.update_launch(self.launch_id, launch_data)
        else:
            self.db.add_launch(launch_data)
        
        self.accept()


class MainWindow(QMainWindow):
    """Main application window for SHOCKWAVE PLANNER v1.1"""
    
    def __init__(self):
        super().__init__()
        self.db = LaunchDatabase()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("SHOCKWAVE PLANNER v1.1 - Launch Operations Planning")
        self.setGeometry(100, 100, 1600, 900)
        
        # Menu bar
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        new_launch_action = QAction('New Launch', self)
        new_launch_action.setShortcut('Ctrl+N')
        new_launch_action.triggered.connect(self.new_launch)
        file_menu.addAction(new_launch_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        refresh_action = QAction('Refresh', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.refresh_all)
        view_menu.addAction(refresh_action)
        
        launch_site_action = QAction('Launch Site', self)
        launch_site_action.triggered.connect(self.open_launch_site_window)
        view_menu.addAction(launch_site_action)

        launch_vehicle_action = QAction('Launch Vehicle', self)
        launch_vehicle_action.triggered.connect(self.open_launch_vehicle_window)
        view_menu.addAction(launch_vehicle_action)


        reentry_vehicle_action = QAction('Re-entry Vehicle', self)
        reentry_vehicle_action.triggered.connect(self.open_reentry_vehicle_window)
        view_menu.addAction(reentry_vehicle_action)


        support_ship_action = QAction('Support Ship', self)
        support_ship_action.triggered.connect(self.open_support_ship_window)
        view_menu.addAction(support_ship_action)
      
        # Data menu (for future Space Devs integration)
        data_menu = menubar.addMenu('Data')
        import_action = QAction('Import from Space Devs... (Coming Soon)', self)
        import_action.setEnabled(False)
        data_menu.addAction(import_action)
        
        file_menu.addSeparator()

        import_action = QAction('Manual Edit (Coming Soon)', self)
        import_action.setEnabled(False)
        data_menu.addAction(import_action)

        file_menu.addSeparator()

        import_action = QAction('Database Admin (Coming Soon)', self)
        import_action.setEnabled(False)
        data_menu.addAction(import_action)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Timeline view - NEW in v1.1
        self.timeline_view = TimelineView(self.db)
        self.timeline_view.launch_selected.connect(self.edit_launch)
        self.tab_widget.addTab(self.timeline_view, "Timeline View")
        
        # Enhanced List view - Updated in v1.1
        self.list_view = EnhancedListView(self.db)
        self.list_view.launch_selected.connect(self.edit_launch)
        self.tab_widget.addTab(self.list_view, "List View")
        
        # Statistics view
        stats_widget = self.create_statistics_widget()
        self.tab_widget.addTab(stats_widget, "Statistics")
        
        main_layout.addWidget(self.tab_widget)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        new_btn = QPushButton("➕ New Launch")
        new_btn.clicked.connect(self.new_launch)
        button_layout.addWidget(new_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_all)
        button_layout.addWidget(refresh_btn)
        
        button_layout.addStretch()
        
        # Version label
        version_label = QLabel("v1.1")
        version_label.setStyleSheet("color: gray;")
        button_layout.addWidget(version_label)
        
        main_layout.addLayout(button_layout)
        
        central_widget.setLayout(main_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready - SHOCKWAVE PLANNER v1.1")
    
    def create_statistics_widget(self):
        """Create statistics display"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        stats = self.db.get_statistics()
        
        overview_group = QGroupBox("Overview")
        overview_layout = QFormLayout()
        overview_layout.addRow("Total Launches:", QLabel(str(stats['total_launches'])))
        overview_layout.addRow("Successful:", QLabel(str(stats['successful'])))
        overview_layout.addRow("Failed:", QLabel(str(stats['failed'])))
        overview_layout.addRow("Pending:", QLabel(str(stats['pending'])))
        
        success_rate = 0
        if stats['successful'] + stats['failed'] > 0:
            success_rate = (stats['successful'] / (stats['successful'] + stats['failed'])) * 100
        overview_layout.addRow("Success Rate:", QLabel(f"{success_rate:.1f}%"))
        
        overview_group.setLayout(overview_layout)
        layout.addWidget(overview_group)
        
        rockets_group = QGroupBox("Top 10 Rockets")
        rockets_layout = QVBoxLayout()
        rockets_text = QTextEdit()
        rockets_text.setReadOnly(True)
        rocket_stats = "\n".join([f"{r['name']}: {r['count']} launches" 
                                 for r in stats['by_rocket']])
        rockets_text.setPlainText(rocket_stats)
        rockets_layout.addWidget(rockets_text)
        rockets_group.setLayout(rockets_layout)
        layout.addWidget(rockets_group)
        
        sites_group = QGroupBox("Launches by Site")
        sites_layout = QVBoxLayout()
        sites_text = QTextEdit()
        sites_text.setReadOnly(True)
        site_stats = "\n".join([f"{s['location']}: {s['count']} launches" 
                               for s in stats['by_site']])
        sites_text.setPlainText(site_stats)
        sites_layout.addWidget(sites_text)
        sites_group.setLayout(sites_layout)
        layout.addWidget(sites_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        
        return widget
    
    def new_launch(self):
        """Create new launch"""
        dialog = LaunchEditorDialog(self.db, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_all()
            self.statusBar().showMessage("Launch added successfully", 3000)
    
    def edit_launch(self, launch_id: int):
        """Edit existing launch"""
        dialog = LaunchEditorDialog(self.db, launch_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_all()
            self.statusBar().showMessage("Launch updated successfully", 3000)
    
    def refresh_all(self):
        """Refresh all views"""
        self.timeline_view.update_timeline()
        self.list_view.refresh()
        
        # Recreate statistics tab
        stats_widget = self.create_statistics_widget()
        self.tab_widget.removeTab(2)
        self.tab_widget.insertTab(2, stats_widget, "Statistics")
        
        self.statusBar().showMessage("Refreshed", 2000)
    
    def closeEvent(self, event):
        """Handle window close"""
        self.db.close()
        event.accept()

    def open_launch_site_window(self):
        print("Launch Site menu clicked — add your window here")

    def open_launch_vehicle_window(self):
        print("Launch Vehicle menu clicked — add your window here")

    def open_reentry_vehicle_window(self):
        print("Re-entry Vehicle menu clicked — add your window here")

    def open_support_ship_window(self):
        print("Support Ship menu clicked — add your window here")
