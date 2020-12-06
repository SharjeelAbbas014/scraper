from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import smtplib

char = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
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
  for i in range(1,totalCount):
    url = 'https://www.car.org/Find-a-REALTOR/?page='+str(i)+'&ln='+ch
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup = soup(webpage, 'html.parser')
    allNames = page_soup.findAll('td')
    for s in range(0,30,3):
      names.append(str(allNames[s])[str(allNames[s]).find(';"')+3:str(allNames[s]).find('</a>')])
      links.append(str(allNames[0])[str(allNames[0]).find('href="')+6:str(allNames[0]).find(' style')-1])
      office.append(str(allNames[s+1])[str(allNames[s+1]).find(';"')+3:str(allNames[s+1]).find('</a>')])
      city.append(str(allNames[s+2])[str(allNames[s+2]).find(';"')+3:str(allNames[s+2]).find('</a>')])
    for li in links:
      url = li
      req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
      webpage = urlopen(req).read()
      page_soup = soup(webpage, 'html.parser')
      allNames = page_soup.findAll('div','address')
      phones.append(str(allNames)[str(allNames).find('officePhoneNumber')+43:str(allNames).find('officePhoneNumber')+57])
      links = []
    if(i%100 == 0):
      nameOfFile = str(p)+ch+'.csv'
      p = p+1
      df["name"] = names
      df["office"] = office
      df["city"] = city
      df["phones"] = phones
      df.to_csv(nameOfFile)
      names = []
      office = []
      city = []
      phones = []
  nameOfFile = str(p)+ch+'.csv'
  df["name"] = names
  df["office"] = office
  df["city"] = city
  df["phones"] = phones
  df.to_csv(nameOfFile)
  names = []
  office = []
  city = []
  phones = []