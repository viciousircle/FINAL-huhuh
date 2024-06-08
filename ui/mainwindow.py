from typing import Callable, Optional, Any
from datetime import datetime


from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QPushButton, QMessageBox
from PyQt6 import uic
import sys
from pathlib import Path



class MainWindow_UI(QMainWindow):
    
    
    
    DESIGNER_FILE: str = "mainwindow.ui"

    
    def __init__(self):
        super().__init__()
        
        
        # for designer file
        designer_files_path = Path(__file__).resolve().parent.joinpath("designer-files", self.DESIGNER_FILE)
        self.ui = uic.loadUi(designer_files_path, self)
        
        
        # List of buttons_nav in navigation bar
        self.buttons_nav = [
            self.ui.home_btn,
            self.ui.add_btn,
            self.ui.search_btn,
            self.ui.edit_btn,
            self.ui.open_btn,
        ]
        
        self.buttons_open = [
            self.ui.show_file_1,
            self.ui.show_file_2,
        ]
        
        self.show()
        
        self.lastClickedButton: Optional[QPushButton] = None
                
        # Switch page
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
        
        
        # Show file
        self.ui.show_file_1.clicked.connect(lambda: self.ui.files_stackedWidget.setCurrentWidget(self.ui.bookMarc_page))
        self.ui.show_file_2.clicked.connect(lambda: self.ui.files_stackedWidget.setCurrentWidget(self.ui.book_page))
        
    
        for button in self.buttons_nav:
            button.clicked.connect(lambda checked, b=button: self.buttonClicked(b))
        for button in self.buttons_open:
            button.clicked.connect(lambda checked, b=button: self.buttonClicked(b))
        
        #Connect log out button
        self.ui.logout_btn.clicked.connect(self.comfirmLogout)  
        
        # Set home page as default
        self.buttonClicked(self.ui.home_btn)
        
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
    
    def comfirmLogout(self):
        reply = QMessageBox.question(self, 'Message', "Are you sure you want to log out?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.logout()
        
    def logout(self):
        print("Logout")
        self.close()
        
        from login import Login_UI
        self.login_window = Login_UI()
        self.login_window.show()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow_UI()
    widget.show()
    sys.exit(app.exec())
