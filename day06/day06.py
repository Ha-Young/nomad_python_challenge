import os
import requests
from bs4 import BeautifulSoup

os.system("clear")


url = "https://www.iban.com/currency-codes"
convert_url = "https://transferwise.com/gb/currency-converter"

countries = []

request = requests.get(url)
soup = BeautifulSoup(request.text, "html.parser")

table = soup.find("table")
rows = table.find_all("tr")[1:]

for row in rows:
    items = row.find_all("td")
    name = items[0].text
    code = items[2].text
    if name and code:
        if name != "No universal currency":
            country = {
                'name': name.capitalize(),
                'code': code
            }
            countries.append(country)


def ask_country(askMessage):
    try:
        print(askMessage)
        choice = int(input("#: "))
        if choice > len(countries):
            print("Choose a number from the list.\n")
            return ask_country(askMessage)
        else:
            print(countries[choice]['name'], end='\n\n')
            return countries[choice]
    except ValueError:
        print("That wasn't a number.\n")
        return ask_country(askMessage)


def ask_amount(from_country_code, to_country_code):
    try:
        print(
            f"How many {from_country_code} do you want to convert to {to_country_code}")
        amount = int(input())
        return amount
    except ValueError:
        print("That wasn't a number.\n")
        return ask_amount(from_country_code, to_country_code)


def get_convert_money(from_code, to_code, amount):
    url_convert = f"{convert_url}/{from_code}-to-{to_code}-rate?amount={amount}"
    req = requests.get(url_convert)
    soup = BeautifulSoup(req.text, 'html.parser')
    convert_money = soup.select(".text-success")[0].text.strip()
    return int(float(convert_money) * amount)


print("Welcome to CurrencyConvert PRO 2000\n")
for index, country in enumerate(countries):
    print(f"#{index} {country['name']}")

from_country_code = ask_country(
    "Where are you from? Choose a country by number\n")['code']

to_country_code = ask_country("Now Choose another country")['code']

convert_amount = ask_amount(from_country_code, to_country_code)

converted_amount = get_convert_money(
    from_country_code, to_country_code, convert_amount)

print(f"{from_country_code} {format(convert_amount, ',')} is {to_country_code} {format(converted_amount, ',')}")
