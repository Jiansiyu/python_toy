import urllib2
from bs4 import BeautifulSoup  # used for decode the html data
from datetime import datetime, timedelta
import socket
#from DataBase_interface.mysql_interface import mysql_interface


import sys
#from __builtin__ import str
sys.path.append('../DataBase_interface')
sys.path.append('../Internet_config')
sys.path.append('../Data/cfg')
from Internet_prox import Internet_prox
from mysql_interface import mysql_interface
from config import STOCK_SCAN_IPPROX_MAXRETRYTIMES

from Nasdaq_tool import  Nasdaq_tool

class Nasdaq_realtimeData(object):
    def __init__(self, *args, **kwargs):
        print "nasdaq"
        self.Nasdaqmainurl = 'http://www.nasdaq.com/'
        
    def GetSummaryQuote(self, stock_symbol):
        summary_result= {
                      "1 Year Target": None, 
                      "Today's High":None,
                      "Today's Low":None,
                      "Share Volume": None, 
                      "90 Day Avg. Daily Volume": None, 
                      "Previous Close": None, 
                      "52 Week High": None,
                      "52 Week Low": None, 
                      "Market cap": None, 
                      "P/E Ratio": None, 
                      "Forward P/E(1y)": None, 
                      "Earnings Per Share (EPS)": None,
                      "Annualized dividend": None,
                      "Ex Dividend Date": None,
                      "Dividend Payment Date": None,
                      "Current Yield": None,
                      "Beta": None}
        SummaryQuote_infor_list = {
                      "1 Year Target": None, 
                      "Today's High /Low":None,
                      "Share Volume": None, 
                      "90 Day Avg. Daily Volume": None, 
                      "Previous Close": None, 
                      "52 Week High/Low": None, 
                      "Market cap": None, 
                      "P/E Ratio": None, 
                      "Forward P/E(1y)": None, 
                      "Earnings Per Share (EPS)": None,
                      "Annualized dividend": None,
                      "Ex Dividend Date": None,
                      "Dividend Payment Date": None,
                      "Current Yield": None,
                      "Beta": None}
        sectionID = 'symbol'
        fullurl = self.Nasdaqmainurl + sectionID + '/' + stock_symbol
        print fullurl
        try:
            urllib2.socket.setdefaulttimeout(20)
            urlrequest = urllib2.Request(fullurl)
            urlresponse = urllib2.urlopen(urlrequest)
            urlpage = urlresponse.read()
            # print urlpage
            pagesoup = BeautifulSoup(urlpage,"lxml")
            
            summaryQuateTanble = pagesoup.find_all("div", {"class", "genTable thin"})[0].find("table")  # .find_all("a")
            
            # print  summaryQuateTanble
            # decode the table
            for row in summaryQuateTanble.find_all("tr"):
                td_tags = row.find_all("td")
                #print len(td_tags)
                if len(td_tags) is 2:
                    # get the name
                    for span in td_tags[0].findAll('span'):
                        span.replace_with('')
                    term_name=td_tags[0].get_text().lstrip().rstrip()
                    #print "name  :" + term_name
                    if term_name in SummaryQuote_infor_list.keys():#SummaryQuote_infor_list:
                        SummaryQuote_infor_list[term_name]=td_tags[1].get_text().lstrip().rstrip()
                else:
                    print "table error"
                
        except:
            print 'error'
        
        for keys in SummaryQuote_infor_list.keys():
            if keys in summary_result.keys():
                summary_result[keys]=SummaryQuote_infor_list[keys]
        summary_result["Today's High"] = SummaryQuote_infor_list["Today's High /Low"].split()[1]
        summary_result["Today's Low"]  = SummaryQuote_infor_list["Today's High /Low"].split()[-1]
        summary_result["52 Week High"] = SummaryQuote_infor_list["52 Week High/Low"].split()[1]
        summary_result["52 Week Low"]  = SummaryQuote_infor_list["52 Week High/Low"].split()[-1]
        summary_result["Market cap"]   = SummaryQuote_infor_list["Market cap"].split()[-1] 
        summary_result["Earnings Per Share (EPS)"]   = SummaryQuote_infor_list["Earnings Per Share (EPS)"].split()[-1]
        summary_result["Previous Close"]   = SummaryQuote_infor_list["Previous Close"].split()[-1]
        summary_result["Annualized dividend"]   = SummaryQuote_infor_list["Annualized dividend"].split()[-1]
        #summary_result["Previous Close"]   = SummaryQuote_infor_list["Previous Close"].split()[-1]
        
        for keys in summary_result.keys():
            print keys + "   "+summary_result[keys]
        return summary_result
    def SaveRealTimeVolumePrice(self,stock_symbol):
        print 'Get ' +stock_symbol
        RealTimeVolumePrice_result=self.GetRealTimeVolumePrice(stock_symbol=stock_symbol)
        saveline=mysql_interface()
        saveline.Save(databasename_in=stock_symbol, save_data_in=RealTimeVolumePrice_result, table_name='realtimequote', user='test', passcode='123456')
        
    def GetRealTimeVolumePrice(self,stock_symbol):
        print ''
        RealTimeVolumePrice_result=[]
        time_range_code=0
        if datetime.now().time() < datetime.now().replace(hour=9,minute=30,second=0).time() or datetime.now().time() > datetime.now().replace(hour=16,minute=0,second=0).time():
            time_range_code=13
        else:
            time_range_code=(datetime.now()- datetime.now().replace(hour=9,minute=30,second=0)).seconds/3600+1

        for time_code in range(1,time_range_code+1):
            
            NumofPage=self.__GetNumofPageRealTimeVolumePrice(stock_symbol_in=stock_symbol, time_range_code=time_code)
            print str(time_code)+' page:'+str(NumofPage)
            for pageid in range(1,NumofPage+1):
                page_result=self.GetRealTimeVolumePrice_singletime_singlepage(stock_symbol=stock_symbol, page_id=pageid, time_range_code=time_code)
                for single_line_result in page_result:
                    RealTimeVolumePrice_result.append(single_line_result)
        print stock_symbol.upper()+' :: '+ str(len(RealTimeVolumePrice_result))+' realtime trade record detected'    
        print reversed(RealTimeVolumePrice_result)  
        return reversed(RealTimeVolumePrice_result)            
    def GetRealTimeVolumePrice_singletime_singlepage(self,stock_symbol,page_id=None,time_range_code=None):

        error_counter=0
        if time_range_code is None:
            time_id=0
        if time_range_code >=0 and time_range_code <=13:
            time_id=time_range_code
        else:
            print 'ERROR unrecognized time_range_code ...... set it to 0'
            time_id=0
        if page_id is None:
            page_id=1
        sectionID = 'symbol'
        fullurl = self.Nasdaqmainurl + sectionID + '/' + stock_symbol.lower()+'/'+'time-sales?time='+format(str(time_id))+'&pageno='+str(page_id)
        
        page_result=[]
        try:
            urllib2.socket.setdefaulttimeout(20)
            proxy = urllib2.ProxyHandler({'http': Internet_prox().GetProx()})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
            urlrequest = urllib2.Request(fullurl)
            urlresponse = urllib2.urlopen(urlrequest)
            urlpage = urlresponse.read()
            pagesoup = BeautifulSoup(urlpage,"lxml")
            #print self.__GetNumofPageRealTimeVolumePrice(stock_symbol_in='aapl',time_range_code=2)#, time_range_code, pagesoup_in)(pagesoup_in=pagesoup)
            #print pagesoup
            tablepage= pagesoup.find_all("div", {"class", "genTable"})[0].find("table")#find('table',id="AfterHoursPagingContents_Table")#,{"id","AfterHoursPagingContents_Table"})
            #print tablepage
            #print tablepage.find('thead')
            for trs in tablepage.find_all('tr'):
                time   = trs.find_all()[0].text
                price  = trs.find_all()[1].text.split()[1]
                volume = trs.find_all()[2].text
                try:
                    trade_time=datetime.now().replace(hour=int(time.split(':')[0]),minute=int(time.split(':')[1]),second=int(time.split(':')[2]))
                    trade_time=Nasdaq_tool().GetTradeTimeStamp_realtime(datetime_in=trade_time)
                    trade_price=float(price.replace(' ', '').replace(',', ''))
                    trade_volume=int(volume.replace(' ', '').replace(',', ''))
                    single_line_final_data=(stock_symbol,trade_time,trade_price,trade_volume,datetime.now())
                    page_result.append(single_line_final_data)
                    #print single_line_final_data
                except:
                    error_counter=error_counter+1
        except:
            print 'error'
        print fullurl+' :: <'+str(len(page_result))+'> infors are detected   error-counter:'+str(error_counter)
        return page_result
    
    def SaveRealTimePreMaket(self,stock_symbol):
        print 'Get ' +stock_symbol
        PreMaket_result=self.GetRealTimePreMaket(stock_symbol=stock_symbol)
        saveline=mysql_interface()
        saveline.Save(databasename_in=stock_symbol, save_data_in=PreMaket_result, table_name='premarketquote', user='test', passcode='123456')
        
    def GetRealTimePreMaket(self,stock_symbol):
        print ' '
        NumofPage=self.__GeNumofPagePreMaket(stock_symbol_in=stock_symbol)
        RealTimeAfterhours_result=[]
        for pageid in range(1,NumofPage+1):
            page_result=self.GetRealTimePreMaket_singlepage(stock_symbol=stock_symbol, page_id=pageid)
            for single_line_result in page_result:
                #print single_line_result
                RealTimeAfterhours_result.append(single_line_result) 
        
        print stock_symbol.upper()+' :: '+ str(len(RealTimeAfterhours_result))+' premarket trade record detected'
        return reversed(RealTimeAfterhours_result)
    
    def GetRealTimePreMaket_singlepage(self,stock_symbol,page_id=None):
        if page_id is None:
            page_id=1
        sectionID = 'symbol'
        fullurl = self.Nasdaqmainurl + sectionID + '/' + stock_symbol.lower()+'/'+'premarket'+'?page='+str(page_id)
        #print fullurl
        page_result=[]
        try:
            urllib2.socket.setdefaulttimeout(20)
            proxy = urllib2.ProxyHandler({'http': Internet_prox().GetProx()})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
            urlrequest = urllib2.Request(fullurl)
            urlresponse = urllib2.urlopen(urlrequest)
            urlpage = urlresponse.read()
            pagesoup = BeautifulSoup(urlpage,"lxml")
            #self.__GeNumofPagePreMaket(pagesoup_in=pagesoup)
            tablepage= pagesoup.find_all("div", {"class", "genTable"})[1].find("table")#find('table',id="AfterHoursPagingContents_Table")#,{"id","AfterHoursPagingContents_Table"})
            
            for trs in tablepage.find_all('tr'):
                tds= trs.find_all()
                time    = ''
                price   = ''
                volume  = ''
                if len(tds) is 3:
                    time   = tds[0].text
                    price  = tds[1].text.split()[1]
                    volume = tds[2].text
                elif len(tds) is 4:
                    time   = tds[0].text
                    price  = tds[1].text.split()[1]
                    volume = tds[-1].text
                #print time +' '+price+' '+volume
                try:
                    trade_time=datetime.now().replace(hour=int(time.split(':')[0]),minute=int(time.split(':')[1]),second=int(time.split(':')[2]))
                    trade_time=Nasdaq_tool().GetTradeTimeStamp_realtime(datetime_in=trade_time)
                    trade_price=float(price.replace(' ', '').replace(',', ''))
                    trade_volume=int(volume.replace(' ', '').replace(',', ''))
                    single_line_final_data=(stock_symbol,trade_time,trade_price,trade_volume,datetime.now())
                    page_result.append(single_line_final_data)
                except:
                    print "error in decoding the value (premarket)"                
        except:
            print 'error in reading the premarket page'
        return page_result
            
    def SaveRealTimeAfterhours(self,stock_symbol=None, result=None):
        print 'Get ' +stock_symbol
        Afterhours_result=self.GetRealTimeAfterhours(stock_symbol=stock_symbol)
        saveline=mysql_interface()
        saveline.Save(databasename_in=stock_symbol, save_data_in=Afterhours_result, table_name='afterhoursquote', user='test', passcode='123456')
        
        
    def GetRealTimeAfterhours(self,stock_symbol):
        NumofPage=self.__GetNumofPageAfterhours(stock_symbol_in=stock_symbol)
        print NumofPage
        print str(NumofPage)+'  pages detected'
        RealTimeAfterhours_result=[]
        for pageid in range(1,NumofPage+1):
            page_result=self.GetRealTimeAfterhours_singlepage(stock_symbol=stock_symbol, page_id=pageid)
            for single_line_result in page_result:
                #print single_line_result
                RealTimeAfterhours_result.append(single_line_result) 
        print stock_symbol.upper()+' :: '+ str(len(RealTimeAfterhours_result))+' after hour trade record detected'
        return reversed(RealTimeAfterhours_result)    
            
    def GetRealTimeAfterhours_singlepage(self,stock_symbol,page_id=None,retry_counter=None):
        if retry_counter is None:
            retry_counter=0 
        if retry_counter > STOCK_SCAN_IPPROX_MAXRETRYTIMES:
            ERROR=[]
            print 'ERROR  reach max retry times, check the esistance of the SYMBOL or check the internet connection'
            return ERROR
        if page_id is None:
            page_id=1
        sectionID = 'symbol'
        fullurl = self.Nasdaqmainurl + sectionID + '/' + stock_symbol.lower()+'/'+'after-hours'+'?page='+str(page_id)
        page_result=[]
        
        try:
            urllib2.socket.setdefaulttimeout(5)
            proxy = urllib2.ProxyHandler({'http': Internet_prox().GetProx()})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
            urlrequest = urllib2.Request(fullurl)
            urlresponse = urllib2.urlopen(urlrequest)
            urlpage = urlresponse.read()
            pagesoup = BeautifulSoup(urlpage,"lxml")
            #print self.__GetNumofPageAfterhours(stock_symbol_in=stock_symbol)
            #print pagesoup
            tablepage= pagesoup.find_all("div", {"class", "genTable"})[1].find("table")#find('table',id="AfterHoursPagingContents_Table")#,{"id","AfterHoursPagingContents_Table"})
            #print tablepage
            #print tablepage.find('thead')
            for trs in tablepage.find_all('tr'):
                tds= trs.find_all()
                time    = ''
                price   = ''
                volume  = ''
                if len(tds) is 3:
                    time   = tds[0].text
                    price  = tds[1].text.split()[1]
                    volume = tds[2].text
                elif len(tds) is 4:
                    time   = tds[0].text
                    price  = tds[1].text.split()[1]
                    volume = tds[-1].text
                try:
                    trade_time=datetime.now().replace(hour=int(time.split(':')[0]),minute=int(time.split(':')[1]),second=int(time.split(':')[2]))
                    trade_time=Nasdaq_tool().GetTradeTimeStamp_realtime(datetime_in=trade_time)
                    trade_price=float(price.replace(' ', '').replace(',', ''))
                    trade_volume=int(volume.replace(' ', '').replace(',', ''))
                    single_line_final_data=(stock_symbol,trade_time,trade_price,trade_volume,datetime.now())
                    page_result.append(single_line_final_data)
                    #print single_line_final_data
                except:
                    print "error in decoding the value"
            return page_result
        except urllib2.HTTPError, e:
            print 'HTTPError = ' + str(e.code)
            return self.GetRealTimeAfterhours_singlepage(stock_symbol=stock_symbol, page_id=page_id,retry_counter=retry_counter)
        except urllib2.URLError, e:
            print 'URLError = ' + str(e.reason)
            return self.GetRealTimeAfterhours_singlepage(stock_symbol=stock_symbol, page_id=page_id,retry_counter=retry_counter)
        except socket.timeout, e:
            print 'URLError = ' + str(e)
            return self.GetRealTimeAfterhours_singlepage(stock_symbol=stock_symbol, page_id=page_id,retry_counter=retry_counter)    
        except Exception, e:
            print 'error '+str( e)
            return self.GetRealTimeAfterhours_singlepage(stock_symbol=stock_symbol, page_id=page_id,retry_counter=retry_counter)
        except:
            print 'Unknown error in decoding'
            return self.GetRealTimeAfterhours_singlepage(stock_symbol=stock_symbol, page_id=page_id,retry_counter=retry_counter)
        
    def test(self,stock_symbol,page_id=None):  
        if page_id is None:
            page_id=1
        sectionID = 'symbol'
        #fullurl = 'http://www.nasdaq.com/symbol/aapl/after-hours?page=2'
        fullurl = self.Nasdaqmainurl + sectionID + '/' + stock_symbol.lower()+'/'+'after-hours'+'?page='+str(page_id)
        #print fullurl
        
        
        urllib2.socket.setdefaulttimeout(20)
        proxy = urllib2.ProxyHandler({'http': Internet_prox().GetProx()})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        urlrequest = urllib2.Request(fullurl)
        urlresponse = urllib2.urlopen(urlrequest)
        urlpage = urlresponse.read()
        pagesoup = BeautifulSoup(urlpage,"lxml")
            #print self.__GetNumofPageAfterhours(stock_symbol_in=stock_symbol)
            #print pagesoup
        tablepage= pagesoup.find_all("div", {"class", "genTable"})[1].find("table")#find('table',id="AfterHoursPagingContents_Table")#,{"id","AfterHoursPagingContents_Table"})
            #print tablepage
            #print tablepage.find('thead')
        for trs in tablepage.find_all('tr'):
            tds= trs.find_all()
            time    = ''
            price   = ''
            volume  = ''
            if len(tds) is 3:
                time   = tds[0].get_text()
                price  = tds[1].get_text().split()[1]
                volume = tds[2].get_text()
            elif len(tds) is 4:
                time   = tds[0].get_text()
                price  = tds[1].get_text().split()[1]
                volume = tds[-1].get_text()
            print time +' '+price+' '+volume
            try:
                trade_time=datetime.now().replace(hour=int(time.split(':')[0].encode('utf-8')),minute=int(time.split(':')[1].encode('utf-8')),second=int(time.split(':')[2].encode('utf-8')))
                print trade_time
            except:
                print "text"
            
    def __GetNumofPageAfterhours(self,stock_symbol_in=None,pagesoup_in=None,retry_counter=None):
        if retry_counter is None:
            retry_counter=0
        #print '\nGet Page Number afterhour.... '
        if retry_counter > STOCK_SCAN_IPPROX_MAXRETRYTIMES:
            #print 'ERROR  reach max retry times in GET PAGE NUMBER, RETURN 0'
            return int(0)
        if stock_symbol_in is None and pagesoup_in is None:
            print 'Function Error'
            exit(-1)

        if pagesoup_in is not None:
            #print 'decode page soup'
            #print 'lala'
            
            try:
                tablepage= pagesoup_in.find_all("div")#find('table',id="AfterHoursPagingContents_Table")#,{"id","AfterHoursPagingContents_Table"})
            except:
                #print 'page soup maybe empty'
                self.__GetNumofPageAfterhours(stock_symbol_in=stock_symbol_in,retry_counter=retry_counter+1)
                
            tablepage= pagesoup_in.find_all("div", {"id": "pagerContainer"})[0].find_all('li')    
            numberofpage=len(tablepage)-4
            if  numberofpage> 0:
                
                pagenumber = int(tablepage[-3].get_text())
                #print 'where i am************ '
                #print pagenumber
                return pagenumber
                #print pagenumber
            else:
                #print 'where i am 1   '+ str(numberofpage)
                return int(1)
        #print 'where i am 222333'
        if pagesoup_in is None and stock_symbol_in is not None:
            
            sectionID = 'symbol'
            fullurl = self.Nasdaqmainurl + sectionID + '/' + stock_symbol_in.lower()+'/'+'after-hours'
            print fullurl
            req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                              'Accept':'text/html;q=0.9,*/*;q=0.8',
                              'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                              'Accept-Encoding':'gzip',
                              'Connection':'close',
                              'Referer':None
                              }
            try:
                urllib2.socket.setdefaulttimeout(5)
                proxy = urllib2.ProxyHandler({'http': Internet_prox().GetProx()})
                opener = urllib2.build_opener(proxy)
                urllib2.install_opener(opener)
                #urlrequest =urllib2.Request(url=fullurl, data=None, headers=req_header)
                urlrequest = urllib2.Request(fullurl)
                urlresponse = urllib2.urlopen(urlrequest)
                urlpage = urlresponse.read()
                pagesoup = BeautifulSoup(urlpage,"lxml")
                return self.__GetNumofPageAfterhours(stock_symbol_in=stock_symbol_in,pagesoup_in=pagesoup)
            except urllib2.HTTPError, e:
                print 'HTTPError = ' + str(e.code)
                return self.__GetNumofPageAfterhours(stock_symbol_in=stock_symbol_in,retry_counter=retry_counter+1)
            except urllib2.URLError, e:
                print 'URLError = ' + str(e.reason)
                return self.__GetNumofPageAfterhours(stock_symbol_in=stock_symbol_in,retry_counter=retry_counter+1)
            except socket.timeout, e:
                print 'URLError = ' + str(e)
                return self.__GetNumofPageAfterhours(stock_symbol_in=stock_symbol_in,retry_counter=retry_counter+1)    
            except:
                print 'Unknown error get page number afterhour with return 1......'
                return self.__GetNumofPageAfterhours(stock_symbol_in=stock_symbol_in,retry_counter=retry_counter+1)    
            
    def __GeNumofPagePreMaket(self,stock_symbol_in=None,pagesoup_in=None,retry_counter=None):
        
        '''
        '''
        # control the max retry times
        if retry_counter is None:
            retry_counter=0
        if retry_counter > STOCK_SCAN_IPPROX_MAXRETRYTIMES:
            print 'ERROR  reach max retry times in GET PAGE NUMBER, RETURN 0'
            return int(0)   
        
        if stock_symbol_in is None and pagesoup_in is None:
            print 'Function Error'
            exit(-1)
        
        if pagesoup_in is not None:
            try:
                tablepage=pagesoup_in.find_all("div")
            except:
                self.__GeNumofPagePreMaket(stock_symbol_in=stock_symbol_in, retry_counter=retry_counter+1)
                
            tablepage= pagesoup_in.find_all("div", {"id": "pagerContainer"})[0].find_all('li')#find('table',id="AfterHoursPagingContents_Table")#,{"id","AfterHoursPagingContents_Table"})
            numberofpage=len(tablepage)-4
            if  numberofpage> 0:
                return int(tablepage[-3].get_text())
            else:
                return int(1)
            
        if pagesoup_in is None and stock_symbol_in is not None:
            
            sectionID = 'symbol'
            fullurl = self.Nasdaqmainurl + sectionID + '/' + stock_symbol_in.lower()+'/'+'premarket'
            print fullurl
            try:
                urllib2.socket.setdefaulttimeout(20)
                proxy = urllib2.ProxyHandler({'http': Internet_prox().GetProx()})
                opener = urllib2.build_opener(proxy)
                urllib2.install_opener(opener)
                urlrequest = urllib2.Request(fullurl)
                urlresponse = urllib2.urlopen(urlrequest)
                urlpage = urlresponse.read()
                pagesoup = BeautifulSoup(urlpage,"lxml")
                return int(self.__GeNumofPagePreMaket(pagesoup_in=pagesoup, retry_counter=retry_counter+1))
            except:
                #print 'error get page number'
                return int(self.__GeNumofPagePreMaket(pagesoup_in=pagesoup, retry_counter=retry_counter+1))
    def __GetNumofPageRealTimeVolumePrice(self,stock_symbol_in=None,time_range_code=None,pagesoup_in=None):
        if stock_symbol_in is None and pagesoup_in is None:
            print 'Function Error'
            exit(-1)
        if pagesoup_in is not None: 
            tablepage= pagesoup_in.find_all("ul", {"class": "pager"})[0].find_all('li')
            numberofpage=len(tablepage)-4
            if  numberofpage> 0:
                return  int(tablepage[-3].get_text())
            else:
                return int(1)
        if pagesoup_in is None and stock_symbol_in is not None:
            
            if time_range_code is None:
                time_id=0
            if time_range_code >=0 and time_range_code <=13:
                time_id=time_range_code            
            sectionID = 'symbol'
            fullurl = self.Nasdaqmainurl + sectionID + '/' + stock_symbol_in.lower()+'/'+'time-sales?time='+format(str(time_id))
            try:
                urllib2.socket.setdefaulttimeout(20)
                proxy = urllib2.ProxyHandler({'http': Internet_prox().GetProx()})
                opener = urllib2.build_opener(proxy)
                urllib2.install_opener(opener)
                urlrequest = urllib2.Request(fullurl)
                urlresponse = urllib2.urlopen(urlrequest)
                urlpage = urlresponse.read()
                pagesoup = BeautifulSoup(urlpage,"lxml")
                return int(self.__GetNumofPageRealTimeVolumePrice(pagesoup_in=pagesoup))
            except:
                print 'error get page number'  
                return int(1) 
                
if __name__ == '__main__':
    print 'run as main functions'
    #print  Internet_prox().GetProx()
    a = Nasdaq_realtimeData() 
    #a.GetRealTimeAfterhours_singlepage(stock_symbol='AAPL')
    a.GetRealTimeAfterhours(stock_symbol='GOOGL')
    #a.GetRealTimePreMaket(stock_symbol='AAPL')
    #a.SaveRealTimeVolumePrice(stock_symbol='aapl')
    #a.GetRealTimePreMaket(stock_symbol='aapl')
    #a.GetRealTimeVolumePrice(stock_symbol='a')
    #a.GetRealTimeVolumePrice_singletime_singlepage(stock_symbol='aapl', page_id=1, time_range_code=2)
    #print a.__GetNumofPageRealTimeVolumePrice(stock_symbol_in='aapl')