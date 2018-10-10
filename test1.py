import pandas as pd
import numpy as np
import requests
from io import BytesIO
from datetime import datetime, timedelta

def get_daily_price(code,fromdate=None,todate=None):
    if todate==None:
        todate = datetime.today().strftime('%Y%m%d')

    if fromdate==None:
        fromdate = (datetime.today() - timedelta(days=30)).strftime('%Y%m%d')
    
    gen_otp_url="http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx"
    gen_otp_data={
        'name':'fileDown',
        'filetype':'csv',
        'url':'MKD/04/0402/04020100/mkd04020100t3_02',
        'isu_cd':code,
        'fromdate':fromdate,
        'todate':todate,
    }

    r=requests.post(gen_otp_url,gen_otp_data)
    code = r.content

    down_url = "http://file.krx.co.kr/download.jspx"
    down_data={
        'code':code,
    }

    r=requests.post(down_url,down_data)
    r.encoding = "utf-8-sig"
    
    df=pd.read_csv(BytesIO(r.content),header=0, thousands=',')
    return df


# df = get_daily_price('KR7005930003')
# # df = df.loc[:,['년/월/일','시가','고가','저가','종가','거래량(주)']]
# # df.columns = ['date','open','high','low','close','volume']
# # df.set_index('date',inplace=True)
# print(df)


a=0

while a == 20:
    a = a+1
    b=a+a        
    print(a,b)