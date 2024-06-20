# ------IMPORTS------------------------------------------
import sys
import os
from PyQt6.QtWidgets import QPushButton, QMessageBox, QLabel
from db.db_session import DBSession
from typing import Optional

# Append the parent directory to sys.path to access sibling modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Login_UI from the ui module
from ui import Login_UI

# ---------NAVIGATION_UI CLASS--------------------------------
class Navigation_UI:
    
    # List of objects in .ui file related to this module
    admin_id: QLabel
    admin_name: QLabel
    
    home_btn: QPushButton
    open_btn: QPushButton
    search_btn: QPushButton
    add_btn: QPushButton
    
    logout_btn: QPushButton
    
    def __init__(self, ui, db_session: DBSession):
        
        # Linking the objects in the .ui file to the variables in this module
        self.ui = ui
        self.db_session = db_session

        # Initialize the last clicked navigation button to None
        self.lastClickedNavButton: Optional[QPushButton] = None

        # Automatically click on the home button to show the home page initially
        self.navigationButtonClicked(self.ui.home_btn)

        # List of buttons in the navigation bar
        self.buttons_nav = [
            self.ui.home_btn,
            self.ui.add_btn,
            self.ui.search_btn,
            self.ui.open_btn,
        ]

        # Connect each button to its corresponding function
        self.ui.open_btn.clicked.connect(self.updateOpenFilesPage)
        self.ui.home_btn.clicked.connect(self.updateHomePages)
        self.ui.add_btn.clicked.connect(lambda: self.ui.main_stackedWidget.setCurrentWidget(self.ui.add_page))
        self.ui.search_btn.clicked.connect(lambda: self.ui.main_stackedWidget.setCurrentWidget(self.ui.search_page))
        self.ui.open_btn.clicked.connect(lambda: self.ui.main_stackedWidget.setCurrentWidget(self.ui.open_page))
        self.ui.home_btn.clicked.connect(lambda: self.ui.main_stackedWidget.setCurrentWidget(self.ui.home_page))
        
        # Connect logout button to confirm logout function
        self.ui.logout_btn.clicked.connect(self.confirmLogOut)

        # Connect navigation button click events to navigationButtonClicked function
        for button in self.buttons_nav:
            button.clicked.connect(lambda checked, b=button: self.navigationButtonClicked(b))

    # Function to confirm logout with a message box
    def confirmLogOut(self):
        reply = QMessageBox.question(self.ui, 'Message', "Are you sure you want to log out?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.logOut()

    # Function to perform logout
    def logOut(self):
        # Close the current UI window
        self.ui.close()

        # Open a new instance of the Login_UI window
        self.login_window = Login_UI(self.db_session)
        self.login_window.show()

    # Function to handle navigation button clicks
    def navigationButtonClicked(self, button):
        print(f"Button navigation clicked: {button.text()}")

        # Reset style and enable the last clicked button (if exists)
        if self.lastClickedNavButton is not None:
            self.lastClickedNavButton.setStyleSheet("""
                QPushButton{
                    border: 2px solid black;
                    color: black;
                }
                QPushButton:hover{
                    border: 2px solid #560bad;
                    color: #560bad;
                }
            """)
            self.lastClickedNavButton.setDisabled(False)
        
        # Set the style and disable the clicked button
        button.setStyleSheet("""
            QPushButton{
                border: 2px solid grey;
                color: grey;
            }
        """)
        button.setDisabled(True)
        
        # Update the last clicked button to the current one
        self.lastClickedNavButton = button

    # Function to update the 'Open Files' page
    def updateOpenFilesPage(self):
        from ui import ShowFile_UI
        showfile = ShowFile_UI(self.ui, self.db_session)
        showfile.updateBookMarcTable()
        showfile.updateBookTable()

    # Function to update the 'Home' page
    def updateHomePages(self):
        from ui import Home_UI
        home = Home_UI(self.ui, self.db_session)
        home.showNumberOfBooks()
        home.showQuantityOfBooks()
        home.showNewAddedBooks()

