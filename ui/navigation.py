import sys
import os
from PyQt6.QtWidgets import  QPushButton, QMessageBox, QLabel
from db_session import DBSession

from login import Login_UI

# Ensure the project root is in the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Navigation_UI:
    
    admin_id                : QLabel
    admin_name              : QLabel
    
    home_btn                : QPushButton
    open_btn                : QPushButton
    search_btn              : QPushButton
    add_btn                 : QPushButton
    edit_btn                : QPushButton
    
    logout_btn              : QPushButton
    
    def __init__(self, ui, db_session: DBSession):
        self.ui         = ui
        self.db_session = db_session
        
        # List of buttons in the navigation bar
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
        
        # Log out
        self.ui.logout_btn.clicked.connect(self.comfirmLogOut)
        
    def comfirmLogOut(self):
        
        reply = QMessageBox.question(self.ui, 'Message', "Are you sure you want to log out?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.logOut()
        
    def logOut(self):
        
        self.ui.close()
        
        self.login_window = Login_UI(self.db_session)
        self.login_window.show()
    
    
    

    
    