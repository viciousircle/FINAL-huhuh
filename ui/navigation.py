from typing import Callable, Optional, Any
from datetime import datetime


from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QPushButton, QMessageBox, QComboBox, QLabel, QListWidget, QStackedWidget, QWidget, QLineEdit
from PyQt6 import uic
from PyQt6 import QtCore
from PyQt6.QtCore import QDate

import sys
from pathlib import Path
import os

# Ensure the project root is in the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_session import DBSession
from lms_types import UsersAccountData, UsersHistoryData, UsersGuestData, BooksBookMarcData, BooksBookData, ExecuteResult

class Navigation_UI:
    def __init__(self, ui, db_session: DBSession):
        self.ui = ui
        self.db_session = db_session
        
        self.buttons_nav = [
            self.ui.home_btn,
            self.ui.add_btn,
            self.ui.search_btn,
            self.ui.edit_btn,
            self.ui.open_btn,
        ]


        # Add page
        self.ui.add_btn.clicked.connect(lambda: self.ui.main_stackedWidget.setCurrentWidget(self.ui.add_page))
        # Search page
        self.ui.search_btn.clicked.connect(lambda: self.ui.main_stackedWidget.setCurrentWidget(self.ui.search_page))
        # Edit page
        self.ui.edit_btn.clicked.connect(lambda: self.ui.main_stackedWidget.setCurrentWidget(self.ui.edit_page))
        # Open page
        self.ui.open_btn.clicked.connect(lambda: self.ui.main_stackedWidget.setCurrentWidget(self.ui.open_page))
        # Home page
        self.ui.home_btn.clicked.connect(lambda: self.ui.main_stackedWidget.setCurrentWidget(self.ui.home_page))
        
    def comfirmLogOut(self):
        reply = QMessageBox.question(self, 'Message', "Are you sure you want to log out?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.logOut()
        
    def logOut(self):
        print("Log Out")
        
        self.close()
        
        from login import Login_UI
        self.login_window = Login_UI(self.db_session)
        self.login_window.show()
    
    
    

    
    