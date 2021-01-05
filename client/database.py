import sqlalchemy as sqla
from passlib.hash import pbkdf2_sha512


class UsersDb:
    """
    Handles user database connection and operations
    """

    def __init__(self):
        self.db_engine:sqla.engine.Engine = sqla.create_engine('mysql+pymysql://chat_server:password_server@127.0.0.1:3306/chat_db')
        self.db_conn:sqla.engine.Connection = self.db_engine.connect()
        self.metadata:sqla.MetaData = sqla.MetaData()

    def table(self, table_name:str) -> sqla.Table:
        """
        Returns the specified table
        """
        return sqla.Table(table_name, self.metadata, autoload=True, autoload_with=self.db_engine)

    def get_password_hash(self, password:str) -> str:
        """
        Hashes a raw password and returns the hashed value
        """
        return pbkdf2_sha512.hash(password, rounds=200000, salt_size=16)

    def check_password_hashes(self, password:str, hashed_password:str) -> bool:
        """
        Compares a raw password to a hashed password.
        Returns true if they match else it returns false
        """
        return pbkdf2_sha512.verify(password, hashed_password)


class ChatHistoryDb:
    """
    Handles local chat database connection and operations
    """

    def __init__(self, db_name:str):
        self.db_engine:sqla.engine.Engine = sqla.create_engine(f'sqlite:///{db_name}')
        self.db_conn:sqla.engine.Connection = self.db_engine.connect()
        self.metadata:sqla.MetaData = sqla.MetaData()

    def table(self, table_name:str) -> sqla.Table:
        """
        Returns the specified table
        """
        return sqla.Table(table_name, self.metadata, autoload=True, autoload_with=self.db_engine)