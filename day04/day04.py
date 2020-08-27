import requests


def checkIsOnline(url):
    if 'com' not in url:
        print(f"{url} is not valid url")
        return False

    if 'http://' not in url:
        url = "http://" + url

    try:
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            print(f"{url} is up!")
        else:
            print(f"{url} is down!")

    except expression:
        print(f"{url} is down!")


def isEndInput():
    print("Do you want to start over? (y/n)")
    anwser = input()
    if anwser == "y" or anwser == "yes":
        return True
    elif anwser == "n" or anwser == "no":
        return False
    else:
        print("is not valid answer")
        return True


while True:
    print("Welcome to IsItDown.py!")
    print("Please write a URL or  URL's you want to check. (separated by comma)")

    urls = input()

    urls = urls.split(',')

    for url in urls:
        url = url.strip()
        checkIsOnline(url)

    if isEndInput():
        break

print("bye")
