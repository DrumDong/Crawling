# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 10:16:35 2020

@author: USER
"""

'''
네이버 블로그 크롤링
'''
import platform        
import sys
import os
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import tqdm
#from tqdm.notebook import tqdm

def make_crawling(query_txt,start_date,end_date,yearmonth,type_):
    '''검색어 변수 세팅'''
    #query_txt = input('1.크롤링할 키워드 입력')
    #start_date = input('조회를 시작할 날짜 입력(예:2017-01-01)')
    #end_date = input('조회를 종료할 날짜 입력(예:2017-12-31)')

    '''크롬 웹드라이버 시행'''
    # Step 1. 크롬 웹브라우저 실행
    path = 'C:/Users/USER/Dropbox (kk-bigdata)/0.Workspace/DG/김동규_Spyder/chromedriver.exe'
    driver = webdriver.Chrome(path)
    #사이트 주소는 네이버
    driver.get('http://www.naver.com')

    time.sleep(2)

    #Step2. 네이버 검색창에 '검색어' 검색
    element = driver.find_element_by_id('query')
    element.send_keys(query_txt) # query_txt는 위에서 입력한 내용
    element.submit()

    #Step 3. '블로그' 카테고리 선택
    try:
        driver.find_element_by_link_text('블로그').click() # .click() 괄호 안으 눌러라는 뜻
    except:
        driver.find_element_by_link_text('더보기').click()
        driver.find_element_by_link_text('블로그').click()
    '''검색옵션-관련도순 정렬'''
    #Step 4. 오른쪽의 검색 옵션 버튼 클릭
    driver.find_element_by_id('_search_option_btn').click()

    #Step 5. 정렬: 관련도순
    driver.find_element_by_xpath('''//*[@id='snb']/div/ul/li[1]/a''').click() # 정렬 버튼의 xpath 클릭
    element_ok=driver.find_element_by_xpath('''//*[@id='snb']/div/ul/li[1]/div/ul/li[1]/a''')
    element_ok.click() #관련도순 xpath


    '''검색옵션 - 검색기간 입력'''
    #Step 6. 날짜 입력
    driver.find_element_by_xpath('''//*[@id='snb']/div/ul/li[2]/a''').click()
    time.sleep(2)

    # 시작 날짜 입력하기
    s_date = driver.find_element_by_xpath("""//*[@id="blog_input_period_begin"]""")     
    driver.find_element_by_xpath("""//*[@id="blog_input_period_begin"]""")
    s_date.clear()  # 날짜 입력 부분에 기존에 입력되어 있던 날짜를 제거합니다. 
    time.sleep(1)
    # 아래 코드가 날짜를 for 반복문으로 1 글자씩 입력하는 부분입니다.
    for c in start_date:
        s_date.send_keys(c) 
        time.sleep(0.1)
    
    # 종료 날짜 입력하기
    e_date = driver.find_element_by_xpath("""//*[@id="blog_input_period_end"]""")
    driver.find_element_by_xpath("""//*[@id="blog_input_period_end"]""").click()    
    e_date.clear()
    time.sleep(1)

    for c in end_date:
        e_date.send_keys(c)
        time.sleep(0.1)
    
    # Step7. 날짜 입력 "적용하기" 버튼을 클릭 합니다.  
    driver.find_element_by_class_name("tx").click()
    time.sleep(3)
    
    url_list = []
    title_list = []

    # ★몇개의 페이지를 크롤링할지 선택
    total_page = 100
    for i in tqdm.tqdm(range(0, total_page)):  # 페이지 번호
        i = i*10 + 1
        print(start_date,end_date,start_date,end_date,query_txt, i)
        url = "https://search.naver.com/search.naver?date_from={0}&date_option=8&date_to={1}&dup_remove=1&nso=p%3Afrom{2}to{3}post_blogurl=&post_blogurl_without=&query={4}&sm=tab_pge&srchby=all&st=sim&where=post&start={5}".format(str(start_date),str(end_date),str(start_date),str(end_date),str(query_txt),str(i))
        driver.get(url)
        time.sleep(0.5)
    
        # URL 크롤링 시작
        titles = "a.sh_blog_title._sp_each_url._sp_each_title"
        article_raw = driver.find_elements_by_css_selector(titles)
        #     article_raw

        # url 크롤링 시작    
        for article in article_raw:
            url = article.get_attribute('href')   
            url_list.append(url)
    
        # 제목 크롤링 시작    
        for article in article_raw:
            title = article.get_attribute('title')   
            title_list.append(title)
    
            #print(title)
    
    print('url갯수: ', len(url_list))
    print('url갯수: ', len(title_list))

    df = pd.DataFrame({'url':url_list, 'title':title_list})
    # 저장하기
    df.to_excel("C:/Users/USER/Dropbox (kk-bigdata)/0.Workspace/DG/김동규_Spyder/blog_url_%s_%s_%s.xlsx"%(query_txt,yearmonth,type_))
    
###############################################################################################
###############################################################################################

def make_crawling_f(query_txt,yearmonth,type_):
    import sys
    import os
    import pandas as pd
    import numpy as np
    
    # "url_list.csv" 불러오기
    url_load = pd.read_excel("C:/Users/USER/Dropbox (kk-bigdata)/0.Workspace/DG/김동규_Spyder/blog_url_%s_%s_%s.xlsx"%(query_txt,yearmonth,type_))        # 기본 모델

    num_list = len(url_load)

    print(num_list)
    url_load




    dict = {}  # 전체 크롤링 데이터를 담을 그릇

    # ★수집할 글 갯수
    number = num_list
    for i in tqdm.tqdm(range(0, number)): 
        # 글 띄우기
        url = url_load['url'][i]
        driver = webdriver.Chrome('C:/Users/USER/Dropbox (kk-bigdata)/0.Workspace/DG/김동규_Spyder/chromedriver.exe')
        driver.get(url)   # 글 띄우기
    
        # 크롤링
    
        try : 
            # iframe 접근
            driver.switch_to_frame('mainFrame')

            target_info = {}

            # 제목 크롤링 시작
            overlays = ".se-fs-.se-ff-"                                 
            tit = driver.find_element_by_css_selector(overlays)         # title
            title = tit.text
            title
            
            # 글쓴이 크롤링 시작
            overlays = ".nick"                                 
            nick = driver.find_element_by_css_selector(overlays)         # nick
            nickname = nick.text

            # 날짜 크롤링
            overlays = ".se_publishDate.pcol2"                                 
            date = driver.find_element_by_css_selector(overlays)         # date
            datetime = date.text

            # 내용 크롤링
            overlays = ".se-component.se-text.se-l-default"                                 
            contents = driver.find_elements_by_css_selector(overlays)         # date

            content_list = []
            for content in contents:
                content_list.append(content.text)

            content_str = ' '.join(content_list)

            # 글 하나는 target_info라는 딕셔너리에 담기게 되고,
            target_info['title'] = title
            target_info['nickname'] = nickname
            target_info['datetime'] = datetime
            target_info['content'] = content_str

            # 각각의 글은 dict라는 딕셔너리에 담기게 됩니다.
            dict[i] = target_info
            time.sleep(1)
        
            print(i, title)

            # 글 하나 크롤링 후 크롬 창 닫기
            driver.close()       
    
        # 에러나면 현재 크롬창 닫고 다음 글(i+1)로 이동
        except:
            driver.close()
            time.sleep(1)
            continue
    
        # 중간,중간에 파일로 저장하기
        #if i == 30 or 50 or 80:
        #    # 판다스로 만들기
        #    import pandas as pd
        #    result_df = pd.DataFrame.from_dict(dict, 'index')

        #    # 저장하기
        #    result_df.to_excel("C:/Users/USER/Dropbox (kk-bigdata)/0.Workspace/DG/김동규_Spyder/blog_content_%s_%s.xlsx"%(query_txt,yearmonth))
        #    time.sleep(3)
    
    print('수집한 글 갯수: ', len(dict))
    print(dict)    
    
    # 판다스로 만들기
    import pandas as pd
    result_df = pd.DataFrame.from_dict(dict, 'index')

    # 저장하기
    result_df.to_excel("C:/Users/USER/Dropbox (kk-bigdata)/0.Workspace/DG/김동규_Spyder/blog_content_%s_%s_%s.xlsx"%(query_txt,yearmonth,type_))
