import urllib2
from bs4 import BeautifulSoup  # used for decode the html data


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
    
    def GetRealTimeVolumePrice(self,stock_symbol):
        sectionID = 'symbol'
        fullurl = self.Nasdaqmainurl + sectionID + '/' + stock_symbol+'/'+'time-sales?time=1'
        print fullurl
        try:
            urllib2.socket.setdefaulttimeout(20)
            urlrequest = urllib2.Request(fullurl)
            urlresponse = urllib2.urlopen(urlrequest)
            urlpage = urlresponse.read()
            pagesoup = BeautifulSoup(urlpage,"lxml")
            self.__GetNumofPageRealTime(pagesoup_in=pagesoup)
            #print pagesoup
            tablepage= pagesoup.find_all("div", {"class", "genTable"})[0].find("table")#find('table',id="AfterHoursPagingContents_Table")#,{"id","AfterHoursPagingContents_Table"})
            #print tablepage
            #print tablepage.find('thead')
            for trs in tablepage.find_all('tr'):
                time   = trs.find_all()[0].text
                price  = trs.find_all()[1].text
                volume = trs.find_all()[2].text
                print time +' '+price+ ' '+volume
        except:
            print 'error'
    def GetRealTimePreMaket(self,stock_symbol):
        sectionID = 'symbol'
        fullurl = self.Nasdaqmainurl + sectionID + '/' + stock_symbol+'/'+'premarket'
        print fullurl
        try:
            urllib2.socket.setdefaulttimeout(20)
            urlrequest = urllib2.Request(fullurl)
            urlresponse = urllib2.urlopen(urlrequest)
            urlpage = urlresponse.read()
            pagesoup = BeautifulSoup(urlpage,"lxml")
            #self.__GeNumofPagePreMaket(pagesoup_in=pagesoup)
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
                print time +' '+price+' '+volume
                #print trs.find_all()[1].text.split()[1]
        except:
            print 'error in reading the premarket page'
    def GetRealTimeAfterhours(self,stock_symbol):
        sectionID = 'symbol'
        fullurl = self.Nasdaqmainurl + sectionID + '/' + stock_symbol+'/'+'after-hours'
        print fullurl
        try:
            urllib2.socket.setdefaulttimeout(20)
            urlrequest = urllib2.Request(fullurl)
            urlresponse = urllib2.urlopen(urlrequest)
            urlpage = urlresponse.read()
            pagesoup = BeautifulSoup(urlpage,"lxml")
            print self.__GetNumofPageAfterhours(stock_symbol_in=stock_symbol)

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
                print time +' '+price+' '+volume
                #print trs.find_all()[1].text.split()[1]
        except:
            print 'error'    
    def Test_Functions(self):
        print "test function"
        
    def __GetNumofPageAfterhours(self,stock_symbol_in=None,pagesoup_in=None):
        if stock_symbol_in is None and pagesoup_in is None:
            print 'Function Error'
            exit(-1)
        if pagesoup_in is not None:
            tablepage= pagesoup_in.find_all("div", {"id": "pagerContainer"})[0].find_all('li')#find('table',id="AfterHoursPagingContents_Table")#,{"id","AfterHoursPagingContents_Table"})
            numberofpage=len(tablepage)-4
            if  numberofpage> 0:
                return int(tablepage[-3].get_text())
                #return  int(numberofpage)
            else:
                return int(1)
        if pagesoup_in is None and stock_symbol_in is not None:
            sectionID = 'symbol'
            fullurl = self.Nasdaqmainurl + sectionID + '/' + stock_symbol_in+'/'+'after-hours'
            print fullurl
            try:
                urllib2.socket.setdefaulttimeout(20)
                urlrequest = urllib2.Request(fullurl)
                urlresponse = urllib2.urlopen(urlrequest)
                urlpage = urlresponse.read()
                pagesoup = BeautifulSoup(urlpage,"lxml")
                return int(self.__GetNumofPageAfterhours(pagesoup_in=pagesoup))
            except:
                print 'error get page number'
    
    def __GeNumofPagePreMaket(self,stock_symbol_in=None,pagesoup_in=None):
        if stock_symbol_in is None and pagesoup_in is None:
            print 'Function Error'
            exit(-1)
        if pagesoup_in is not None:
            tablepage= pagesoup_in.find_all("div", {"id": "pagerContainer"})[0].find_all('li')#find('table',id="AfterHoursPagingContents_Table")#,{"id","AfterHoursPagingContents_Table"})
            numberofpage=len(tablepage)-4
            if  numberofpage> 0:
                return int(tablepage[-3].get_text())
                #return  int(numberofpage)
            else:
                return int(1)
        if pagesoup_in is None and stock_symbol_in is not None:
            sectionID = 'symbol'
            fullurl = self.Nasdaqmainurl + sectionID + '/' + stock_symbol_in+'/'+'premarket'
            print fullurl
            try:
                urllib2.socket.setdefaulttimeout(20)
                urlrequest = urllib2.Request(fullurl)
                urlresponse = urllib2.urlopen(urlrequest)
                urlpage = urlresponse.read()
                pagesoup = BeautifulSoup(urlpage,"lxml")
                return int(self.__GetNumofPageAfterhours(pagesoup_in=pagesoup))
            except:
                print 'error get page number'
    def __GetNumofPageRealTime(self,stock_symbol_in=None,pagesoup_in=None):
        if stock_symbol_in is None and pagesoup_in is None:
            print 'Function Error'
            exit(-1)
        if pagesoup_in is not None:  
            tablepage= pagesoup_in.find_all("ul", {"class": "pager"})[0].find_all('li')
            numberofpage=len(tablepage)-4
            if  numberofpage> 0:
                #print tablepage[-3].get_text()
                return  int(tablepage[-3].get_text())
            else:
                return int(1)
        if pagesoup_in is None and stock_symbol_in is not None:
            sectionID = 'symbol'
            fullurl = self.Nasdaqmainurl + sectionID + '/' + stock_symbol_in+'/'+'time-sales?time=1'
            print fullurl
            try:
                urllib2.socket.setdefaulttimeout(20)
                urlrequest = urllib2.Request(fullurl)
                urlresponse = urllib2.urlopen(urlrequest)
                urlpage = urlresponse.read()
                pagesoup = BeautifulSoup(urlpage,"lxml")
                return int(self.__GetNumofPageAfterhours(pagesoup_in=pagesoup))
            except:
                print 'error get page number'   
                
if __name__ == '__main__':
    print 'run as main functions'
    a = Nasdaq_realtimeData() 
    a.GetRealTimeAfterhours(stock_symbol='AAPL')
    a.GetRealTimeVolumePrice(stock_symbol='AAPL')
    a.GetRealTimePreMaket('AAPL')
