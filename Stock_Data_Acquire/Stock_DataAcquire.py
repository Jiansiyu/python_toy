# main stock Data Acquire function that used for get the stock data
# Stock_DataAcquire.py
# used for searching the stock price and save in to csv file
# add the real time stock scan method to get the realtime price in a day
# issues for realtime stock price
# when scan all the companies, the time delay would be a big issues.Maybe need to change to parellel
# to solve the time delay issues, would be better just build a interest list and only retrieve the informations in the interest list

from pandas_datareader import data
from googlefinance import getQuotes
from csv import DictWriter
import urllib   # used for get the NASDAQ company name list from ftp server
import os.path  # used for check the existance of files
import datetime
import json     # json decoder interface
import os
import errno
import csv
import sys

import timeit

class Stock_DataAcquire(object):

    def __init__(self,stock_listfilename=None,data_source_engine=None):
        """
        """
        print 'test'
        # set the data source
        if data_source_engine is None:
            self.data_source_engine='google'
        else:
            self.data_source_engine=data_source_engine
        #set the filename list
        if stock_listfilename is None:
            #get the listed nasdaq company names from nasdaq ftp server
            self.Get_Nasdaq_companylist()
            self.stock_listfilename='nasdaqlisted.txt'
        else:
            # check the existance of the nasdaq filename list, if the file is not exist try to download from ftp server
            if os.path.isfile(stock_listfilename):
                self.stock_listfilename=stock_listfilename
            else:
                print 'The specified file is not exist, trying to down load from ftp server...'
                self.Get_Nasdaq_companylist()
                self.stock_listfilename='nasdaqlisted.txt'
        # finish retrieve the company filename

    #loading realtime data list
    def Google_finance_acquire(self,Stock_Interest_list=None):
        if Stock_Interest_list is None:
            self.Stock_list_filename=self.stock_listfilename
        else:
            self.Stock_list_filename=Stock_Interest_list
        Data_path='Daily_Stock_Infor'

        # create folder if not exist
        if not os.path.exists(Data_path):
            os.makedirs(Data_path)
        #decode the stock compony name, and use that name to get the real time price
        with open(self.Stock_list_filename) as Stock_list_io:
            Stock_list_filename_lines=Stock_list_io.readlines()
        # decoder the header, and get the data strcuture of the csv file
        Stock_header_infor=Stock_list_filename_lines[0].split('|')
        Stock_name_Symbol_position=Stock_header_infor.index('Symbol')
        Stock_name_Security_name_position=Stock_header_infor.index('Security Name')
        Stock_name_Market_Category_position=Stock_header_infor.index('Market Category')
        Stock_name_Financial_Status_position=Stock_header_infor.index('Financial Status')
        Stock_name_ETF_position=Stock_header_infor.index('ETF')

        #finish decode the csv compony name list, start aquire the realtime data
        #loops on all the lines and get all the price, create a folder and save the price in that folder
        self.iterator_couter=0
        for Stock_list_Single_line in Stock_list_filename_lines:
            Stock_Single_line_infor=Stock_list_Single_line.split('|')
            print self.iterator_couter
            self.iterator_couter=self.iterator_couter+1
            print Stock_Single_line_infor[Stock_name_Symbol_position]+'  Stock_Market_Category  '+Stock_Single_line_infor[Stock_name_Market_Category_position]
            try:
                self.Single_Company_temp=json.dumps(getQuotes(Stock_Single_line_infor[Stock_name_Symbol_position]))
                #print self.Single_Company_temp
                self.json_data=json.loads(self.Single_Company_temp)
                for self.Single_company_inpackage in self.json_data:
                    for self.keys in self.Single_company_inpackage.keys():
                        print self.keys
                    for self.keys,self.values in  self.Single_company_inpackage.iteritems():
                        print self.keys +'                     '+ self.values

                    print '++++++++++++++++++++++++++++++++++++++++'
            except:
                print 'retrieve error'
                
    #def Yahoo_finance_acquire(self):

    # pandas data acquire interface, only used for get the daily informations
    def Pandas_Data_acquire(self,Stock_Interest_list=None,Data_source=None,StartTime=None,EndTime=None,data_path=None):

        # loading the insterest list
        if Stock_Interest_list is None:
            Pandas_Stock_list_filename=self.stock_listfilename
        else:
            Pandas_Stock_list_filename=Stock_Interest_list

        # loading the data source
        if Data_source is not None:
            Pandas_Data_Source=Data_Source
        else:
            Pandas_Data_Source='yahoo'
        
        # loading the stat time 
        if StartTime is not None:
            Pandas_StartTime=StartTime
        else:
            Pandas_StartTime='1980-01-01'
        #loading data path
        if data_path is not None:
            Pandas_Data_path=data_path
        else:
            Pandas_Data_path='Data/Stock_daily_infor'
        # create folder if not exist
        if not os.path.exists(Pandas_Data_path):
            os.makedirs(Pandas_Data_path)
            
        with open(Pandas_Stock_list_filename) as Stock_list_io:
            Stock_list_lines=Stock_list_io.readlines()
            #get the nasdaq systerm infor
            Stock_header_infor=Stock_list_lines[0].split('|')
            Symbol_position =  Stock_header_infor.index('Symbol')
            Security_name_position=Stock_header_infor.index('Security Name')
            Market_Category_position=Stock_header_infor.index('Market Category')
            Financial_Status_position=Stock_header_infor.index('Financial Status')
            ETF_position=Stock_header_infor.index('ETF')
            #print Symbol_position
            #get the individual nasdaq conpany name
            for Single_line in Stock_list_lines:
                Stock_infor=Single_line.split('|')
                print Stock_infor[Symbol_position]+' Security name=>'+Stock_infor[Security_name_position]
                try:
                    stock_data=data.DataReader(Stock_infor[Symbol_position], 'google','1980-01-01')
                    stock_data.to_csv(Pandas_Data_path+'/'+Stock_infor[Symbol_position]+'.csv')
                except:
                    with open('errorlog.log','a') as error_log:
                        error_log.writelines(Pandas_Stock_list_filename+'   Error in' +Stock_infor[Symbol_position]+' Security name=>'+Stock_infor[Security_name_position])
                        error_log.close()
                        print '[ERROR] '+Stock_infor[Symbol_position]+' Security name=>'+Stock_infor[Security_name_position]
                    
    # get finance data from google finance
    def Get_Nasdaq_companylist(self,Nasdaq_ftp_nasdaqlisted=None,Nasdaq_ftp_nasdaqtraded=None):

        print 'Trying to retrieve the NASDAQ company name list from server'
        if Nasdaq_ftp_nasdaqlisted is None:
            self.Nasdaq_ftp_nasdaqlisted='ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt'
        else:
            self.Nasdaq_ftp_nasdaqlisted=nasdaqlisted_url

        # get the file from nasdaq ftp server
        if Nasdaq_ftp_nasdaqtraded is None:
            self.Nasdaq_ftp_nasdaqtraded='ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqtraded.txt'
        else:
            self.Nasdaq_ftp_nasdaqtraded=nasdaqlisted_url
         # get the file from nasdaq ftp server
        try:
            urllib.urlretrieve(self.Nasdaq_ftp_nasdaqlisted, 'nasdaqlisted.txt')
        except:
            print 'Read company list from ftp server error from  '+ self.Nasdaq_ftp_nasdaqlisted

        try:
            urllib.urlretrieve(self.Nasdaq_ftp_nasdaqlisted, 'nasdaqlisted.txt')
        except:
            print 'Read company list from ftp server error from  ' + self.Nasdaq_ftp_nasdaqtraded

    #check whether the current time is trade time, used for retrieve the realtime data and save to files
    def Check_NASDAQ_open(self):
        self.current_time=datetime.datetime.now()
        if self.current_time.isoweekday() in range(1,5) and current_time.hour in range(9,18):
            return True
        else:
            return False

    # save the json data into folders/files
    # need to set the save path, and the save name, and the save mode(recreate or add)
    # it will auto check the existance of the files,
    # by default, the save mode would be add instead of recreate
    def _Save_json(self,json_data,save_path,stock_companyname=None,save_mode=None):
        if json_data is not None:
            Save_JsonData=json_data
        else:
            print 'Save Data is empty'
        if save_path is not None:
            Save_Save_path=save_path
        else:
            print 'Save Path is empty'

        #check the existance of the folder, if not trying to create the folder used to save the file
        save_basename=os.path.dirname(save_path)
        if not os.path.exists(save_basename):
            os.makedirs(save_basename)

        if stock_companyname is not None:
            save_stock_companyname=stock_companyname
        else:
            save_stock_companyname=Save_JsonData['StockSymbol']

        if save_mode is None or save_mode is 'w' or save_mode is 'recreate' or save_mode is 'new':
            save_targetfile= open(save_stock_companyname+'.csv','w') # create a new file
            # write the headers
            savewriter=DictWriter(save_targetfile,Save_JsonData.keys())
            savewriter.writeheader()
            savewriter.writerows(Save_JsonData)
            save_targetfile.close()
        else:
            # read the headers and write cresponding data into the folder
            print 'write to existance files'
