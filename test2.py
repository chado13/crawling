import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlopen
import lxml.html
import re
from html_table_parser import parser_functions as parser

auth_key = "3dbd76db63ebf30768656d187e57e6f57c0b6203"
code = "024110"
start_date = '1990101'

url = "http://dart.fss.or.kr/api/search.xml?auth="+auth_key+"&crp_cd="+code+"&start_dt="+start_date+"&bsn_tp=A001&bsn_tp=A002&bsn_tp=A003"

resultxml=requests.get(url)
# resultxml = urlopen(url)
# result = resultxml.read()
result = resultxml.text
xmlsoup=bs(result,"html.parser")

data = pd.DataFrame()
te = xmlsoup.findAll("list")

for t in te:
    temp=pd.DataFrame(([[t.crp_cls.string, t.crp_nm.string,t.crp_cd.string,
        t.rpt_nm.string,t.rcp_no.string,t.flr_nm.string, t.rcp_dt.string,
        t.rmk.string]]),
        columns=["crp_cls","crp_nm","crp_cd","rpt_nm","rcp_no","flr_nm",
        "rcp_dt","rmk"])
    data = pd.concat([data,temp])

data = data.reset_index(drop=True)
user_num=int(input("몇 번째 보고서를 확인하시겠습니까?"))

url = "http://dart.fss.or.kr/dsaf001/main.do?rcpNo="+data["rcp_no"][user_num]

req=requests.get(url).text

tree=lxml.html.fromstring(req)

onclick=tree.xpath('//*[@id="north"]/div[2]/ul/li[1]/a')[0].attrib['onclick']
pattern=re.compile("^openPdfDownload\('\d+',\s*'(\d+)'\)")
dcm_no=pattern.search(onclick).group(1)
url_parsing="http://dart.fss.or.kr/report/viewer.do?rcpNo="+data['rcp_no'][user_num]+"&dcmNo="+dcm_no+"&eleId=15&offset=1489233&length=105206&dtd=dart3.xsd"


report=urlopen(url_parsing)
r=report.read()


xmlsoup_another=bs(r,'html.parser')
body = xmlsoup_another.find("body")
table=body.find_all("table")
p=parser.make2d(table[3])

