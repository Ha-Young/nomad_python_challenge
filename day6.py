import os
import requests
from bs4 import BeautifulSoup

os.system("clear")


url = "https://www.iban.com/currency-codes"
convert_url = "https://transferwise.com/gb/currency-converter"

def get_countries():
  tmp_countries = []

  request = requests.get(url)
  soup = BeautifulSoup(request.text, "html.parser")

  table = soup.find("table")
  rows = table.find_all("tr")[1:]

  for row in rows:
    items = row.find_all("td")
    name = items[0].text
    currency = items[1].text
    code =items[2].text
    if name and code:
      if currency != "No universal currency":
        country = {
          'name':name.capitalize(),
          'code': code
        }
        tmp_countries.append(country)

  return tmp_countries

def ask_country():
  try:
    choice = int(input("#: "))
    if choice > len(countries):
      print("Choose a number from the list.")
      print()
      ask_country()
    else:
      chooseCountry = countries[choice]
      print(f"{chooseCountry['name']}")
      print()
      return chooseCountry
  except ValueError:
    print("That wasn't a number.")
    print()
    ask_country()

def ask_amount():
  try:
    print(f"How many {country1['code']} do you want to convert to {country2['code']}?")
    amount = int(input())
    return amount
  except ValueError:
    print("That wasn't a number.")
    print()
    ask_amount()

def get_convert_money(from_code, to_code, amount):
  url_convert = f"{convert_url}/{from_code}-to-{to_code}-rate?amount={amount}"
  print(url_convert)
  req = requests.get(url_convert)
  soup = BeautifulSoup(req.text, 'html.parser')
  convert_money = soup.select("#cc-amount-to")[0]['value']
  return int(convert_money.split('.')[0])

print("Hello! Please choose select a country by number:")
countries = get_countries()
for index, country in enumerate(countries):
  print(f"#{index} {country['name']}")

print("Where are you from? Choose a country by number")
print()
country1 = ask_country()
print("Now choose another country")
country2 = ask_country()

country1_code = country1['code']
country2_code = country2['code']

amount = ask_amount()
convert_money = get_convert_money(country1_code, country2_code, amount)
print(f"{country1_code}{format(amount, ',')} is {country2_code}{format(convert_money, ',')}")