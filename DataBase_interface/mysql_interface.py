'''
PYTHON  MYSPL interface functions 
used for save the the stock to database
autor : Siyu  
'''
import mysql.connector
from mysql.connector import errorcode
#from mysql.utilities.common import database
#from gtk.keysyms import cursor

#from datetime import date
from datetime import datetime
#from datetime import timedelta

class mysql_interface(object):
    def __init__(self):
        print '\n\nMYSQL INTERFACE'
        print '   GO WAHOO\n'
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
        self.__DataBase_stucture()
        
    def __DataBase_stucture(self):
        
        self.databasename = 'testdb'
        self.datatable={}
        self.datatable['realtimequote']=(
            "CREATE TABLE `realtimequote`("
            " `stock_no` bigint NOT NULL AUTO_INCREMENT,"
            " `stock_symbol` varchar(16) NOT NULL,"
            " `time` datetime NOT NULL,"
            " `price` float NOT NULL, "
            " `volume` int(32) NOT NULL,"
            " `datasavetime` datetime NOT NULL,"
            " PRIMARY KEY(`stock_no`)"
            ")ENGINE=InnoDB")
        
        self.datatable['premarketquote']=(
            "CREATE TABLE `premarketquote`("
            " `stock_no` bigint NOT NULL AUTO_INCREMENT,"
            " `stock_symbol`varchar(16)  NOT NULL,"
            " `time` datetime NOT NULL,"
            " `price` float NOT NULL, "
            " `volume` int(32) NOT NULL,"
            " `datasavetime` datetime NOT NULL,"
            " PRIMARY KEY(`stock_no`)"
            ")ENGINE=InnoDB")  
        
        self.datatable['afterhoursquote']=(
            "CREATE TABLE `afterhoursquote`("
            " `stock_no` bigint NOT NULL AUTO_INCREMENT,"
            " `stock_symbol` varchar(16)  NOT NULL,"
            " `time` datetime NOT NULL,"
            " `price` float NOT NULL,"
            " `volume` int(32) NOT NULL,"
            " `datasavetime` datetime NOT NULL,"
            " PRIMARY KEY(`stock_no`)"
            ")ENGINE=InnoDB")
        
        self.datatable['summaryquote']=(
            "CREATE TABLE `summaryquote`("
            " `stock_no` bigint NOT NULL AUTO_INCREMENT,"
            " `stock_symbol` varchar(16)  NOT NULL,"
            " `1_Year_Target` float NOT NULL,"
            " `todayhigh` float NOT NULL,"
            " `todaylow` float NOT NULL,"
            " `sharevolume` int(32) NOT NULL,"
            " `50dayave_volome` int(32) NOT NULL,"
            " `previousclose` float NOT NULL,"
            " `52weekhigh` float NOT NULL,"
            " `52weeklow` float NOT NULL,"
            " `marketcap` float NOT NULL,"
            " `pe_ratio` float(24) NOT NULL,"
            " `forwordpe1y` float(24) NOT NULL,"
            " `earningpershare` float(24) NOT NULL,"
            " `annualizeddividend` float NOT NULL,"
            " `exdividenddate` date NOT NULL,"
            " `dividendpaymentdate` date NOT NULL,"
            " `currentyield` float(24) NOT NULL,"
            " `beta` float(24) NOT NULL,"
            " `NASDAQ_official_open_price` float NOT NULL,"
            " `dateofopenprice` date NOT NULL,"
            " `NASDAQ_official_close_price` float NOT NULL,"
            " `dateofcloseprice` date NOT NULL,"
            " `datasavetime` datetime NOT NULL,"
            "PRIMARY KEY(`stock_no`)"
            ")ENGINE=InnoDB")
        
        self.add_table={}
        self.add_table['realtimequote'] = ("INSERT INTO realtimequote"
                                           "(stock_symbol,time,price,volume,datasavetime)"
                                           "VALUES (%s,%s,%s,%s,%s)")
        self.add_table['premarketquote'] = ("INSERT INTO premarketquote"
                                           "(stock_symbol,time,price,volume,datasavetime)"
                                           "VALUES (%s,%s,%s,%s,%s)") 
        self.add_table['afterhoursquote'] = ("INSERT INTO afterhoursquote"
                                           "(stock_symbol,time,price,volume,datasavetime)"
                                           "VALUES (%s,%s,%s,%s,%s)") 
        
        self.add_table['summaryquote'] = ("INSERT INTO realtimequote"
                                           "(stock_symbol,1_Year_Target,todayhigh,todaylow,sharevolume,50dayave_volome,previousclose,52weekhigh, \
                                           52weeklow,marketcap,pe_ratio,forwordpe1y,earningpershare,annualizeddividend,exdividenddate,dividendpaymentdate, \
                                           currentyield,beta,NASDAQ_official_open_price,dateofopenprice,NASDAQ_official_close_price,dateofcloseprice,datasavetime \
                                           )"
                                           "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        
    def create_database(self, databasename_in=None, user=None,passcode=None):
 
        DB_name = ''
        if databasename_in is None:
            DB_name = self.databasename
        else:
            DB_name = databasename_in
        
        DB_user = ''
        if user is None:
            DB_user = 'test'
        else:
            DB_user = user
        DB_passcode=''
        if passcode is None:
            DB_passcode = '123456'
        else:
            DB_passcode = passcode
        
        cnx=mysql.connector.connect(user=DB_user, 
                                        password=DB_passcode,
                                        )
        cursor=cnx.cursor()
        
        # create database
        print '\n\n  **Create DataBase**\n'
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
        print '\n\n  **Create DataBase Table**\n'
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
        
    def Save(self,databasename_in,save_data_in,user=None,passcode=None):
        DB_user=''
        if user is None:
            DB_user='test'
        else:
            DB_user=user
        DB_passcode=''
        if passcode is None:
            DB_passcode='123456'
        else:
            DB_passcode=passcode
        
        DB_name = databasename_in
        
        # connect to the database
        cursor=''
        try:
            cnx=mysql.connector.connect(user=DB_user,password=DB_passcode,database=DB_name)
            cursor=cnx.cursor()
            print '    <'+format(DB_name)+'> connected'
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print 'error in connect database '+format(DB_name)+', TRY TO Recreate it'
                self.create_database(DB_name, DB_user, DB_passcode)
                self.Save(databasename_in, save_data_in, user, passcode)
            else:
                print 'Can NOT connect to database <'+format(DB_name)+'>'
                exit(-1)
                
        data=('A',datetime.now(),float(100.01),int(200000),datetime.now())
        cursor.execute(self.add_table['afterhoursquote'],data)
        cnx.commit()
        cursor.close()
        cnx.close()
        
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
    data=('A',datetime.now(),100.01,200000,datetime.now())
    a.Save('testdb', data, 'test', '123456')
    #a.CloseDB()
    