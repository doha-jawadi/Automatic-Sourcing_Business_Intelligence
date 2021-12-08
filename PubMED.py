import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pymongo
from tkinter import *
from tkinter import ttk
from pymongo import MongoClient
import pandas as pd
import json

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
    format.select_by_value('pubmed-text')
    time.sleep(1)

    driver.find_element(By.CLASS_NAME, 'action-panel-submit').click()
    time.sleep(100)

    driver.close()

def action():
   searchWord = str(entryword.get())
   scrape_PM()
   client = MongoClient("mongodb://localhost:27017/")
   db = client["PubMed"]
   col = db[searchWord]
   # verify the existence of the collection in the DataBase
   if searchWord in db.list_collection_names() :
       col.drop()

   searchWord = searchWord.replace(" ", "")

   while (len(searchWord) > 10):
       searchWord = searchWord.rstrip(searchWord[-1])
    #erreur sur l'importation du fichier txt en mongodb
   df = pd.read_csv('C:\\Users\\lenevo\\Downloads\\pubmed-'+searchWord+'-set.txt')
   data_json = json.loads(df.to_json(orient='records'))
   col.insert_many(data_json)


#interface de recherche

fen = Tk()
fen.title('Search Engine')
frm = ttk.Frame(fen, height=400, width=400)
frm.grid()
lbl=Label(fen, text="Welcome to the fastest search engine in the world ^_^",background='magenta')
lbl.place(x=50 , y=10)
lbsearch=Label(fen, text="Search")
lbsearch.place(x=80 , y=70)
entryword = Entry(fen)
entryword.place(x=150 , y=70)
lbbd1=Label(fen, text="PubMED")
lbbd1.place(x=50 , y=120)
slctbd1 = Checkbutton(fen)
slctbd1.place(x=100 , y=120)

lbbd2=Label(fen, text="IEEE")
lbbd2.place(x=150 , y=120)
slctbd2 = Checkbutton(fen)
slctbd2.place(x=200 , y=120)

lbbd3=Label(fen, text="Scopus")
lbbd3.place(x=250 , y=120)
slctbd3 = Checkbutton(fen)
slctbd3.place(x=320 , y=120)

lbbd4=Label(fen, text="USPTO")
lbbd4.place(x=50 , y=150)
slctbd4 = Checkbutton(fen)
slctbd4.place(x=100 , y=150)

lbbd5=Label(fen, text="WIPO")
lbbd5.place(x=150 , y=150)
slctbd5 = Checkbutton(fen)
slctbd5.place(x=200 , y=150)

lbbd5=Label(fen, text="Esp@ceNet")
lbbd5.place(x=250 , y=150)
slctbd5 = Checkbutton(fen)
slctbd5.place(x=320 , y=150)

valider =Button(fen,text="Extract",command=action)
valider.place(x=180 , y=200)

fen.mainloop()