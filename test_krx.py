import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from io import BytesIO
import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

#종목별 공매도 현황
def get_krx_short(code,start_date=None, end_date=None):
    if end_date ==None:
        end_date = datetime.today().strftime('%Y%m%d')
    if start_date==None and end_date==None:
        start_date = (datetime.today()- relativedelta(years=1)).strftime('%Y%m%d')
    elif start_date ==None and end_date!=None:
        end_date=end_date
        start_date = (datetime.strptime(end_date, '%Y%m%d')-relativedelta(years=1)).strftime('%Y%m%d')
    gen_otp_url = 'http://short.krx.co.kr/contents/COM/GenerateOTP.jspx'
    gen_otp_data = {
        'name':'fileDown',
        'filetype':'xls',
        'url':'SRT/02/02010100/srt02010100',
        'isu_cd':code,
        'strt_dd':start_date,
        'end_dd':end_date,
        'pagePath':'/contents/SRT/02/02010100/SRT02010100.jsp',
    }

    r=requests.post(gen_otp_url,gen_otp_data)
    code=r.content

    down_url = 'http://file.krx.co.kr/download.jspx'
    down_data={
        'code':code,
    }

    r=requests.post(down_url,down_data)
    r.encoding = "utf-8-sig"
    
    df=pd.read_excel(BytesIO(r.content),header=0, thousands=',')

    return df

def get_markets_short(market,start_date=None, end_date=None):
    market_dict = {'kospi':'1','kospi_prod':'2','kosdaq':'3'}
    market_code = market_dict[market]

    if start_date !=None and end_date == None:
        end_date = (datetime.strptime(start_date, '%Y%m%d')+relativedelta(years=1)).strftime('%Y%m%d')
    if start_date==None and end_date==None:
        end_date =datetime.today().strftime('%Y%m%d')
        start_date =(datetime.strptime(end_date, '%Y%m%d')-relativedelta(years=1)).strftime('%Y%m%d')
    if start_date ==None and end_date!=None:
        start_date = (datetime.strptime(end_date, '%Y%m%d')-relativedelta(years=1)).strftime('%Y%m%d')
    

    gen_otp_url='http://short.krx.co.kr/contents/COM/GenerateOTP.jspx'
    gen_otp_data={
        'name':'fileDown',
        'filetype':'xls',
        'url':'SRT/02/02020100/srt02020100',
        'mkt_tp_cd':market_code,
        'isu_cdnm':'전체',
        'isu_cd': '',
        'isu_nm': '',
        'isu_srt_cd':'', 
        'strt_dd':start_date,
        'end_dd':end_date,
        'pagePath':'/contents/SRT/02/02020100/SRT02020100.jsp',
    }
    print(gen_otp_data)
    r = requests.post(gen_otp_url, gen_otp_data)
    code = r.content

    down_url = 'http://file.krx.co.kr/download.jspx'
    down_data = {
        'code':code,
    }

    r=requests.post(down_url,down_data)
    r.encoding = "utf-8-sig"
    df = pd.read_excel(BytesIO(r.content), header=0, thousands=',')

    return df

# df = get_krx_short('KR7005930003')
# df.columns=['date','code','name','short_volums','short_balance',
#     'short_values','short_balance_amount']
# df.set_index('date',inplace=True)
# print(df.head())
df = get_markets_short('kospi')
df.columns = ['date','code','name','short_volumes','total_volumes',
        'weight(%)', 'short_values','total_values','weight(%)']
df.set_index('date', inplace=True)
print(df.head())
