# main stock Data Acquire function that used for get the stock data 
# Stock_DataAcquire.py 
# used for searching the stock price and save in to csv file
# add the real time stock scan method to get the realtime price in a day

# issues for realtime stock price
# when scan all the companies, the time delay would be a big issues.Maybe need to change to parellel 

from pandas_datareader import data
from googlefinance import getQuotes
import json  # json decoder interface
import os
import errno
import csv
import sys 

class Stock_DataAcquire:
    
    def __init__(self,data_source_engine):
        self.data_source_engine = data_source_engine;
        self.CompListName='nasdaqlisted.txt'
        self.CompInFor=[];
        
    def Stock_Aquire(self):
        
    def Google_finance_acquire(self):
        Stock_list_filename='nasdaqlisted.txt'
        Data_path='Daily_Stock_Infor'
        
        # create folder if not exist 
        if not os.path.exists(Data_path):
            os.makedirs(Data_path)
        #decode the stock compony name, and use that name to get the real time price 
        with open(Stock_list_filename) as Stock_list_io:
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
        for Stock_list_Single_line in Stock_list_filename_lines:
            Stock_Single_line_infor=Stock_list_Single_line.split('|')
            print Stock_Single_line_infor[Stock_name_Symbol_position]+'  Stock_Market_Category  '+Stock_Single_line_infor[Stock_name_Market_Category_position]
            try:
                json.dumps(getQuotes(Stock_Single_line_infor[Stock_name_Symbol_position]))
         
        
    def Yahoo_finance_acquire(self):
        

    def Print_infor(self):
         