import unittest
from db_session import DBSession

class TestDBSession(unittest.TestCase):
    def setUp(self):
        # Initialize the DBSession instance
        self.db_session = DBSession()
    
    def test_login_successful(self):
        # Test a successful login
        admin_id = "1"
        password = "password123"
        admin_data = self.db_session.logIn(admin_id, password)
        # Assert that the admin_data is not None
        self.assertIsNotNone(admin_data)
        # You can add more assertions to check the returned admin data
        
    def test_login_failed(self):
        # Test a failed login
        admin_id = "nonexistent_user"
        password = "incorrect_password"
        admin_data = self.db_session.logIn(admin_id, password)
        # Assert that the admin_data is None
        self.assertIsNone(admin_data)
        # You can add more assertions to check the behavior for failed logins
    
if __name__ == "__main__":
    unittest.main()
