
# ---------IMPORTS------------------------------------------

from typing import Optional
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt6 import uic

import sys
import os
from pathlib import Path
# Ensure the project root is in the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_session import DBSession

from ui import Navigation_UI, ShowFile_UI, EditBook_UI, AddBook_UI, SearchBook_UI

# ------------------------------------------------------------

# ---------MAINWINDOW_UI CLASS--------------------------------

class MainWindow_UI(QMainWindow):
    
    DESIGNER_FILE: str = "mainwindow.ui"

    def __init__(self, db_session: DBSession, account_id: Optional[str] = None, account_name: Optional[str] = None) -> None:
        
        super().__init__()
        
        # Set up the database session
        self.db_session = db_session
        
        # Set up the UI
        designer_files_path = Path(__file__).resolve().parent.joinpath("designer-files", self.DESIGNER_FILE)
        self.ui = uic.loadUi(designer_files_path, self)
        
        # Set fixed size of the window
        self.setFixedSize(1400, 630)  # Replace with your desired width and height
        
        # Connect modules
        self.navigation = Navigation_UI(self.ui, self.db_session)
        self.addbook = AddBook_UI(self.ui, self.db_session)
        self.searchbook = SearchBook_UI(self.ui, self.db_session)
        self.showfile = ShowFile_UI(self.ui, self.db_session)
        
        # Connect buttons to functions in the modules
        self.ui.find_btn.clicked.connect(self.searchbook.searchBookInformation)
        
        # Show admin id and name in the navigation bar
        self.account_id = account_id
        self.account_name = account_name
        self.ui.admin_id.setText(self.account_id)
        self.ui.admin_name.setText(self.account_name)
        
        # Set up the page buttons
        self.lastClickedPageButton: Optional[QPushButton] = None
        for button in self.showfile.buttons_open:
            button.clicked.connect(lambda checked, b=button: self.pageButtonClicked(b))
            
        for button in self.searchbook.buttons_edit:
            button.clicked.connect(lambda checked, b=button: self.pageButtonClicked(b))
        
        # Set home page as default page
        self.navigation.navigationButtonClicked(self.ui.home_btn)
    
        # Show the main window
        self.show()
        
    def pageButtonClicked(self, button):
        if self.lastClickedPageButton is not None:
            self.lastClickedPageButton.setStyleSheet("""
                QPushButton{
                    border: 2px solid black;
                    color: black;
                }
                QPushButton:hover{
                    border: 2px solid #560bad;
                    color: #560bad;
                }
            """)
            self.lastClickedPageButton.setDisabled(False)
        
        button.setStyleSheet("""
            QPushButton{
                border: 2px solid grey;
                color: grey;
            }
        """)
        button.setDisabled(True)
        
        self.lastClickedPageButton = button
    
    
# ---------MAIN-----------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    db_session_instance = DBSession()
    widget = MainWindow_UI(db_session_instance)
    widget.show()
    sys.exit(app.exec())


# ---------MAIN-----------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    db_session_instance = DBSession()
    widget = MainWindow_UI(db_session_instance)
    widget.show()
    sys.exit(app.exec())
    
# ------------------------------------------------------------
