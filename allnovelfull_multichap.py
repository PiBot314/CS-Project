from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
from unidecode import unidecode

#When no more chapters, href = None
chosen_options = Options()
chosen_options.add_argument("--headless")
chromedriver_loc = "/usr/local/bin/chromedriver_v120"
driver = webdriver.Chrome(chromedriver_loc,options =chosen_options )
contentTextArr=[] #List to store name of the product
chapterCount = int(input("How many chapters? - "))
bookName = {
    'LOTM': "Lord of the Mysteries",
    'VM' : "VERSATILE MAGE",
    'LOG' : 'Life Once Again',
    'SG' : 'SUPER GENE',
    "ROTSSG" : "REINCARNATION OF THE STRONGEST SWORD GOD",
    'PM':"PERMANENT MARTIAL ARTS",
    'UMG':"UNRIVALED MEDICINE GOD",
    "SATS":"Scholars Advanced Technological System",
    "GMRY":"THE GREAT MAGE RETURNS AFTER 4000 YEARS",
    "LGM": "The Legendary Mechanic",
}
print("Book Shorts:")
for key, val in bookName.items():
    print(key,":",val)

chosenBook = bookName[input('Enter Book Short: ')]
chapStart = int(input('Enter the initial chapter: '))
linkBookName = chosenBook.lower().replace(' ', '-')
                 
def locate_book(bookName, firstChap):
    pgNo = ((firstChap-1)/50)+1
    driver.get('https://allnovelfull.net/'+linkBookName+'.html?page='+str(pgNo))
    content = driver.page_source
    soup = BeautifulSoup(content,features="html.parser")
    chapterList = driver.find_element_by_class_name("list-chapter")
    chapOne = chapterList.find_element_by_tag_name('a')
    driver.get(chapOne.get_attribute("href"))

def append_content(element, contentTextArr): #Requires Driver to be on correct page
    element = clean_element(element) #CLEAN ELEMENT FUNCTION TO BE CREATED
    contentTextArr.append(element)
    
def clean_element(soup):
    for ad in soup.find_all(class_ = "ads ads-holder ads-middle text-center"):
        ad.decompose()
    return soup

def create_file(chapter_name, contentTextArr):
    print ("Writing File..")
    with open(chapter_name+".html", "w", encoding="utf-8") as f:  #----> FOR HTML FILE
        f.write("<HTML><BODY>")
        chapterCounter=0
        for chapterContent in contentTextArr:
            #Add chapter content - This includes all the headers already within the website (title unnecessary
            f.write(str(unidecode(str(chapterContent))))
            #chapterCounter+=1
            #print("<BR/><HR/>")
        #f.write()

        f.write("</BODY></HTML>")
        f.close()

locate_book(chosenBook, chapStart)
for x in range(chapterCount):
    content = driver.page_source
    soup = BeautifulSoup(content)
    #Entirety of Page content in
    element = soup.find(id='chapter-content')
    append_content(element, contentTextArr)
    #append_title(element, chapterTitleArr)
    driver.get(driver.find_element_by_id('next_chap').get_attribute('href'))
    #print('-'*5+str(x))

file_name = str(linkBookName)+'_'+str(chapStart)+'-'+str(chapStart+chapterCount-1)
create_file(file_name, contentTextArr)
driver.quit()
print ("Process completed")
