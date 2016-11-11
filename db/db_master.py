from __future__ import print_function
import mysql.connector as mc
import logging
loger = logging.getLogger('DB master')

class MysqlMaster(object):
    """ Management mysql database """
    def __init__(self):
        self.config = {
            'user': 'sgdba',
            'password': 'sgdba',
            'host': '10.8.9.212',
            'port': 3306,
            'database': 'myskyg',
            'raise_on_warnings': True,
            'use_pure': False,
        }
        self.table_name = 'DOM_AIR_HANDLING_FEE_MST'
        self.connect_2_db()

    def connect_2_db(self):
        try:
            self.cnm = mc.connect(**self.config)
            self.cursor = self.cnm.cursor(buffered=True)
            print('Success')
            return True
        except mc.DatabaseError:
            print('Fail on connect to db')
        return False

    def count_handling_fee_rule_number(self):
        # Not use %s for table name because escape characters cause error
        # this one will prevent that.
        query_count = """SELECT COUNT(%s) FROM """ + self.table_name
        self.cursor.execute(query_count, ('FEE_CD',))
        return self.cursor.fetchone()[0]

    def print_fee_cd(self):
        query = 'SELECT * FROM ' + self.table_name
        self.cursor.execute(query)
        for row in self.cursor:
            print(row[0])

    def close_connection(self):
        self.cursor.close()
        self.cnm.close()
