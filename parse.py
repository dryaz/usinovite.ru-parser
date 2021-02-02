import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd 
import re

finalData = []

with open('source.txt') as f:
    lines = [line.rstrip() for line in f]

def handleUrl(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")

    bs = BeautifulSoup(html, 'html.parser')
    
    name = bs.find("h2", {"class": "search-bd__slaider--content_title"}).contents[0]
    content = bs.findAll("p", {"class": "search-bd__slaider--content_text"})

    print("name: {}".format(name))

    row = {'Name': name, 'Url': url} 

    for entry in content:
        rowData = str(entry.contents[0]).split(":")

        if rowData[0] == "Регион":
            row["Region"] = rowData[1]
        elif rowData[0] == "Группа здоровья":
            row["Health"] = rowData[1]
        elif "родил" in str(rowData[0]):
            row["Birth"] = rowData[0]
        elif rowData[0] == "Возможные формы устройства":
            row["Status"] = rowData[1]

    finalData.append(row)
    time.sleep(0.5)

for line in lines:
    handleUrl(line)

df = pd.DataFrame(finalData) 

# saving the dataframe 
df.to_csv('children.csv') 
