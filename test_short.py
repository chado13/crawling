import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from io import BytesIO
import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def get_kospi_short(start_date=None, end_date=None):
    if end_date ==None:
        end_date = datetime.today().strftime('%Y%m%d')
    if start_date==None and end_date==None:
        start_date = (datetime.today()- relativedelta(years=1)).strftime('%Y%m%d')
    elif start_date ==None and end_date!=None:
        end_date=end_date
        start_date = (datetime.strptime(end_date, '%Y%m%d')-relativedelta(years=1)).strftime('%Y%m%d')
    
    gen_otp_url="http://short.krx.co.kr/contents/COM/GenerateOTP.jspx"
    gen_otp_data={
        'name':'fileDown',
        'filetype':'xls',
        'url':'SRT/02/02020100/srt02020100',
        'mkt_tp_cd':'1',
        'isu_cdnm':'전체',
        'isu_cd': '',
        'isu_nm': '',
        'isu_srt_cd':'', 
        'strt_dd':start_date,
        'end_dd':end_date,
        'pagePath':'/contents/SRT/02/02020100/SRT02020100.jsp',
    }
 
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

df = get_kospi_short('19951201')
print(df.head())