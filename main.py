import requests
from tkinter import *
import re
import codecs
import mysql
from bs4 import BeautifulSoup
import jobinf
import time
from matplotlib import pyplot as plt
from matplotlib import font_manager as fm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import numpy as np
import cmath

'''
用来爬取拉勾网网页源代码
返回网页源代码
'''


def lagou(url):
    time.sleep(3)
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Connection': 'keep-alive',
               'Content-Length': '0',
               'Cookie': 'user_trace_token=20180510173728-c10e8885-5435-11e8-81e3-5254005c3644; LGUID=20180510173728-c10e8dc2-5435-11e8-81e3-5254005c3644; RECOMMEND_TIP=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22164c5783eda87c-0e212618735884-2b6f686a-2073600-164c5783edba7b%22%2C%22%24device_id%22%3A%22164c5783eda87c-0e212618735884-2b6f686a-2073600-164c5783edba7b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; LG_LOGIN_USER_ID=ec7fa65f96faa142155083240141dc9fa4bffacc5d93f845; WEBTJ-ID=20180807202654-165145abbbd1-07565951bc1e25-2b6f686a-2073600-165145abbbe813; _putrc=D77B83FA8386AF06; JSESSIONID=ABAAABAAAGFABEF2459CB313D5B578466552447E8949A42; login=true; unick=%E8%92%99; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=e88ad3d2bcfd6a45a13f96c27ef16f5d554fd33351d5dd49; TG-TRACK-CODE=search_code; _gat=1; LGSID=20180807211731-3d9cb491-9a44-11e8-b790-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; LGRID=20180807211731-3d9cb73f-9a44-11e8-b790-525400f775ce; SEARCH_ID=74cd6ad4b3f049608ab302ca7353d451; index_location_city=%E5%85%A8%E5%9B%BD; _ga=GA1.2.1352197252.1525945051; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533539615,1533568515,1533602926,1533644815; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533647874',
               'Host': 'www.lagou.com',
               'Origin': 'https://www.lagou.com',
               'Referer': '%s' % (url),
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER',
               'X-Anit-Forge-Code': '0',
               'X-Anit-Forge-Token': 'None',
               'X-Requested-With': 'XMLHttpRequest',
               'first': 'true',
               'pn': '1',
               'kd': '%E5%A4%A7%E6%95%B0%E6%8D%AE?'
               }
    # s = requests.session()
    response = requests.post(url, headers=headers)
    response.encoding = 'utf-8'
    wenben = response.text
    wenben.encode("utf-8")
    # print(wenben)
    return wenben
    # f = codecs.open('D:/test/lagou.html', 'w', encoding="utf-8")
    # f.write(wenben)


def liezhi(url):
    time.sleep(2)
    response = requests.get(url)
    response.encoding = "utf-8"
    wenben = response.text
    wenben.encode("utf-8")
    return wenben


def readwenben(fp):
    f = codecs.open(fp, "r", encoding="utf-8")
    string = f.read()
    return string


'''
用来解析爬取到的拉钩网网页
html是网页源代码
返回Job列表
'''


def htmlparser(html):
    ####html暂时设置为这个
    # html = readwenben("D:/test/lagou.html")
    soup = BeautifulSoup(html, "html.parser")
    rs = soup.select("#content-container > #main_container > .content_left > .s_position_list > ul > li")
    if bool(rs) == False:
        return
    job = jobinf.Job("", "", "", "", "", "", "")
    jobinf_list = []  # 用来保存分析出的职位信息
    experience_pattern = re.compile(r".*/")
    diploma_pattern = re.compile(r"/.*")
    for i in range(0, len(rs)):
        inf = rs[i].select('span')
        experience_diploma = rs[i].select(".li_b_l")
        e_diploma = experience_diploma[0].contents[4]
        experience = re.findall(experience_pattern, e_diploma)[0]
        experience = experience.replace(" /", "")
        diploma = re.findall(diploma_pattern, e_diploma)[0]
        diploma = diploma.replace("/ ", "")
        job.set_job_name(rs[i].attrs['data-positionname'])
        job.set_company_name(rs[i].attrs['data-company'])
        job.set_position(inf[0].select("em")[0].string)
        job.set_create_time(inf[1].string)
        job.set_salary_fr(inf[2].string)
        job.set_diploma(diploma)
        job.set_experience(experience)
        jobinf_list.append(
            jobinf.Job(rs[i].attrs['data-positionname'], rs[i].attrs['data-company'], inf[1].string, inf[2].string,
                       experience, diploma, inf[0].select("em")[0].string))
        jobinf_list[len(jobinf_list) - 1].process()
    return jobinf_list


def liezhi_htmlparser(html):
    soup = BeautifulSoup(html, "html.parser")
    rs = soup.select(".container > .wrap > .job-content > .sojob-result > .sojob-list > li")
    job_list = []
    for jobinfo in rs:
        job_tag = jobinfo.select(".sojob-item-main > .job-info")
        job_name = job_tag[0].select("h3 > a")[0].string.replace("\n", "").replace("\t", "").replace(" ", "").replace(
            "\r", "")
        company_name = jobinfo.select(".company-info > p > a")[0].string
        salary_fr = job_tag[0].select(".condition > .text-warning")[0].string
        a_tag = job_tag[0].select(".condition > a")
        span_tag = job_tag[0].select(".condition > span")
        time = job_tag[0].select(".time-info > time")[0].attrs["title"]
        time = time.replace("年", "-").replace("月", "-").replace("日", "")
        if bool(a_tag):  # 有a标签
            city_area = a_tag[0].string
            diploma = span_tag[1].string
            experience = span_tag[2].string
        else:
            city_area = job_tag[0].select(".condition > span")[1].string
            diploma = span_tag[2].string
            experience = span_tag[3].string
        job_list.append(jobinf.Job(job_name, company_name, time, salary_fr, experience, diploma, city_area))
        job_list[len(job_list) - 1].process()
    return job_list


'''
返回公司信息
'''


def gongsiparser(html):
    soup = BeautifulSoup(html, "html.parser")
    rs_name = soup.select(".top_info > .top_info_wrap > .company_info > .company_main > h1 > a")
    if bool(rs_name) == False:
        return
    name = rs_name[0].string.replace(" ", "").replace("\n", "")
    rs = soup.select("#main_container > #container_right > #basic_container > .item_content > ul > li")
    if bool(rs) == False:
        return
    return jobinf.Company(name, rs[0].select("span")[0].string, rs[1].select("span")[0].string,
                          rs[2].select("span")[0].string, rs[3].select("span")[0].string)


id = 50000


def exe(html):  # 测试一下整个工程
    global id
    joblist = htmlparser(html)
    db = mysql.Mysql()
    for job in joblist:
        print(job.get_job_name(), job.get_company_name(), job.get_create_time(), job.get_salary_fr(),
              job.get_low_salary(), job.get_high_salary(),
              job.get_experience(), job.get_diploma(), job.get_position(), job.get_city())
        sql = "insert into Position values(%d,\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%d,%d,\"%s\",\"%s\",\"%s\",\"%s\")" % (
            id, "大数据", job.get_job_name(), job.get_company_name(), job.get_create_time(), job.get_salary_fr(),
            job.get_low_salary(), job.get_high_salary(),
            job.get_experience(), job.get_diploma(), job.get_position(), job.get_city())
        db.excutesql(sql)
        id = id + 1


def insertdb(link, tag):
    db = mysql.Mysql()
    global id
    for i in range(1, 31):
        url = link + str(i) + "/?filterOption=3"
        html = lagou(url)
        joblist = htmlparser(html)
        if bool(joblist) == False:
            break
        for job in joblist:
            print(job.get_job_name(), job.get_company_name(), job.get_create_time(), job.get_salary_fr(),
                  job.get_experience(), job.get_diploma(), job.get_position())
            sql = "insert into Position values(%d,\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%d,%d,\"%s\",\"%s\",\"%s\",\"%s\")" % (
                id, tag, job.get_job_name(), job.get_company_name(), job.get_create_time(), job.get_salary_fr(),
                job.get_low_salary(), job.get_high_salary(),
                job.get_experience(), job.get_diploma(), job.get_position(), job.get_city())
            db.excutesql(sql)
            id = id + 1
    print(tag + "标签执行完毕!")


def insert_job(job_list, tag):
    db = mysql.Mysql()
    global id
    if bool(job_list) == False:
        return
    for job in job_list:
        print(job.get_job_name(), job.get_company_name(), job.get_create_time(), job.get_salary_fr(),
              job.get_experience(), job.get_diploma(), job.get_position())
        sql = "insert into Position values(%d,\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%d,%d,\"%s\",\"%s\",\"%s\",\"%s\")" % (
            id, tag, job.get_job_name(), job.get_company_name(), job.get_create_time(), job.get_salary_fr(),
            job.get_low_salary(), job.get_high_salary(),
            job.get_experience(), job.get_diploma(), job.get_position(), job.get_city())
        db.excutesql(sql)
        id = id + 1


def extractlink():
    text = lagou("http://www.lagou.com")
    soup = BeautifulSoup(text, "html.parser")
    menu_boxs = soup.select(".container > .container-body > .clearfix > #sidebar > .mainNavs > .menu_box")
    job_link_list = menu_boxs[0]
    job_links = job_link_list.select("a")
    print(len(job_links))
    tag = open("D:/test/tag.txt", "w")
    link = open("D:/test/link.txt", "w")
    for job_link in job_links:
        tag.write(job_link.string + "\n")
        link.write(job_link.attrs["href"] + "\n")


# 对每个标签进行爬虫
def start():
    tag_file = open("D:/test/tag.txt")
    tag_list = tag_file.readlines()
    link_file = open("D:/test/link.txt")
    link_list = link_file.readlines()
    for i in range(0, len(tag_list)):
        tag = tag_list[i].replace("\n", "")
        link = link_list[i].replace("\n", "")
        print("正在执行" + tag + "标签")
        insertdb(link, tag)
        time.sleep(60)


def company_crawler():
    db = mysql.Mysql()
    for i in range(13076, 40000):
        company = gongsiparser(lagou("https://www.lagou.com/gongsi/%d.html" % i))
        if bool(company):
            db.excutesql("insert into Company values(%d,\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" % (
                i, company.name, company.type, company.process, company.number, company.address))
        else:
            print(i, "空")


def analyse():
    zhfont1 = fm.FontProperties(fname="C:/Windows/Fonts/simsun.ttc")
    db = mysql.Mysql()
    db.excutesql("select 职位标签,avg(最低薪资) from Position group by 职位标签 order by avg(最低薪资) desc")
    rs = db.getdata()
    taglist = []
    avglist = []
    for i in range(0, 10):
        taglist.append(rs[i][0])
        avglist.append(rs[i][1])
    plt.bar(taglist, avglist)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # x=np.linspace(1,7,100)
    # y=np.sin(x)
    # plt.plot(x,y)
    plt.xlabel("职位标签")
    plt.ylabel("月薪，单位k")
    plt.title("互联网职位薪资排行前十职位")
    plt.legend()
    plt.show()


def pc():
    bigdata_url = "https://www.lagou.com/jobs/list_%E5%A4%A7%E6%95%B0%E6%8D%AE?labelWords=&fromSearch=true&suginput="
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gup")
    browser = webdriver.Chrome(chrome_options=chrome_options)
    try:
        while True:
            try:
                browser.get(bigdata_url)
                time.sleep(1)
                html = browser.page_source
                exe(html)
                nextpage = browser.find_element_by_class_name("pager_next")
                time.sleep(1)
                nextpage.click()
            except Exception as e:
                print(str(e))
            finally:
                time.sleep(1)
    finally:
        time.sleep(10)
        browser.close()

def tag_percent(job_list,tag):
    i=0
    for job in job_list:
        if bool(re.findall(re.compile(r".*%s.*" % tag,re.IGNORECASE), job.get_job_name())):
            i+=1
        else:
            pass
    return i/len(job_list)

def html(url):
    response = requests.get(url)
    response.encoding="utf-8"
    return response.text

def parser(html):
    bs=BeautifulSoup(html,"html.parser")
    left_list=bs.find_all("div",class_="left")
    level_list=[]
    h3=[]
    for x in left_list:
        level=re.findall(re.compile(r"Biosafety Level.*?</em>",re.DOTALL),str(x))
        h3_list=x.find_all("h3")
        if bool(level):
            h3.append(h3_list[0])
            level=level[0]
            level=re.findall(re.compile(r"\d"),level)
            level_list.append(level)
        else:
            print(x.string)
    rs=bs.find_all("h3")

    return (h3,level_list)
if __name__ == '__main__':
    url="https://www.atcc.org/Search_Results.aspx?dsNav=Rpp:100,Ro:100,N:1000552-1000574&adv=1&redir=1"
    [rs,level]=parser(html(url))
    name_list=[]
    for x in rs:
        string=re.findall(re.compile(r"<em>|<i>.*</sup>"),str(x))
        if bool(string):
            string=string[0].replace("/n","").replace("<em>","").replace("</em>","").replace("<sup>","").replace("</sup>","").replace("<i>","").replace("</i>","")
            print(string)

    print(len(rs),len(level))

    # f = open("D:/test/tag.txt", "r")
    # tag_list = f.readlines()
    # for i in range(0, len(tag_list)):
    #     tag_list[i] = tag_list[i].replace("\n", "")
    # key = ""
    # for tag in tag_list:
    #     key = tag
    #     for curpage in range(0, 100):
    #         liezhi_url = "https://www.liepin.com/zhaopin/?ckid=bb7f9bb3192d7370&fromSearchBtn=2&init=-1&dqs=000&degradeFlag=0&key=%s&imscid=R000000035&headckid=bb7f9bb3192d7370&d_pageSize=40&siTag=I-7rQ0e90mv8a37po7dV3Q~NOaAwuxhyWp3swgLalmlSA&d_headId=498c9de3f7f1e2056d52f1ac18ba1b2b&d_ckId=498c9de3f7f1e2056d52f1ac18ba1b2b&d_sfrom=search_prime&d_curPage=99&curPage=%d" % (
    #         key, curpage)
    #         job_list = liezhi_htmlparser(liezhi(liezhi_url))
    #         print(liezhi(liezhi_url))
    #         if tag_percent(job_list,key)<0.8:
    #             break
    #         #insert_job(job_list,key)
