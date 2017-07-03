'''
Created on Jun 30, 2017

@author: newdriver
'''
import sys
from __builtin__ import str
from time import sleep
sys.path.append('../Stock_Data_Acquire')
from Nasdaq_realtimedata_spyder import Nasdaq_realtimeData
#import os.path  # used for check the existance of files
from datetime import datetime,timedelta
from multiprocessing import Pool

class Nasdaq_scan(object):
    '''
    classdocs
    '''


    def __init__(self,stock_interestlist=None):
        '''
        Constructor
        '''
        self.Stock_list=''
        if stock_interestlist is not None:
            self.stock_list=stock_interestlist
        else:
            self.stock_list = '../Data/StockList/nasdaqlisted.txt'
    
    def Nasdaq_Scanall(self,Stock_Interest_list=None):
        print '.....'
        if Stock_Interest_list is None:
            Stock_list_filename=self.stock_list
        else:
            Stock_list_filename=Stock_Interest_list
        #decode the stock compony name, and use that name to get the real time price
        with open(Stock_list_filename) as Stock_list_io:
            Stock_list_filename_lines=Stock_list_io.readlines()
            
        TotalComponyNumb=len(Stock_list_filename_lines)
        # decoder the header, and get the data strcuture of the csv file
        Stock_header_infor=Stock_list_filename_lines[0].split('|')
        Stock_name_Symbol_position=Stock_header_infor.index('Symbol')
        #Stock_name_Security_name_position=Stock_header_infor.index('Security Name')
        #Stock_name_Market_Category_position=Stock_header_infor.index('Market Category')
        starttime=datetime.now()
        print 'Current Time : '+str(starttime)
        self.iterator_couter=0
        for Stock_list_Single_line in Stock_list_filename_lines:
            Stock_Single_line_infor=Stock_list_Single_line.split('|')
            #print self.iterator_couter
            self.iterator_couter=self.iterator_couter+1
            #print Stock_Single_line_infor[Stock_name_Symbol_position]+'  Stock_Market_Category  '+Stock_Single_line_infor[Stock_name_Market_Category_position]
            try:
                #print Stock_list_filename_lines.index(Stock_list_Single_line)
                print '\n********************************'
                print 'ID =' + str(Stock_list_filename_lines.index(Stock_list_Single_line))+'/'+str(TotalComponyNumb) + '  time token: '+str(datetime.now()-starttime) \
                 +'  time remains: ' +str(TotalComponyNumb*(datetime.now()-starttime)/Stock_list_filename_lines.index(Stock_list_Single_line))
                nasdaq_interface=Nasdaq_realtimeData()
                #nasdaq_interface.GetRealTimeAfterhours(stock_symbol=Stock_Single_line_infor[Stock_name_Symbol_position])
                nasdaq_interface.SaveRealTimeAfterhours(stock_symbol=Stock_Single_line_infor[Stock_name_Symbol_position])
                #nasdaq_interface.SaveRealTimePreMaket(stock_symbol=Stock_Single_line_infor[Stock_name_Symbol_position])
                print '********************************\n'
                #nasdaq_interface.SaveRealTimePreMaket(stock_symbol=Stock_Single_line_infor[Stock_name_Market_Category_position])
                sleep(1)
            except:
                print 'retrieve error'
    def Nasdaq_premarket(self,Stock_Interest_list=None):
        print '.....'
        if Stock_Interest_list is None:
            Stock_list_filename=self.stock_list
        else:
            Stock_list_filename=Stock_Interest_list
        #decode the stock compony name, and use that name to get the real time price
        with open(Stock_list_filename) as Stock_list_io:
            Stock_list_filename_lines=Stock_list_io.readlines()
            
        TotalComponyNumb=len(Stock_list_filename_lines)
        # decoder the header, and get the data strcuture of the csv file
        Stock_header_infor=Stock_list_filename_lines[0].split('|')
        Stock_name_Symbol_position=Stock_header_infor.index('Symbol')
        #Stock_name_Security_name_position=Stock_header_infor.index('Security Name')
        #Stock_name_Market_Category_position=Stock_header_infor.index('Market Category')
        starttime=datetime.now()
        print 'Current Time : '+str(starttime)
        self.iterator_couter=0
        for Stock_list_Single_line in Stock_list_filename_lines:
            Stock_Single_line_infor=Stock_list_Single_line.split('|')
            #print self.iterator_couter
            self.iterator_couter=self.iterator_couter+1
            #print Stock_Single_line_infor[Stock_name_Symbol_position]+'  Stock_Market_Category  '+Stock_Single_line_infor[Stock_name_Market_Category_position]
            try:
                #print Stock_list_filename_lines.index(Stock_list_Single_line)
                print '\n********************************'
                print 'ID =' + str(Stock_list_filename_lines.index(Stock_list_Single_line))+'/'+str(TotalComponyNumb) + '  time token: '+str(datetime.now()-starttime) \
                 +'  time remains: ' +str(TotalComponyNumb*(datetime.now()-starttime)/Stock_list_filename_lines.index(Stock_list_Single_line))
                nasdaq_interface=Nasdaq_realtimeData()
                #nasdaq_interface.GetRealTimeAfterhours(stock_symbol=Stock_Single_line_infor[Stock_name_Symbol_position])
                #nasdaq_interface.SaveRealTimeAfterhours(stock_symbol=Stock_Single_line_infor[Stock_name_Symbol_position])
                nasdaq_interface.SaveRealTimePreMaket(stock_symbol=Stock_Single_line_infor[Stock_name_Symbol_position])
                print '********************************\n'
                #nasdaq_interface.SaveRealTimePreMaket(stock_symbol=Stock_Single_line_infor[Stock_name_Market_Category_position])
                sleep(1)
            except:
                print 'retrieve error'  
    def  Nasdaq_realtimevolumeprice(self,Stock_Interest_list=None):
        print '.....'
        if Stock_Interest_list is None:
            Stock_list_filename=self.stock_list
        else:
            Stock_list_filename=Stock_Interest_list
        #decode the stock compony name, and use that name to get the real time price
        with open(Stock_list_filename) as Stock_list_io:
            Stock_list_filename_lines=Stock_list_io.readlines()
            
        TotalComponyNumb=len(Stock_list_filename_lines)
        # decoder the header, and get the data strcuture of the csv file
        Stock_header_infor=Stock_list_filename_lines[0].split('|')
        Stock_name_Symbol_position=Stock_header_infor.index('Symbol')
        #Stock_name_Security_name_position=Stock_header_infor.index('Security Name')
        #Stock_name_Market_Category_position=Stock_header_infor.index('Market Category')
        starttime=datetime.now()
        print 'Current Time : '+str(starttime)
        self.iterator_couter=0
        for Stock_list_Single_line in Stock_list_filename_lines:
            Stock_Single_line_infor=Stock_list_Single_line.split('|')
            #print self.iterator_couter
            self.iterator_couter=self.iterator_couter+1
            #print Stock_Single_line_infor[Stock_name_Symbol_position]+'  Stock_Market_Category  '+Stock_Single_line_infor[Stock_name_Market_Category_position]
            try:
                #print Stock_list_filename_lines.index(Stock_list_Single_line)
                print '\n********************************'
                print 'ID =' + str(Stock_list_filename_lines.index(Stock_list_Single_line))+'/'+str(TotalComponyNumb) + '  time token: '+str(datetime.now()-starttime) \
                 +'  time remains: ' +str((TotalComponyNumb-Stock_list_filename_lines.index(Stock_list_Single_line))*(datetime.now()-starttime)/Stock_list_filename_lines.index(Stock_list_Single_line))
                nasdaq_interface=Nasdaq_realtimeData()
                #nasdaq_interface.GetRealTimeAfterhours(stock_symbol=Stock_Single_line_infor[Stock_name_Symbol_position])
                #nasdaq_interface.SaveRealTimeAfterhours(stock_symbol=Stock_Single_line_infor[Stock_name_Symbol_position])
                nasdaq_interface.SaveRealTimeVolumePrice(stock_symbol=Stock_Single_line_infor[Stock_name_Symbol_position])
                print '********************************\n'
                #nasdaq_interface.SaveRealTimePreMaket(stock_symbol=Stock_Single_line_infor[Stock_name_Market_Category_position])
                #sleep(1)
            except:
                print 'retrieve error'          
    def Nasdaq_realtimevolumepriceMT(self,Stock_Interest_list=None):
        print '.....'
        if Stock_Interest_list is None:
            Stock_list_filename=self.stock_list
        else:
            Stock_list_filename=Stock_Interest_list
        #decode the stock compony name, and use that name to get the real time price
        with open(Stock_list_filename) as Stock_list_io:
            Stock_list_filename_lines=Stock_list_io.readlines()
            
        TotalComponyNumb=len(Stock_list_filename_lines)
        # decoder the header, and get the data strcuture of the csv file
        Stock_header_infor=Stock_list_filename_lines[0].split('|')
        Stock_name_Symbol_position=Stock_header_infor.index('Symbol')
        #Stock_name_Security_name_position=Stock_header_infor.index('Security Name')
        #Stock_name_Market_Category_position=Stock_header_infor.index('Market Category')
        starttime=datetime.now()
        StockList=[]
        print 'Current Time : '+str(starttime)
        self.iterator_couter=0
        for Stock_list_Single_line in Stock_list_filename_lines:
            Stock_Single_line_infor=Stock_list_Single_line.split('|')
            #print self.iterator_couter
            self.iterator_couter=self.iterator_couter+1
            try:
                print 'ID =' + str(Stock_list_filename_lines.index(Stock_list_Single_line))+'/'+str(TotalComponyNumb) + '  time token: '+str(datetime.now()-starttime) \
                 +'  time remains: ' +str((TotalComponyNumb-Stock_list_filename_lines.index(Stock_list_Single_line))*(datetime.now()-starttime)/Stock_list_filename_lines.index(Stock_list_Single_line))
                StockList.append(Stock_Single_line_infor[Stock_name_Symbol_position])
            except:
                print 'retrieve error'            
        print StockList
        threadrun=Pool(100)
        threadrun.map(MT_thread,StockList)
        
def MT_thread(stock_list):
    nasdaq_interface=Nasdaq_realtimeData()
    nasdaq_interface.SaveRealTimeAfterhours(stock_symbol=stock_list)
if __name__ == '__main__':                
    a=Nasdaq_scan()
    a.Nasdaq_realtimevolumepriceMT()
        