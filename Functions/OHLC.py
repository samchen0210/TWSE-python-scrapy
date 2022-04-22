#Package import
import os
import glob
import time
import datetime
import requests
import pandas as pd
from io import StringIO
from datetime import date

def OHLC(date,stock_id):
    stock_id =str(stock_id)
    date = str(date)
    timestamp = str(time.time() * 1000 + 1000000)
    url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+ date
    #https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20210702&st
    res = requests.get(url)
    
    #"日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數
    content = res.text.replace(':[[','],[').replace("]]","],[").split('],[')
    lines = list(filter(lambda l:(len(l.split('",')) < 10) & (len(l.split('",')) > 6)))
    content = "\n".join(lines)
    
    #Index column set
    df = pd.read_csv(StringIO(content),names=["日期","成交股數",
                                              "成交金額","開盤價","最高價","最低價",
                                              "收盤價","漲跌價差","成交筆數"])
    df = df.astype(str)
    
    #Change date format (108->2019)
    d = df['日期']
    for i in range(len(d)):
        df.iloc[i]=d.iloc[i].replace(d.iloc[i][0:3], str(int(d.iloc[i][0:3]) + 1911))
        df_dt=pd.to_datetime(df.日期,format="%Y/%m/%d")
        df.set_index('日期',inplace=True)
    
    #Last Check
    df = df.apply(lambda s: s.str.replace(',', ''))
    df = df.apply(lambda s:pd.to_numeric(s, errors='coerce'))
    df = df[df.columns[df.isnull().all() == False]]
    
    #Change file directory to stock_id individual flile
    path = os.chdir('C:\\Users\\SC.210\\FinTech\\stock\\'+ stock_id)
    df.to_csv(date +'.csv',encoding='utf_8_sig')
    print(date +'.csv is downloaded!')
    
    
#Download from 2019~2020 OHLC data
def fetch_data(startyear, startmonth,stock_id):
    currentdate = datetime.datetime.today().strftime("%Y/%m/%d")
    currentyear = datetime.datetime.now().year
    currentmonth = datetime.datetime.now().month
    print('Current date: ' + str(currentdate))
    
    for i in range(startyear, currentyear+1):
        if (i != currentyear):
            for j in range(startmonth, 13):
                if j <10:
                    date = str(i)+'0'+str(j)+'01'
                    OHLC(date,stock_id)
                    time.sleep(3) #sleep for 5 secods avoid rate limiting
                else:
                    date = str(i)+str(j)+'01'
                    OHLC(date,stock_id)
                    time.sleep(3)
        else:
           for j in range(startmonth, currentmonth):
                if j <10:
                    date = str(i)+'0'+str(j)+'01'
                    OHLC(date,stock_id)
                    time.sleep(3)
                else:
                    date = str(i)+str(j)+'01'
                    OHLC(date,stock_id)
                    time.sleep(3)
        print('===========================')
        print('Download done!!')
        
def concat_csv(stock_id):
    #Enter the path where store csv files
    path = 'C:/Users/SC.210/FinTech/stock/'+str(stock_id)
    os.chdir(path)
    
    #Use glob to match the pattern ‘csv’
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    
    #Combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    
    #Export to csv
    combined_csv.to_csv( "tse_"+str(stock_id)+".csv", index=False, encoding='utf-8-s')
                        
                        

