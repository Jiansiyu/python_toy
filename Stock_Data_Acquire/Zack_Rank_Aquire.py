#
#    Python toy spyder used for get the Zack Stock Rank 
#    By Siyu Jun 7 @ JLab
#

import urllib2
#import socket
import csv      #csv interface

from bs4 import BeautifulSoup  # used for decode the html data
from docutils.nodes import row
#from Tix import ROW


class Zack_Spyder(object):
    def __init__(self):
        print 'Zacks Stock Spyder'
        self.debug_glag = False
        
    #used for get the stock ranck from zack
    def Zack_Rank_aquire(self,stock_symble=None):
        if stock_symble is not None:
            print self.__Zack_Rank_stock(stock_symble)
        else:
            print 'single mode'
    
    # used for input any file, read the symble and add rank into the files
    def Zack_csv_addrank(self,csv_filename):
        if csv_filename is None:
            print 'Please input the csv file name that need to add the rank data'
        else:
            #print 'add the rank data input the csv files'
            csv_symble_header='symbles'
            with open(csv_filename,'r') as csvinput:
                with open('out.csv','w') as cvsoutput:
                    writer=csv.writer(cvsoutput,lineterminator='\n')
                    reader=csv.reader(csvinput)
                    
                    all=[]
                    row = next(reader)
                    row.append('Rank')
                    row.append('Value')
                    row.append('Growth')
                    row.append('Momentum')
                    row.append('VGM')
                    all.append(row)
                    
                    for row in reader:
                        print 'read '+row[0]+'.....'
                        #row.append(row[0])
                        try:
                            Result_stock=self.__Zack_Rank_stock(row[0])
                            row.append(Result_stock['rank'])
                            row.append(Result_stock['value'])
                            row.append(Result_stock['growth'])
                            row.append(Result_stock['momentum'])
                            row.append(Result_stock['vgm'])
                        except:
                            print 'error'
                        all.append(row)
                    writer.writerows(all)  

        
    def __Zack_Rank_stock(self,stock_symble):
        # apply the url request for get the stock rank
        base_url='https://www.zacks.com/stock/quote/'
        full_url=base_url+stock_symble
        print full_url
        try:
            urllib2.socket.setdefaulttimeout(20)   # set the defult timeout
            urlrequest=urllib2.Request(full_url)
            urlresponse=urllib2.urlopen(urlrequest)
            urlpage=urlresponse.read()
            
            pagesoup=BeautifulSoup(urlpage)
            rank_box=pagesoup.select('.rank_container_right')[0]
            
            Result_Rank     = rank_box.select('.zr_rankbox')[0].get_text().strip().split()[-1]
            Result_Value    = rank_box.select('.composite_group')[0].select('.composite_val')[0].get_text()
            Result_Growth   = rank_box.select('.composite_group')[0].select('.composite_val')[1].get_text()
            Result_Momentum = rank_box.select('.composite_group')[0].select('.composite_val')[2].get_text()
            Result_VGM      = rank_box.select('.composite_group')[0].select('.composite_val')[3].get_text()
        except:
            print 'Error reading' + stock_symble
            
        if self.debug_glag is True:
                print 'Rank:'+rank_box.select('.zr_rankbox')[0].get_text().strip().split()[1]
                print 'Value: '+rank_box.select('.composite_group')[0].select('.composite_val')[0].get_text()
                print 'Growth: '+rank_box.select('.composite_group')[0].select('.composite_val')[1].get_text()
                print 'Momentum: '+rank_box.select('.composite_group')[0].select('.composite_val')[2].get_text()
                print 'VGM: '+rank_box.select('.composite_group')[0].select('.composite_val')[3].get_text()
        print stock_symble + '=> Rank: '+ Result_Rank + ' Value: '+Result_Value+' Growth: '+Result_Growth+' Momentum: '+Result_Momentum+' VGM: '+Result_VGM
        return {'rank':Result_Rank,'value':Result_Value,'growth':Result_Growth,'momentum':Result_Momentum,'vgm':Result_VGM}

if __name__ =='__main__':
    test=Zack_Spyder()
    test.Zack_Rank_stock('A')