# 融资融券交易总量
# http://stock.jrj.com.cn/rzrq/jyzs.shtml

import os
import json
import math

psize = 50

def getDataRzrq (page):
  tmpl = open('tmpl.js').read()
  
  cmd = "curl 'http://stock.jrj.com.cn/action/rzrq/getMarketDetailSecondPage.jspa?vname=market&sec_trade=1,2&havingType=2&page=%s&psize=50&order=desc&sort=transactionDate&_dc=1611838870358' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Connection: keep-alive' -H 'Referer: http://stock.jrj.com.cn/rzrq/jyzs.shtml' -H 'Cookie: WT_FPC=id=2eb95600ff95653c4e91611837868793:lv=1611838864944:ss=1611837868793; channelCode=3763BEXX; ylbcode=24S2AZ96; jrj_uid=1611837868814cRJbU1qccP'" % page
  market = os.popen(cmd).readlines()
  
  fo = open("tmp.js", "w")
  fo.write(tmpl.format("".join(market)))
  fo.close()
  os.system("node tmp.js")

  return json.load(open("tmp.json"))

latest = getDataRzrq(1)

n = latest["summary"]["total"] - len(latest["data"])

old = None

if os.path.exists("data.json"):
  old = json.load(open("data.json"))
  n = n - old["summary"]["total"]

if (n > 0):
  for i in range(2, int(math.ceil(n/psize)) + 2):
    tmp = getDataRzrq(i)
    latest["data"].extend(tmp["data"])

if old:
  start = len(latest["data"]) + len(old["data"]) - latest["summary"]["total"]
  latest["data"].extend(old["data"][start:])

print("total:", latest["summary"]["total"])
print("data:", len(latest["data"]))

json.dump(latest, open("data.json", "w"), indent=2, ensure_ascii=False )