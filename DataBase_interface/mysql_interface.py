'''
PYTHON  MYSPL interface functions 
used for save the the stock to database
autor : Siyu  
'''
import mysql.connector
from mysql.connector import errorcode
# from datetime import date
# from datetime import datetime
# from datetime import timedelta

class mysql_interface(object):
    def __init__(self):
        print 'MYSQL INTERFACE'
        print '   GO WAHOO'
#        print 'connect to the data bese'
#         try: 
#             self.MysqlDataBase=mysql.connector.connect(user='test', 
#                                         password='123456',
#                                         host='localhost',
#                                         database='testdb')
#             print 'database connect sucessfully'
#         except:
#             print 'data base connect error'

        # create the datatable variable list
        self.DataBase_stucture()
        
    def DataBase_stucture(self):
        
        self.databasename = 'testdb'
        
        self.datatable={}
        self.datatable['realtimequote']=(
            "CREATE TABLE `realtimequote`("
            " `stock_no` int(12) NOT NULL AUTO_INCREMENT,"
            " `stock_symbol` char(16) NOT NULL,"
            " `time` date NOT NULL,"
            " `volume` int(64) NOT NULL,"
            " PRIMARY KEY(`stock_no`)"
            ")ENGINE=InnoDB")
          
        self.datatable['premarketquote']=(
            "CREATE TABLE `premarketquote`("
            " `stock_no` int(12) NOT NULL AUTO_INCREMENT,"
            " `stock_symbol` char(16)  NOT NULL,"
            " `time` date NOT NULL,"
            " `volume` int(64) NOT NULL,"
            " PRIMARY KEY(`stock_no`)"
            ")ENGINE=InnoDB")  
        self.datatable['afterhoursquote']=(
            "CREATE TABLE `afterhoursquote`("
            " `stock_no` int(12) NOT NULL AUTO_INCREMENT,"
            " `stock_symbol` char(16)  NOT NULL,"
            " `time` date NOT NULL,"
            " `volume` int(64) NOT NULL,"
            " PRIMARY KEY(`stock_no`)"
            ")ENGINE=InnoDB")
        self.datatable['summaryquote']=(
            "CREATE TABLE `summaryquote`("
            "`stock_no` int(12) NOT NULL AUTO_INCREMENT,"
            "`stock_symbol` char(16)  NOT NULL,"
            "`1_Year_Target` int(16) NOT NULL,"
            "`todayhigh` int(16) NOT NULL,"
            "`todaylow` int(16) NOT NULL,"
            "`sharevolume` int(16) NOT NULL,"
            "`50dayave_volome` int(32) NOT NULL,"
            "`previousclose` int(16) NOT NULL,"
            "`52weekhigh` int(16) NOT NULL,"
            "`52weeklow` int(16) NOT NULL,"
            "`marketcap` int(16) NOT NULL,"
            "`pe_ratio` int(16) NOT NULL,"
            "`forwordpe1y` int(16) NOT NULL,"
            "`earningpershare` int(16) NOT NULL,"
            "`annualizeddividend` int(16) NOT NULL,"
            "`exdividenddate` date NOT NULL,"
            "`dividendpaymentdate` date NOT NULL,"
            "`currentyield` int(16) NOT NULL,"
            "`beta` int(16) NOT NULL,"
            "`NASDAQ_official_open_price` int(16) NOT NULL,"
            "`dateofopenprice` date NOT NULL,"
            "`NASDAQ_official_close_price` int(16) NOT NULL,"
            "`dateofcloseprice` int(16) NOT NULL,"
            "PRIMARY KEY(`stock_no`)"
            ")ENGINE=InnoDB")
    
    def create_database(self, databasename_in=None, user=None):
 
        DB_name = ''
        if databasename_in is None:
            DB_name = self.databasename
        else:
            DB_name = databasename_in
        
        db_user = ''
        if user is None:
            db_user = 'test'
        else:
            db_user = user
        
        cnx=mysql.connector.connect(user=db_user, 
                                        password='123456',
                                        )
        cursor=cnx.cursor()
        # create database
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_name)
                )
        except mysql.connector.Error as err:
            print "Failed creating database:" + format(err)
        
        # connect the database ready to create the data table 
        try:
            cnx.database=DB_name
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print 'errorcode.ER_BAD_DB_ERROR, Maybe the database ' +format(DB_name)+ 'has not beem crerated' 
            else:
                print err
                exit(1)
        
        # create the data tables
        for name, ddl in self.datatable.iteritems():
            try:
                print 'create table '+format(name)
                cursor.execute(ddl)
                print '    '+format(name) +' database create sucessfully'  
            except  mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print '    data base already exist'
                else:
                    print err.msg
        cursor.close()
        cnx.close()
        
    def Save(self,databasename_in,save_data_in):
        print 'test'
    def GetStockData(self,stock_symbol):
        print 'extract the data from server'
    
    def DB_test(self):
        print 'database save functions'

    def CloseDB(self):
        print 'close datadb....'
        try:
            self.MysqlDataBase.close()
            print 'database closed'
        except:
            print 'data base close error'

# test functions
if __name__ == '__main__':
    print 'this is only used for test....'
    a=mysql_interface()
    a.create_database()
    a.CloseDB()
    