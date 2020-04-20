import requests as req
import sys
import os

while(True):
  print("Welcom to IsItDown.py!")
  print("Please write a URL or URLs you want to check. (separeated by comma)")
  inputUrls = map(str.strip, sys.stdin.readline().split(','))

  for url in inputUrls:
    if ".com" not in url:
      print(f"{url} is not valid url")
      continue

    if "http://" not in url:
      url = "http://" + url
    try:
      res = req.get(url)

      if res.status_code == req.codes.ok:
        print(f"{url} is up!")
      else:
        print(f"{url} is down!")

    except:
      print(f"{url} is down!")
    
  restart = None
  while True:
    restart = input("Do you Want to start over? y/n ")
    if restart == "y" or restart == "n":
      break
    else:
      print("is not valid answer")

  if restart == "n":
    break
  elif restart == "y":
    os.system('clear')

print("bye")