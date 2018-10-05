import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
from io import BytesIO

def stock_master():
    url = "http://kind.krx.co.kr/corpgeneral/corpList.do"
    data = {
        'method':'download',
        'orderMode':'3',
        'orderStat':'D',
        'searchType':'13',
        'fiscalYearEnd':'all',
        'location':'all',
    }

    r=requests.post(url, data=data)
    f=BytesIO(r.content)
    dfs=pd.read_html(f,header=0, parse_dates=['상장일'])
    df = dfs[0].copy()

    df['종목코드']=df['종목코드'].astype(np.str)
    df['종목코드']=df['종목코드'].str.zfill(6)

    return df

df_master = stock_master()
df =df_master.loc[:,['회사명','종목코드','업종','상장일','결산월']]
print(df.head())
