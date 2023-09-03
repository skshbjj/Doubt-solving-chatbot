import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as BeautifulSoup
import csv
import mysql.connector
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="leadingAi"
)
print(mydb)
#my_url="https://www.quora.com/Who-are-the-most-evil-humans-in-history-that-most-people-have-never-heard-of"

mycursor = mydb.cursor()
mycursor.execute ("Select id ,link, answer from quora")
r= mycursor.fetchall()

for x in r:
    print(x[1])
    my_url=x[1]
    #my_url=x[1].encode(encoding='UTF-8',errors='strict'))
    driver = webdriver.Chrome()
    driver.get(my_url)
    source_data = driver.page_source
    driver.quit()
    print("page loaded")
    page_soup = BeautifulSoup(source_data,"html.parser")
    div = page_soup.findAll("div",{"class":"pagedlist_item"})
    divu = div[0].findAll("div",{"class":"ui_qtext_expanded"})
    print(divu[0])
    sql = "UPDATE quora SET answer = %s WHERE id = %s"
    val = (str(divu[0]), x[0])
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")
     
