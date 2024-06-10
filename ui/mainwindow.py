from typing import Optional
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QLabel, QListWidget
from PyQt6 import uic

import sys
import os
from pathlib import Path
# Ensure the project root is in the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_session import DBSession

from ui import Navigation_UI, ShowFile_UI, EditBook_UI, AddBook_UI, SearchBook_UI
# from addbook import AddBook

class MainWindow_UI(QMainWindow):
    
    DESIGNER_FILE: str = "mainwindow.ui"

    def __init__(self, db_session: DBSession, account_id: Optional[str] = None, account_name: Optional[str] = None)-> None:
        
        super().__init__()
        
        # Set up the database session
        self.db_session     = db_session
        
        # Set up the UI
        designer_files_path = Path(__file__).resolve().parent.joinpath("designer-files", self.DESIGNER_FILE)
        self.ui             = uic.loadUi(designer_files_path, self)
        
        # Connect modules
        self.navigation     = Navigation_UI(self.ui, self.db_session)
        self.addbook        = AddBook_UI(self.ui, self.db_session)
        self.editbook       = EditBook_UI(self.ui, self.db_session)
        self.searchbook     = SearchBook_UI(self.ui, self.db_session)
        self.showfile       = ShowFile_UI(self.ui, self.db_session)
        
        # Show admin id and name in the main window
        self.account_id     = account_id
        self.account_name   = account_name
        self.ui.admin_id.setText(str(self.account_id))
        self.ui.admin_name.setText(self.account_name)
        
        # Connect buttons to functions in the modules
        self.ui.submit_btn.clicked.connect(self.addbook.addBookInformation)
        self.ui.find_btn.clicked.connect(self.searchbook.searchBookInformation)
        self.ui.find_btn_2.clicked.connect(self.editbook.editBookInformation)
        self.ui.save_btn.clicked.connect(self.editbook.saveBookInformation)
        
        # # Show files in page open file
        # self.showfile.showFileBookMarc()
        # self.showfile.showFileBook()
        
        # Save the last clicked button
        self.lastClickedButton: Optional[QPushButton] = None

        for button in self.navigation.buttons_nav:
            button.clicked.connect(lambda checked, b=button: self.buttonClicked(b))
        for button in self.showfile.buttons_open:
            button.clicked.connect(lambda checked, b=button: self.buttonClicked(b))
        
        
        # Set home page as default
        self.buttonClicked(self.ui.home_btn)
        
        
        # ----- Show the main window -----
        self.show()
        

    def buttonClicked(self,button):
        
        if self.lastClickedButton is not None:
            self.lastClickedButton.setStyleSheet("""
                QPushButton{
                    border: 2px solid black;
                    color: black;
                }
                QPushButton:hover{
                    border: 2px solid #560bad;
                    color: #560bad;
                }
            """)
            self.lastClickedButton.setDisabled(False)
            
        
        
        button.setStyleSheet("""
            QPushButton{
                border: 2px solid grey;
                color: grey;
            }
        """)
        button.setDisabled(True)
        
        self.lastClickedButton = button
    
    # def comfirmLogOut(self):
    #     reply = QMessageBox.question(self, 'Message', "Are you sure you want to log out?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
    #     if reply == QMessageBox.StandardButton.Yes:
    #         self.logOut()
        
    # def logOut(self):
    #     print("Log Out")
        
    #     self.close()
        
    #     from login import Login_UI
    #     self.login_window = Login_UI(self.db_session)
    #     self.login_window.show()
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    db_session_instance = DBSession()
    widget = MainWindow_UI(db_session_instance)
    widget.show()
    sys.exit(app.exec())
