import re

#计算运行时间
import time

import requests
import pymongo

#连接MongoDB数据库
mymongo = pymongo.MongoClient('localhost',27017)
mydata = mymongo['chasenes']
mytab = mydata['_scenic']
mykey = mydata['sets']

from lxml import etree
from lxml.doctestcompare import strip
from urllib import response
# /*/*/*/*/*/*/*/*/*/*/*/*/*/*
# IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/
# 仅仅爬取首页IP地址就足够一般使用
from bs4 import BeautifulSoup
import requests
import random
def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list
def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
        proxy_ip = random.choice(proxy_list)
        proxies = {'http': proxy_ip}
        return proxies
if __name__ == '__main__':
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
    ip_list = get_ip_list(url, headers=headers)
    proxies = get_random_ip(ip_list)
    # print(proxies)
    #函数get_ip_list(url, headers)传入url和headers，最后返回一个IP列表，列表的元素类似42.84.226.65:8888格式，这个列表包括国内髙匿代理IP网站首页所有IP地址和端口。
# /*/*/*/*/*/*/*/*/*/*/*/*/*/*


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}
cookie = {'NewProvinceId': '3', ' NCid': '53', ' NewProvinceName': '%E5%8C%97%E4%BA%AC', ' NCName': '%E5%8C%97%E4%BA%AC', ' Hm_lvt_64941895c0a12a3bdeb5b07863a52466': '1546604656', ' Hm_lpvt_64941895c0a12a3bdeb5b07863a52466': '1546604656', ' 17uCNRefId': 'RefId=4140683&SEFrom=baidu&SEKeyWords=%E5%90%8C%E7%A8%8B', ' TicketSEInfo': 'RefId=4140683&SEFrom=baidu&SEKeyWords=%E5%90%8C%E7%A8%8B', ' CNSEInfo': 'RefId=4140683&tcbdkeyid=&SEFrom=baidu&SEKeyWords=%E5%90%8C%E7%A8%8B&RefUrl=https%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3DUTF-8%26wd%3D%25E5%2590%258C%25E7%25A8%258B', ' qdid': '39264|1|6928722|0a6c16', ' route': '583cc1e511349ae6f51225724a31e80a', ' __tctma': '144323752.1546604656293708.1546604656125.1546604656125.1546604656125.1', ' __tctmu': '144323752.0.0', ' __tctmz': '144323752.1546604656125.1.1.utmccn=(organic)|utmcmd=organic|utmEsl=utf-8|utmcsr=baidu|utmctr=%e5%90%8c%e7%a8%8b', ' longKey': '1546604656293708', ' __tctrack': '0', ' ASP.NET_SessionId': 'vmxohlmsixubhjyycdyvnwqb', ' wwwscenery': '98273b7e8b4c33977ca7c786db77b994', ' Hm_lvt_c6a93e2a75a5b1ef9fb5d4553a2226e5': '1546604667', ' Hm_lpvt_c6a93e2a75a5b1ef9fb5d4553a2226e5': '1546604667', ' __tctmc': '144323752.72999573', ' __tctmd': '144323752.737325', ' __tctmb': '144323752.2543334769460941.1546604656125.1546604667755.2'}


num_str = 0#统计数据条数
page = 1
while page:
    url = 'https://www.ly.com/scenery/NewSearchList.aspx?&page='+str(page)
    #https://www.ly.com/scenery/AjaxHelper/SceneryPriceFrame.aspx?action=GETNEWFRAMEFORLIST&ids=181784&iid=0.8105935568666023
    #https://www.ly.com/scenery/AjaxHelper/SceneryPriceFrame.aspx?action=GETNEWFRAMEFORLIST&ids=18681&iid=0.8633963606545751
    #https://www.ly.com/scenery/AjaxHelper/SceneryPriceFrame.aspx?action=GETNEWFRAMEFORLIST&ids=23479&iid=0.17546899964017793
    response = requests.post(url=url,headers=headers,cookies=cookie,proxies=proxies)
    html = etree.HTML(response.text)
    all_href = html.xpath("//div[@class='scenery_list']/div[@class='list_l']//a[@class='img_c goFinal']//@href")

    for i in all_href:
        kai = time.clock()
        start = time.clock()

        dict_2 = {}
        href = "https://www.ly.com/"+i
        respon = requests.get(url=href,headers=headers,cookies=cookie)
        hmtl_1 = etree.HTML(respon.text)
        name = strip(hmtl_1.xpath("//h3[@class='s_name']/text()")[0])#景点[0]
        # print('/*/*/*/*/*----',name)
        if [i['scenic'] for i in mytab.find({'scenic': name})]:
            num_str+=1
            guan = time.clock()
            print([i['scenic'] for i in mytab.find({'scenic': name})][0],'---===---',name,'------------该景点信息已存在%s'%(guan-kai))
            continue
        else:
            dict_2['scenic'] = name
            star_level = hmtl_1.xpath('//*[@id="content"]/div[3]/div[2]/h3/span/text()')
            if len(star_level) != 0:
                dict_2['star_level'] = strip(star_level[0])#星级
            dict_2['address'] = strip(hmtl_1.xpath("//p[@class='s_com']/span/text()")[0])
            dict_2['intro'] = strip(hmtl_1.xpath("//div[@class='s_des clearfix']/p[@class='des']/text()")[0])#简介
            a = hmtl_1.xpath("//div[@class='s_price']/div[@class='s_p_t']//text()")
            dict_2['price'] = "".join(a)
            open_time = re.findall(r'<pre>(.*?)</pre>',respon.text,re.S)[0]
            dict_2['open_time'] = open_time
            img = re.findall(r'<img bigsrc="(.*?)" nsrc=',respon.text,re.S)#相关图片
            list_img = []#相关图片
            for i in img:
                list_img.append('http:'+i)
            dict_2['correlation_img'] = list_img
            gonggao = re.findall(r'<li><span>(.*?)</span></li>',respon.text,re.S)
            # dict_2['notice'] = '暂无公告'  # 公告
            if len(gonggao) !=0:
                dict_2['notice'] = gonggao[0]#公告

            # /*/*/*mongoDB插入数据
            mytab.insert(dict_2)
            num_str += 1

            print(dict_2)
            end = time.clock()
            print(name,'的景点的相关信息已经保存.____数据库存量:*_',num_str,'_*time: %s Seconds'%(end-start))
            page += 1

