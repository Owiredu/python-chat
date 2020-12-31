import sqlalchemy as sqla 
from passlib.hash import pbkdf2_sha512


class UsersDb:
    """
    Handles database connection and operations
    """

    def __init__(self):
        self.db_engine = sqla.create_engine('mysql+pymysql://chat_server:password_server@127.0.0.1:3306/chat_db')
        self.db_conn = self.db_engine.connect()
        self.metadata = sqla.MetaData()

    def table(self, table_name):
        """
        Returns the specified table
        """
        return sqla.Table(table_name, self.metadata, autoload=True, autoload_with=self.db_engine)

    def get_password_hash(self, password):
        """
        Hashes a raw password and returns the hashed value
        """
        return pbkdf2_sha512.hash(password, rounds=200000, salt_size=16)

    def check_password_hashes(self, password, hashed_password):
        """
        Compares a raw password to a hashed password.
        Returns true if they match else it returns false
        """
        return pbkdf2_sha512.verify(password, hashed_password)