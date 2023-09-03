
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as BeautifulSoup
import csv
# my_url = "https://www.quora.com/topic/Third-Battle-of-Panipat-January-1761/all_questions"

# uclient = uReq(my_url)
# page_html = uclient.read()
# uclient.close()
# page_soup = BeautifulSoup(page_html,"html.parser")
# div = page_soup.findAll("div",{"class":"pagedlist_item"})
# print(len(div))
import mysql.connector
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
url = "https://www.quora.com/search?q=shivaji%20maharaj&type=question"
scrollTime = 5
limit=10
driver = webdriver.Chrome()
driver.get(url)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="leadingAi"
)

print(mydb)

mycursor = mydb.cursor()


div = []
#links={}
elm = driver.find_element_by_tag_name('html')

while(len(div)<limit):
	elm.send_keys(Keys.END)
	time.sleep(scrollTime)
	elm.send_keys(Keys.HOME)
	source_data = driver.page_source
	page_soup = BeautifulSoup(source_data,"html.parser")
	div = page_soup.findAll("div",{"class":"pagedlist_item"})
	print(len(div))


print(len(div))
with open('beneficiary.csv','w') as newFile:
	newFileWriter = csv.writer(newFile)
	for i in range(0,len(div)):
		print(div[i].text)
		links = div[i].findAll("a")
		print('https://www.quora.com'+links[0]['href'])
		newFileWriter.writerow([div[i].text,'https://www.quora.com'+links[0]['href']])
		sql = "INSERT INTO quora (question, link ) VALUES (%s, %s)"
		val = (div[i].text,'https://www.quora.com'+links[0]['href'])
		mycursor.execute(sql, val)

		mydb.commit()

print(mycursor.rowcount, "record inserted.")
# Now that the page is fully scrolled, grab the source code.
#source_data = browser.page_source









