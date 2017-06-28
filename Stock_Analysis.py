# from pandas_datareader import data
# from googlefinance import getQuotes
# #import graphlib
#  
# #read the nasdaq componies name 
# Stock_list_filename='nasdaqlisted.txt'
# data_path='NasdaqListed'
# 
# with open(Stock_list_filename) as Stock_list_io:
#     Stock_list_lines=Stock_list_io.readlines()
# #get the nasdaq systerm infor
# Stock_header_infor=Stock_list_lines[0].split('|')
# Symbol_position =  Stock_header_infor.index('Symbol')
# Security_name_position=Stock_header_infor.index('Security Name')
# Market_Category_position=Stock_header_infor.index('Market Category')
# Financial_Status_position=Stock_header_infor.index('Financial Status')
# ETF_position=Stock_header_infor.index('ETF')
# #print Symbol_position
# # get the individual nasdaq conpany name
# for Single_line in Stock_list_lines:
#     Stock_infor=Single_line.split('|')
#     print Stock_infor[Symbol_position]+' Security name=>'+Stock_infor[Security_name_position]
#     try:
#         stock_data=data.DataReader(Stock_infor[Symbol_position], 'google','1980-01-01')
#         stock_data.to_csv(data_path+'/'+Stock_infor[Symbol_position]+'.csv')
#     except:
#         with open('errorlog.log','a') as error_log:
#             error_log.writelines(Stock_list_filename+'   Error in' +Stock_infor[Symbol_position]+' Security name=>'+Stock_infor[Security_name_position])
#             error_log.close()
#             print '[ERROR] '+Stock_infor[Symbol_position]+' Security name=>'+Stock_infor[Security_name_position]
#              
#              

from Stock_DataAcquire import Stock_DataAcquire
from Zack_Rank_Aquire import Zack_Spyder

from Stock_DataAcquire import Stock_DataAcquire
A=Stock_DataAcquire()
#A.Google_finance_acquire()
A.Pandas_Data_acquire()

# Zack_Spyder test

Zack_Spyder_test=Zack_Spyder();
#Zack_Spyder_test.Zack_Rank_aquire('AAPL')
Zack_Spyder_test.Zack_csv_addrank('Prediction.csv')
#Zack_Spyder_test.Zack_Rank_stock('CMTL')