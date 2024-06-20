
# ---------IMPORTS------------------------------------------

from typing import Optional
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt6 import uic

import sys
import os
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.db_session import DBSession

from ui import Navigation_UI, ShowFile_UI, EditBook_UI, AddBook_UI, SearchBook_UI, Home_UI


# ---------MAINWINDOW_UI CLASS--------------------------------

class MainWindow_UI(QMainWindow):
    
    DESIGNER_FILE: str = "mainwindow.ui"

    def __init__(self, db_session: DBSession, account_id: Optional[str] = None, account_name: Optional[str] = None, guest_name: Optional[str] = None, guest: Optional[bool] = False):
        
        super().__init__()        
        self.db_session = db_session

        self.db_session.connect()
        
        designer_files_path = Path(__file__).resolve().parent.joinpath("designer-files", self.DESIGNER_FILE)
        self.ui = uic.loadUi(designer_files_path, self)
        
        if guest:
            self.guestWindow(guest_name)
        else:
            self.adminWindow(str(account_id), str(account_name))

        self.show()

    def guestWindow(self, guest_name):
        self.guestRecord(guest_name)
        self.connectModulesForGuest()
        self.ui.add_btn.hide()

    def adminWindow(self, account_id, account_name):
        self.adminRecord(account_id, account_name)
        self.connectModulesForAdmin()

    def connectModulesForAdmin(self):
        self.navigation = Navigation_UI(self.ui, self.db_session)
        self.addbook = AddBook_UI(self.ui, self.db_session)
        self.searchbook = SearchBook_UI(self.ui, self.db_session)
        self.showfile = ShowFile_UI(self.ui, self.db_session)
        self.editbook = EditBook_UI(self.ui, self.db_session)
        self.home = Home_UI(self.ui, self.db_session)

    def connectModulesForGuest(self):
        self.navigation = Navigation_UI(self.ui, self.db_session)
        self.showfile = ShowFile_UI(self.ui, self.db_session)
        self.searchbook = SearchBook_UI(self.ui, self.db_session)
        self.home = Home_UI(self.ui, self.db_session)

    def adminRecord(self, account_id, account_name):
        self.account_id = account_id
        self.account_name = account_name
        self.ui.admin_id.setText(self.account_id)
        self.ui.admin_name.setText(self.account_name)

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

