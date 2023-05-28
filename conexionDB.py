import pymongo
import mysql.connector


class DataBase:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="platanex"
        )
        self.cursor = self.connection.cursor()



