'''
Created on Jun 30, 2017

@author: newdriver
'''
import urllib

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, FR


class Nasdaq_tool(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    
    def GetTradeTimeStamp_premarket(self,datetime_in):
        '''
        main motivation for this functions:
        the web site does not contain the trade date
        used for calculate the trade time
        '''
        weekno=datetime.today().weekday()
        if weekno < 5 :
            if datetime.now() > datetime.now().replace(hour=4,minute=0,second=0):
                return (datetime.now()).replace(hour=datetime_in.hour,minute=datetime_in.minute,second=datetime_in.second)
            else:
                return (datetime.now()-timedelta(days=1)).replace(hour=datetime_in.hour,minute=datetime_in.minute,second=datetime_in.second)
        else:
            return (datetime.now() + relativedelta(weekday=FR(-1))).replace(hour=datetime_in.hour,minute=datetime_in.minute,second=datetime_in.second)
        
        
    def GetTradeTimeStamp_afterhour(self,datetime_in):
        '''
        main motivation for this functions:
        the web site does not contain the trade date
        used for calculate the trade time
        '''
        weekno=datetime.today().weekday()
        if weekno < 5 :
            if datetime.now() > datetime.now().replace(hour=16,minute=0,second=0):
                return (datetime.now()).replace(hour=datetime_in.hour,minute=datetime_in.minute,second=datetime_in.second)
            else:
                return (datetime.now()-timedelta(days=1)).replace(hour=datetime_in.hour,minute=datetime_in.minute,second=datetime_in.second)
        else:
            return (datetime.now() + relativedelta(weekday=FR(-1))).replace(hour=datetime_in.hour,minute=datetime_in.minute,second=datetime_in.second)
    
    def GetTradeTimeStamp_realtime(self,datetime_in):
        '''
        main motivation for this functions:
        the web site does not contain the trade date
        used for calculate the trade time
        '''
        weekno=datetime.today().weekday()
        if weekno < 5 :
            if datetime.now() > datetime.now().replace(hour=9,minute=30,second=0):
                return (datetime.now()).replace(hour=datetime_in.hour,minute=datetime_in.minute,second=datetime_in.second)
            else:
                return (datetime.now()-timedelta(days=1)).replace(hour=datetime_in.hour,minute=datetime_in.minute,second=datetime_in.second)
        else:
            return (datetime.now() + relativedelta(weekday=FR(-1))).replace(hour=datetime_in.hour,minute=datetime_in.minute,second=datetime_in.second)
            
    def Get_Nasdaq_companylist(self,Nasdaq_ftp_nasdaqlisted=None,Nasdaq_ftp_nasdaqtraded=None,Nasdaq_ftp_nasdaqotherlist=None):

        print 'Trying to retrieve the NASDAQ company name list from server'
        
        Nasdaq_compony_list=["nasdaqlisted.txt","otherlisted.txt"] #"nasdaqtraded.txt",
        Nasdaq_ftp_baseaddr='ftp://ftp.nasdaqtrader.com/SymbolDirectory/'
        
        for componylist in Nasdaq_compony_list:
            try:
                print 'Get '+componylist + ' Save as ' + self.StockComponyListPath+componylist
                urllib.urlretrieve(Nasdaq_ftp_baseaddr+componylist, self.StockComponyListPath+componylist)
            except Exception,e:
                print e
                print '[ERROR] => Reading "'+Nasdaq_ftp_baseaddr+componylist+'"' 
        #combine the data and generate the insterest list
        InterestList= open(self.StockComponyListPath+self.stock_listfilename,'w+') # create a new file
        InterestList.write('Symbol|Security Name\n')
        InterestList.close()
        for componylist in Nasdaq_compony_list:
            try:
                with open(self.StockComponyListPath+componylist) as Stock_list_io:
                    
                    print 'Combine file "'+componylist+'"'
                    Stock_list_lines=Stock_list_io.readlines()
                    Stock_header_infor=Stock_list_lines[0].split('|')
                    #Stock_name_Symbol_position=
                    #print Stock_header_infor.index('Symbol')
                    if 'Symbol' in Stock_header_infor:
                        Symbol_position = Stock_header_infor.index('Symbol')
                    elif 'ACT Symbol' in Stock_header_infor:
                        Symbol_position = Stock_header_infor.index('ACT Symbol')
                    else:
                        continue
                    Stock_name_Security_name_position=Stock_header_infor.index('Security Name')
                    print 'Symbol_position: '+str(Symbol_position)+'  Stock_name_Security_name_position: '+str(Stock_name_Security_name_position)
                    
                    for Single_line in Stock_list_lines[1:]:
                        Stock_infor=Single_line.split('|')
                        print Stock_infor[Symbol_position]+' Security name=>'+Stock_infor[Stock_name_Security_name_position]
                        with open(self.StockComponyListPath+self.stock_listfilename,'a') as interest_list_io:
                            interest_list_io.writelines(Stock_infor[Symbol_position]+'|'+Stock_infor[Stock_name_Security_name_position]+'\n')
                            interest_list_io.close()
                
            except Exception, e:
                print e 
                
if __name__ == '__main__':
    test=Nasdaq_tool()
    print test.GetTradeTimeStamp_afterhour(datetime.now())