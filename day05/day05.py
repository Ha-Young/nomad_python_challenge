import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"

req = requests.get(url)

soup = BeautifulSoup(req.text, "html.parser")

table = soup.find('table', {'class': 'table'})
tbody = table.find('tbody')

trs = tbody.find_all('tr')
dict_country_code = {}

for i, tr in enumerate(trs):
  tds = tr.find_all('td')

  country = tds[0].text.strip()
  currency = tds[1].text.strip()
  code = tds[2].text.strip()
  number = tds[3].text.strip()
  
  dict_country_code[i] = {
    'country':country, 
    'currency': currency, 
    'code': code, 
    'number':number
  }

print("Hello Please Choose select a country")

for key, value in dict_country_code.items():
  print(key,value['country'])

while(True):
  try:
    inputNum = int(input('#: '))
    if inputNum not in dict_country_code.keys():
      print("Choose a number from the list.")
    else :
      print('You Chose',dict_country_code[inputNum]['country'])
      print('The currency code is',dict_country_code[inputNum]['code'])
      break
  except:
    print("That wasn't a number")
