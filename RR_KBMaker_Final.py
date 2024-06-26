from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
from unidecode import unidecode

chno = 75
chosen_options = Options()
chosen_options.add_argument("--headless")
chromedriver_loc = "/usr/local/bin/chromedriver_v126"
contentTextArr=[] #List to store name of the product
init_link = "https://www.royalroad.com/fiction/68679/return-of-the-runebound-professor/chapter/1439964/chapter-303-if-all-your-friends"
bookName = str(init_link.split("/")[5])
titles = [str(init_link.split("/")[6])]

print("-"*5,"START","-"*5)

driver = webdriver.Chrome(chromedriver_loc,options =chosen_options)
driver.get(init_link)

def create_rr_file(fname, titles, contentTextArr):
    print ("Writing File..")
    with open(fname+".html", "w", encoding="utf-8") as f:  #----> FOR HTML FILE
        f.write("<HTML><BODY>")
        for title, chapterContent in list(zip(titles, contentTextArr)):
            #Add chapter content - This includes all the headers already within the website (title unnecessary
            f.write("<center><h1>"+str(title)+"</h1></center>")
            f.write(str(unidecode(str(chapterContent))))
        f.write("</BODY></HTML>")
        f.close()

for i in range(0,chno):
    print("Iteration No:",i, end=" | ")
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    element = soup.find(class_='chapter-inner chapter-content')
    contentTextArr.append(element)
    linkhub = soup.find(class_ = "row margin-bottom-10 margin-left-0 margin-right-0").find_all("a")
    linklist = []
    for link in linkhub:
        linklist.append(link.get('href'))
    #print(str(linklist[-1]).split("/")[6])
    titles.append(str(linklist[-1]).split("/")[6])
    driver.get('https://www.royalroad.com'+str(linklist[-1]))

fname = str(bookName)+'_'+str(titles[0])+'-'+str(titles[-2])
create_rr_file(fname, titles, contentTextArr)
driver.close()
print ("Process completed")

