# FULL NAME: Vũ Thị Minh Quý
# MSSV: 20227257
# CLASS: 150328
# PROJECT: 04 - Library Management System
# DATE: 20/06/2024 

from PyQt6.QtWidgets import QApplication
from ui import Login_UI
from db import DBSession

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)  # Initialize QApplication

    db_session = DBSession()  # Create or obtain your database session object
    login_ui = Login_UI(db_session)
    login_ui.show()  # Assuming Login_UI inherits from QWidget and has a show() method

    sys.exit(app.exec())  # Start the application event loop
