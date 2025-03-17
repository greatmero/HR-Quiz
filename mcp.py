import sys
import psutil
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QLabel, QProgressBar, QTableWidget, QTableWidgetItem)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor

class MCP(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Master Control Program")
        self.setMinimumSize(800, 600)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow { background-color: #1a1a1a; }
            QLabel { color: #00ff00; }
            QTableWidget { 
                background-color: #2a2a2a;
                color: #00ff00;
                gridline-color: #404040;
            }
            QHeaderView::section {
                background-color: #404040;
                color: #00ff00;
                padding: 5px;
            }
            QProgressBar {
                border: 2px solid #404040;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #00ff00;
            }
        """)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create header
        header = QLabel("MASTER CONTROL PROGRAM")
        header.setFont(QFont("Courier", 20, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # System status
        self.status_label = QLabel("System Status: OPERATIONAL")
        self.status_label.setFont(QFont("Courier", 12))
        layout.addWidget(self.status_label)

        # CPU Usage
        self.cpu_label = QLabel("CPU Usage:")
        self.cpu_bar = QProgressBar()
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_bar)

        # Memory Usage
        self.memory_label = QLabel("Memory Usage:")
        self.memory_bar = QProgressBar()
        layout.addWidget(self.memory_label)
        layout.addWidget(self.memory_bar)

        # Process Table
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(4)
        self.process_table.setHorizontalHeaderLabels(["PID", "Name", "CPU %", "Memory %"])
        layout.addWidget(self.process_table)

        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(2000)  # Update every 2 seconds

        self.update_stats()

    def update_stats(self):
        # Update CPU usage
        cpu_percent = psutil.cpu_percent()
        self.cpu_bar.setValue(int(cpu_percent))
        self.cpu_label.setText(f"CPU Usage: {cpu_percent:.1f}%")

        # Update memory usage
        memory = psutil.virtual_memory()
        self.memory_bar.setValue(int(memory.percent))
        self.memory_label.setText(f"Memory Usage: {memory.percent:.1f}%")

        # Update process table
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # Sort by CPU usage
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
        
        # Display top 10 processes
        self.process_table.setRowCount(min(10, len(processes)))
        for i, proc in enumerate(processes[:10]):
            self.process_table.setItem(i, 0, QTableWidgetItem(str(proc['pid'])))
            self.process_table.setItem(i, 1, QTableWidgetItem(proc['name']))
            self.process_table.setItem(i, 2, QTableWidgetItem(f"{proc.get('cpu_percent', 0):.1f}%"))
            self.process_table.setItem(i, 3, QTableWidgetItem(f"{proc.get('memory_percent', 0):.1f}%"))

        self.process_table.resizeColumnsToContents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mcp = MCP()
    mcp.show()
    sys.exit(app.exec())
