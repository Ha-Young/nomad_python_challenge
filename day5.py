import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"

req = requests.get(url)

soup = BeautifulSoup(req.text, "html.parser")

table = soup.find('table', {'class':'table'})

trs = table.find_all('tr')
dict_words = {}

for idx, tr in enumerate(trs):
  tds = tr.find_all('td')
  if idx > 0:
    country = tds[0].text.strip()
    currency = tds[1].text.strip()
    code = tds[2].text.strip()
    num = tds[3].text.strip()
    dict_words[idx] = [country,currency,code,num]

print("Hello Please Choose select a country")
for k,v in dict_words.items():
  print("# ", k,v[0])

flag = True
while(flag):
  try:
    x = int(input('#: '))
    if x not in dict_words:
      print("Choose a number from the list.")
    else :
      print('You Chose',dict_words[x][0])
      print('The currency code is',dict_words[x][1])
      flag = False
  except:
    print("That wasn't a number")
