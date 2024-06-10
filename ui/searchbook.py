# ------IMPORTS------------------------------------------
from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QPushButton, QMessageBox, QComboBox, QLabel,QLineEdit
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_session import DBSession
# ---------------------------------------------------------

# ------SEARCHBOOK_UI CLASS---------------------------------
class SearchBook_UI:
    # List of objects in .ui file related to this module
    input_choose            : QComboBox
    input_find              : QLabel
    find_btn                : QPushButton
    search_table            : QTableWidget
    
    book_id_text_2          : QLabel
    warehouse_id_text_2     : QLabel
    input_title_3           : QLineEdit
    input_author_3          : QLineEdit
    input_isbn_3            : QLineEdit
    input_comp_3            : QLineEdit
    input_year_3            : QLineEdit
    
    def __init__(self, ui, db_session: DBSession):
        self.ui         = ui
        self.db_session = db_session
        
    def searchBookInformation(self):
        try:
            # Clear previous search results from the table
            self.ui.search_table.clearContents()
            self.ui.search_table.setRowCount(0)

            column_mapping = {
                "Book ID"       : "book_id",
                "Warehouse ID"  : "warehouse_id",
                "Title"         : "title",
                "Author"        : "author",
                "Public Year"   : "public_year",
                "Public Company": "public_comp",
                "ISBN"          : "isbn",
                "Quantity"      : "quantity",
                "Stage"         : "stage"
            }

            filter_criteria = self.ui.input_choose.currentText()
            column_name     = column_mapping[filter_criteria]
            search_query    = self.ui.input_find.text().strip()
    
            search_results = list(self.db_session.searchBook(column_name, search_query))
            
            if search_results:
                self.ui.search_table.setRowCount(len(search_results))
                column_count = len(search_results[0]) 
                self.ui.search_table.setColumnCount(column_count)
                
                if filter_criteria != "Book ID" and filter_criteria != "Title":
                    header_labels = ['Book ID','Title', filter_criteria]
                else:
                    header_labels = ['Book ID','Title']
                    
                self.ui.search_table.setHorizontalHeaderLabels(header_labels)

                for row_idx, row_data in enumerate(search_results):
                    for col_idx, value in enumerate(row_data):
                        self.ui.search_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

                self.ui.search_table.resizeColumnsToContents()
            else:
                QMessageBox.warning(self.ui, "Search", "No results found.")
        except Exception as e:
            QMessageBox.critical(self.ui, "Error", str(e))

