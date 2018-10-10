import pandas as pd
import numpy as np
import requests
from io import BytesIO
from datetime import datetime
import sqlite3

def stock_master_price(date=None):
    if date == None:
        date = datetime.today().strftime('%Y%m%d')

    gen_otp_url='http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
    gen_otp_data={
        'name':'fileDown',
        'filetype':'xls',
        'url':'MKD/04/0404/04040200/mkd04040200_01',
        'market_gubun': 'ALL',
        'indx_ind_cd':'' ,
        'sect_tp_cd': 'ALL',
        'schdate': date,
        'pagePath': '/contents/MKD/04/0404/04040200/MKD04040200.jsp',

    }

    r=requests.post(gen_otp_url,gen_otp_data)
    code=r.content

    down_url = 'http://file.krx.co.kr/download.jspx'
    down_data = {
        'code':code,
    }

    r=requests.post(down_url,down_data)
    df = pd.read_excel(BytesIO(r.content), header=0,thousands=',')
    return df



# date = datetime(2018,9,5).strftime('%Y%m%d')
# df = stock_master_price(date)


def get_krx_stock_master():
    gen_otp_url ='http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
    gen_otp_data = {
        'name':'fileDown',
        'filetype':'xls',
        'url':'MKD/04/0406/04060100/mkd04060100_01',
        'market_gubun': 'ALL',
        'isu_cdnm': '전체',
        'sort_type': 'A',
        'std_ind_cd': '',
        'cpt': '1',
        'in_cpt':'', 
        'in_cpt2': '',
        'pagePath': '/contents/MKD/04/0406/04060100/MKD04060100.jsp',
    }

    r= requests.post(gen_otp_url,gen_otp_data)
    code = r.content

    down_url = 'http://file.krx.co.kr/download.jspx'
    down_data={
        'code':code,
    }
    r=requests.post(down_url,down_data)
    f=BytesIO(r.content)

    usecols=['종목코드','기업명','업종코드','업종']
    df=pd.read_excel(f,converters={'종목코드':str,'업종코드':str},usecols=usecols)
    df.columns=['code','name','sector_code','sector']
    return df

df_master = get_krx_stock_master()
print(df_master.head())

con = sqlite3.connect("krx_stock_code.db")
cur = con.cursor()
# table = """ CREATE TABLE krx_stocks_master (code text, name text, sector_code text, sector text)"""
# cur.execute(table)

inser_update_sql="""INSERT INTO stock_code VALUES(?,?,?,?)"""

for idx, r in df_master.iterrows():

    cur.execute(inser_update_sql,r)

con.commit()
con.close()