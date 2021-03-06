from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import smtplib

char = ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
names = []
office = []
city = []
links = [] 
phones = []
df = pd.DataFrame()
p = 1
for ch in char:
  url = 'https://www.car.org/Find-a-REALTOR/?ln='+ch
  req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
  webpage = urlopen(req).read()
  page_soup = soup(webpage, 'html.parser')
  totalCount = page_soup.findAll('div','metadataSection')[0]
  totalCount = int(str(totalCount)[str(totalCount).find('<span>')+6:str(totalCount).find('</span>')])
  totalCount = int(totalCount/10)
  x = 1
  if ch == 'B':
      p = 4
      x= 301
  for i in range(x,totalCount):
    try:
        url = 'https://www.car.org/Find-a-REALTOR/?page='+str(i)+'&ln='+ch
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        page_soup = soup(webpage, 'html.parser')
        allNames = page_soup.findAll('td')
        print("Page ",i)
        for s in range(0,30,3):
            names.append(str(allNames[s])[str(allNames[s]).find(';"')+3:str(allNames[s]).find('</a>')])
            links.append(str(allNames[s])[str(allNames[s]).find('href="')+6:str(allNames[s]).find(' style')-1])
            office.append(str(allNames[s+1])[str(allNames[s+1]).find(';"')+3:str(allNames[s+1]).find('</a>')])
            city.append(str(allNames[s+2])[str(allNames[s+2]).find(';"')+3:str(allNames[s+2]).find('</a>')])
        for li in links:
            url = li
            print(li)
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            page_soup = soup(webpage, 'html.parser')
            allNames = page_soup.findAll('div','address')
            phones.append(str(allNames)[str(allNames).find('officePhoneNumber')+43:str(allNames).find('officePhoneNumber')+57])
        links = []
        if i%100 == 0:
            print("Adding CSV "+str(p)+ch)
            nameOfFile = str(p)+ch+'.csv'
            p = p+1
            df["name"] = pd.Series(names)
            df["office"] = pd.Series(office)
            df["city"] = pd.Series(city)
            df["phones"] = pd.Series(phones)
            df.to_csv(nameOfFile)
            names = []
            office = []
            city = []
            phones = []
    except Exception as e:
	    print(str(e))
  p=1
  names = []
  office = []
  city = []
  phones = []
