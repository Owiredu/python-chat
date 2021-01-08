import sqlalchemy as sqla
from passlib.hash import pbkdf2_sha512
import os
import utils
from constants import LOCAL_CHAT_HISTORY_DB_PATH, MAXIMUM_CHAT_HISTORY_DB_SIZE


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

    def __init__(self):
        db_name = utils.current_chat_db_name()
        db_path = os.path.join(LOCAL_CHAT_HISTORY_DB_PATH, db_name)
        if os.path.exists(db_path):
            if utils.get_file_size_MB(db_path) >= MAXIMUM_CHAT_HISTORY_DB_SIZE:
                db_name = utils.next_chat_db_name()
                utils.create_next_chat_db(db_name)
        else:
            utils.create_next_chat_db(db_name)
        db_path = os.path.join(LOCAL_CHAT_HISTORY_DB_PATH, db_name)
        self.db_engine:sqla.engine.Engine = sqla.create_engine(f'sqlite:///{db_path}')
        self.db_conn:sqla.engine.Connection = self.db_engine.connect()
        self.metadata:sqla.MetaData = sqla.MetaData()

    def table(self, table_name:str) -> sqla.Table:
        """
        Returns the specified table
        """
        return sqla.Table(table_name, self.metadata, autoload=True, autoload_with=self.db_engine)