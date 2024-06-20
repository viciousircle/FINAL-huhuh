# FULL NAME: Vũ Thị Minh Quý
# MSSV: 20227257
# CLASS: 150328
# PROJECT: 04 - Library Management System
# DATE: 20/06/2024 

# ----IMPORTS------------------------------------------
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QPushButton, QLineEdit
from PyQt6 import uic

import os
import sys
from pathlib import Path

# Add parent directory to sys.path to ensure relative imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.db_session import DBSession

# ---------LOGIN_UI CLASS--------------------------------
class Login_UI(QMainWindow):
    
    # Define class variables for UI elements
    guestBtn: QPushButton
    adminBtn: QPushButton
    input_name: QLineEdit
    backBtn: QPushButton
    enterBtn: QPushButton
    input_id: QLineEdit
    input_pass: QLineEdit
    backBtnLogIn: QPushButton
    loginBtn: QPushButton
    
    # Designer file name
    DESIGNER_FILE: str = "login.ui"
    
    def __init__(self, db_session: DBSession) -> None:
        super().__init__()
        
        # Initialize database session
        self.db_session = db_session
        
        # Load the .ui file designed with Qt Designer
        designer_files_path = Path(__file__).resolve().parent.joinpath("designer-files", self.DESIGNER_FILE)
        self.ui = uic.loadUi(designer_files_path, self)
        
        # Connect buttons to respective functions
        self.ui.adminBtn.clicked.connect(lambda: self.ui.login_widget.setCurrentWidget(self.ui.page_admin))
        self.ui.guestBtn.clicked.connect(lambda: self.ui.login_widget.setCurrentWidget(self.ui.page_guest))
        
        # Setup other connections
        self.setup_connections()

        # Show the main window
        self.show()
        
    def handle_login(self):
        # Handle admin login
        admin_id = str(self.ui.input_id.text())
        admin_password = str(self.ui.input_pass.text())
        
        # Call DBSession method to validate login
        admin_data = self.db_session.logIn(admin_id, admin_password)

        # Check if login is successful
        if admin_data is not None:
            from ui.mainwindow import MainWindow_UI
            main_window = MainWindow_UI(self.db_session, admin_data.admin_id, admin_data.admin_name, None, guest=False)  
            main_window.show()
            self.close()
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password. Please try again.")
            
    def handle_enter(self):
        # Handle guest enter
        guest_name = self.ui.input_name.text()
        
        # Validate guest name
        if guest_name == "":
            QMessageBox.critical(self, "Enter Failed", "You need enter your name first. Please try again.")  
        else:
            # Proceed with guest login
            from mainwindow import MainWindow_UI
            main_window = MainWindow_UI(self.db_session, None, None, guest_name, guest=True)  
            main_window.show()
            self.close()

    def setup_connections(self):
        # Connect UI buttons to corresponding methods
        self.ui.loginBtn.clicked.connect(self.handle_login)
        self.ui.enterBtn.clicked.connect(self.handle_enter)

        self.ui.backBtn.clicked.connect(self.backButtonClicked)
        self.ui.backBtnLogIn.clicked.connect(self.backButtonClicked)

    def backButtonClicked(self): 
        # Handle back button functionality
        result = QMessageBox.question(self, "Back", "Are you sure you want to go back? This will remove all the signed data.", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if result == QMessageBox.StandardButton.Yes:
            # Reset input fields and navigate back to welcome page
            self.ui.login_widget.setCurrentWidget(self.ui.page_welcome)
            self.ui.input_id.clear()
            self.ui.input_pass.clear()
            self.ui.input_name.clear()
        return

# ----- MAIN FUNCTION -------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    db_session_instance = DBSession()
    login_window = Login_UI(db_session_instance)    
    login_window.show()
    sys.exit(app.exec())
