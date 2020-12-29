from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import smtplib
names = []
numbs = []
addressFinals = []
p = 1
for i in range(1,5440):
  try:
    url = 'https://www.texasrealestate.com/realtors/realtor-search-results/?results_page='+str(i)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    print("page "+ str(i))
    webpage = urlopen(req).read()
    page_soup = soup(webpage, 'html.parser')
    allNames = page_soup.findAll('h5', 'realtor-name')
    allAddress = page_soup.findAll('div', 'realtor-address')
    for addres in allAddress:
      seperateAdd = addres.findChildren("div")
      addressFinals.append(str(seperateAdd[0])[5:-6] +" "+ str(seperateAdd[1])[5:-6] + " " + str(seperateAdd[2])[29:-6])
    for name in allNames:
      names.append(str(name)[63:(str(name)[63:].find('<')+63)])
      url = 'https://www.texasrealestate.com'+str(name)[34:61]
      req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
      webpage = urlopen(req).read()
      page_soup = soup(webpage, 'html.parser')

      numbers = page_soup.findAll('div','realtor-profile-intro')

      for num in numbers:
        n = str(num.find('p').text)[num.find('p').text.find('('):]
        numbs.append(n)
    if(i%50 == 0):
      df = pd.DataFrame()
      newNumbs = []
      for n in numbs:
        nu = n[:n.find('\r')]
        if len(str(nu)) != len('(281) 292-3499') :
          newNumbs.append("NULL")
        else:
          newNumbs.append(str(n[:n.find('\r')]))

      df["Names"] = names[:len(newNumbs)]
      df["Numbers"] = newNumbs
      df["Address"] = addressFinals[:len(newNumbs)]
      addressFinals = []
      newNumbs = []
      numbs = []
      names = []
      nameOfFile = "new"+str(p)+".csv"
      print("Adding "+ nameOfFile)
      df.to_csv(nameOfFile)
      df = pd.DataFrame()
      s = smtplib.SMTP('smtp.gmail.com', 587)
      s.starttls() 
      s.login("sharjeelabbas014@gmail.com", "ozvgfsespnifsxmp")
      message = nameOfFile = "new"+str(p)+".csv"
      s.sendmail("sharjeelabbas014@gmail.com", "sharjeelabbas014@gmail.com", message) 
      s.quit() 
      p=p+1
  except Exception as e:
    print(str(e))
