from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from tkinter import *
from tkinter import ttk
from pymongo import MongoClient
import pandas as pd
import json
import glob
import os
import time
import pymongo
import requests

#Scraping foction of PubMed WebSite
def scrape_PM():
    s = Service("C:\Program Files (x86)\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    searchWord = str(entryword.get())
    driver.get('https://pubmed.ncbi.nlm.nih.gov/?term='+searchWord)
    driver.find_element(By.ID,'save-results-panel-trigger').click()
    time.sleep(1)

    selection=Select(driver.find_element(By.ID,'save-action-selection'))
    selection.select_by_value('all-results')
    time.sleep(1)

    format=Select(driver.find_element(By.ID,'save-action-format'))
    format.select_by_value('csv')
    time.sleep(1)

    driver.find_element(By.CLASS_NAME, 'action-panel-submit').click()
    time.sleep(100)

    driver.close()

#Scraping foction of IEEE WebSite
def scrape_IEEE():
    s = Service("C:\Program Files (x86)\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    searchWord = str(entryword.get())
    url = 'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText='
    driver.get(url+searchWord)
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR,'#xplMainContent > div.ng-Dashboard > div.col-12.action-bar.hide-mobile > ul > li.Menu-item.inline-flexed.export-filter.myproject-export > xpl-export-search-results > button > a').click()
    time.sleep(10)

    driver.find_element(By.CSS_SELECTOR,"#ngb-nav-2-panel > div > div > div > button").click()
    time.sleep(90)

    driver.close()

#Scraping foction of Scopus WebSite
def scrape_Scopus():
    u = 'samia.fahimi@etu.uae.ac.ma'
    p = 'Samia123456789*'
    s = Service("C:\Program Files (x86)\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    searchWord = str(entryword.get())
    url = 'https://www.scopus.com/results/results.uri?sid=bdd266b97c60b8a2c9513c9594efe6d1&src=s&sot=b&sdt=b&origin=searchbasic&rr=&sl=36&s=TITLE-ABS-KEY(' + searchWord + ')&searchterm1=' + searchWord + '&searchTerms=&connectors=&field1=TITLE_ABS_KEY&fields='
    driver.get(url)
    driver.find_element(By.ID, 'bdd-email').send_keys(u)
    time.sleep(1)

    driver.find_element(By.ID, 'bdd-elsPrimaryBtn').click()
    time.sleep(1)

    driver.find_element(By.ID, 'bdd-password').send_keys(p)
    time.sleep(1)

    driver.find_element(By.ID, 'bdd-elsPrimaryBtn').click()
    time.sleep(1)

    driver.find_element(By.ID, 'selectAllCheck').click()
    time.sleep(1)

    driver.find_element(By.ID, 'export_results').click()
    time.sleep(1)

    driver.find_element(By.XPATH,'//label[@for="selectedAbstractInformationItemsAll-Export"]').click()
    time.sleep(1)

    driver.find_element(By.XPATH,'//label[@for="selectedBibliographicalInformationItemsAll-Export"]').click()
    time.sleep(1)

    driver.find_element(By.ID, 'exportTrigger').click()
    time.sleep(1)

    driver.find_element(By.ID, 'exportTypeAndFormat').click()
    time.sleep(1)

    driver.find_element(By.ID, 'chunkExportTrigger').click()
    time.sleep(90)

    driver.close()

#Scraping foction of USPTO WebSite
def scrape_UPSTO():
    articles = []
    s = Service("C:\Program Files (x86)\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    searchWord = str(entryword.get())
    url = 'https://developer.uspto.gov/search/site/' + searchWord + '?type=all'
    driver.get(url)

    while (True):

        markup = requests.get(url).text

        soup = BeautifulSoup(markup, 'html.parser')
        for item in soup.select('.search-result'):
            article = {}
            article['title'] = item.select_one('h3 > a').get_text()
            articles.append(article)

        try:
            driver.get(url)
            next_button = driver.find_element(By.XPATH, '//a[@rel="next"]')
            url = next_button.get_attribute("href")

        except NoSuchElementException:
            break

    return articles

#Scraping foction of WIPO WebSite
def scrape_WIPO() :
    title=[]
    s = Service("C:\Program Files (x86)\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    searchWord = str(entryword.get())
    url = 'https://www.wipo.int/tools/fr/gsearch.html?cx=016458537594905406506%3Ahmturfwvzzq&cof=FORID%3A11&q='+searchWord+'#gsc.tab=0&gsc.q='+searchWord+'&gsc.page='
    driver.get(url)
    n = 1
    currp = 1
    xtra = []
    while(n<11):

        try:
            driver.get(url + str(currp))
            articles = driver.find_element(By.CSS_SELECTOR,'div.gsc-webResult.gsc-result')
            for article in articles:
                title.append(article.find_element_by_css_selector('a.gs-title').text)
                xtra.append(article.find_element_by_css_selector('div.gs-bidi-start-align.gs-snippet').text)
            currp += 1
            n += 1
        except:
            break

    driver.quit()

    return title

#Scraping foction of Esp@ceNet WebSite
def scrape_Net() :
    s = Service("C:\Program Files (x86)\chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    searchWord = str(entryword.get())
    driver.get('https://worldwide.espacenet.com/searchResults?submitted=true&locale=en_EP&DB=EPODOC&ST=singleline&query='+searchWord)

    while True:
        try:
            driver.find_element(By.ID,'loadNext').click()
            time.sleep(10)
        except NoSuchElementException:
            break
    time.sleep(10)

    driver.find_element(By.CLASS_NAME,'exportLink').click()
    time.sleep(60)
    driver.quit()

def action():
   searchWord = str(entryword.get())
   if cb1.get()==1:
        scrape_PM()
        client = MongoClient("mongodb://localhost:27017/")
        db = client["PubMed"]
        col = db[searchWord]
        # verify the existence of the collection in the DataBase
        if searchWord in db.list_collection_names():
            col.drop()

        searchWord = searchWord.replace(" ", "")

        while (len(searchWord) > 10):
            searchWord = searchWord.rstrip(searchWord[-1])
        df = pd.read_csv('C:\\Users\\lenevo\\Downloads\\csv-' + searchWord + '-set.csv')
        data_json = json.loads(df.to_json(orient='records'))
        col.insert_many(data_json)

   if cb2.get()==1:
        scrape_IEEE()
        client = MongoClient("mongodb://localhost:27017/")
        db = client["IEEE"]
        col = db[searchWord]
        # verify the existence of the collection in the DataBase
        if searchWord in db.list_collection_names():
            col.drop()

        files = glob.glob('C:\\Users\\lenevo\\Downloads\\*')
        latest_file = max(files, key=os.path.getctime)
        df = pd.read_csv(latest_file,on_bad_lines='skip')
        data_json = json.loads(df.to_json(orient='records'))
        col.insert_many(data_json)

   if cb3.get()==1:
        scrape_Scopus()
        client = MongoClient("mongodb://localhost:27017/")
        db = client["Scopus"]
        col = db[searchWord]
        # verify the existence of the collection in the DataBase
        if searchWord in db.list_collection_names():
            col.drop()
        list_of_files = glob.glob('C:\\Users\\lenevo\\Downloads\\*')  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        df = pd.read_csv(latest_file)
        data_json = json.loads(df.to_json(orient='records'))
        col.insert_many(data_json)

   if cb4.get()==1:
        pages = scrape_UPSTO()
        client = MongoClient("mongodb://localhost:27017/")
        db = client["UPSTO"]
        col = db[searchWord]
        # verify the existence of the collection in the DataBase
        if searchWord in db.list_collection_names():
            col.drop()
        try:
           col.insert_many(pages)
        except:
           print('an error occurred quotes were not stored to db')

   if cb5.get()==1:
        title = scrape_WIPO()
        client = MongoClient("mongodb://localhost:27017/")
        db = client["WIPO"]
        col = db[searchWord]
        # verify the existence of the collection in the DataBase
        if searchWord in db.list_collection_names():
           col.drop()
        try:
            col.insert_many(title)
        except:
            print('an error occurred quotes were not stored to db')

   if cb6.get() == 1:
       scrape_Net()
       client = MongoClient("mongodb://localhost:27017/")
       db = client["Esp@ceNet"]
       col = db[searchWord]
       # verify the existence of the collection in the DataBase
       if searchWord in db.list_collection_names():
           col.drop()
       list_of_files = glob.glob('C:\\Users\\lenevo\\Downloads\\*')  # * means all if need specific format then *.csv
       latest_file = max(list_of_files, key=os.path.getctime)
       df = pd.read_csv(latest_file)
       data_json = json.loads(df.to_json(orient='records'))
       col.insert_many(data_json)

#interface de recherche

fen = Tk()
fen.title('Search Engine')
fen['bg']='#52688F'
frm = ttk.Frame(fen, height=400, width=400)
fen.geometry('1500x500')

lbl=Label(fen, text="Welcome to the fastest search engine in the world ^_^",bg='#52688F',font=("Arial", 15))
lbl.place(x=500 , y=10)
lbsearch=Label(fen, text="Search",bg='#BDC6D9',width=10,font=("Arial", 12))
lbsearch.place(x=500 , y=70)
entryword = Entry(fen,bd=4)
entryword.place(x=600 , y=70,width=300)

cb1 = IntVar()
lbbd1=Checkbutton(fen, text="PubMED",bg='#52688F', variable=cb1, onvalue=1, offvalue=0).grid(row=0, column=0,padx=300, pady=130)
cb2 = IntVar()
lbbd2=Checkbutton(fen, text="IEEE",bg='#52688F', variable=cb2, onvalue=1, offvalue=0).grid(row=0, column=1)
cb3 = IntVar()
lbbd3=Checkbutton(fen, text="Scopus",bg='#52688F', variable=cb3, onvalue=1, offvalue=0).grid(row=0, column=2,padx=200)
cb4 = IntVar()
lbbd4=Checkbutton(fen, text="USPTO",bg='#52688F', variable=cb4, onvalue=1, offvalue=0).grid(row=1, column=0)
cb5 = IntVar()
lbbd5=Checkbutton(fen, text="WIPO",bg='#52688F', variable=cb5, onvalue=1, offvalue=0).grid(row=1, column=1)
cb6 = IntVar()
lbbd6=Checkbutton(fen, text="Esp@ceNet",bg='#52688F', variable=cb6, onvalue=1, offvalue=0).grid(row=1, column=2)

valider =Button(fen,text="Extract",bg='#BDC6D9',width=10,font=("Arial", 12),command=action)
valider.place(x=600 , y=400,width=300)

fen.mainloop()