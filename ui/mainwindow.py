# FULL NAME: Vũ Thị Minh Quý
# MSSV: 20227257
# CLASS: 150328
# PROJECT: 04 - Library Management System
# DATE: 20/06/2024 
# ----IMPORTS------------------------------------------
from typing import Optional
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt6 import uic

import sys
import os
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.db_session import DBSession

# Import other UI modules from the application
from ui import Navigation_UI, ShowFile_UI, EditBook_UI, AddBook_UI, SearchBook_UI, Home_UI

# ---------MAINWINDOW_UI CLASS--------------------------------
class MainWindow_UI(QMainWindow):
    
    DESIGNER_FILE: str = "mainwindow.ui"

    def __init__(self, db_session: DBSession, account_id: Optional[str] = None, account_name: Optional[str] = None, guest_name: Optional[str] = None, guest: Optional[bool] = False):
        
        super().__init__()        

        # Initialize the database session
        self.db_session = db_session
        self.db_session.connect()  # Connect to the database

        # Load the UI from the designer .ui file using PyQt6
        designer_files_path = Path(__file__).resolve().parent.joinpath("designer-files", self.DESIGNER_FILE)
        self.ui = uic.loadUi(designer_files_path, self)
        
        # Determine whether the window is for admin or guest based on the given parameters
        if guest:
            self.guestWindow(guest_name)
        else:
            self.adminWindow(str(account_id), str(account_name))

        self.show()

    # Method to display the UI for a guest user
    def guestWindow(self, guest_name):
        self.guestRecord(guest_name)
        self.connectModulesForGuest()
        self.ui.add_btn.hide()  # Hide the add book button for guests

    # Method to display the UI for an admin user
    def adminWindow(self, account_id, account_name):
        self.adminRecord(account_id, account_name)
        self.connectModulesForAdmin()

    # Connect and initialize modules for an admin user
    def connectModulesForAdmin(self):
        self.navigation = Navigation_UI(self.ui, self.db_session)
        self.addbook = AddBook_UI(self.ui, self.db_session)
        self.searchbook = SearchBook_UI(self.ui, self.db_session)
        self.showfile = ShowFile_UI(self.ui, self.db_session)
        self.editbook = EditBook_UI(self.ui, self.db_session)
        self.home = Home_UI(self.ui, self.db_session)

    # Connect and initialize modules for a guest user
    def connectModulesForGuest(self):
        self.navigation = Navigation_UI(self.ui, self.db_session)
        self.showfile = ShowFile_UI(self.ui, self.db_session)
        self.searchbook = SearchBook_UI(self.ui, self.db_session)
        self.home = Home_UI(self.ui, self.db_session)

    # Store admin account information in member variables
    def adminRecord(self, account_id, account_name):
        self.account_id = account_id
        self.account_name = account_name
        self.ui.admin_id.setText(self.account_id)
        self.ui.admin_name.setText(self.account_name)

    # Store guest name information in member variables
    def guestRecord(self, guest_name):
        self.guest_name = guest_name
        self.ui.admin_id.setText("Guest")
        self.ui.admin_name.setText(self.guest_name)
        
# ---------MAIN-----------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    db_session_instance = DBSession()
    widget = MainWindow_UI(db_session_instance)
    widget.show()
    sys.exit(app.exec())
