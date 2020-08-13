from bs4 import BeautifulSoup
import requests
import os
from termcolor import colored
import re
import urllib.request
import argv from sys

# clear the CLI
os.system("clear")

url = "https://google.com/search?hl=en&gl=en&q="
raw_film = input("What film do you want to download?\nHint: better if you put the film\'s full name and the year it was released on. - Example: \"interstellar 2014\".\n")
if raw_film == "":
    raw_film = "interstellar 2014"

print('\nSearching for the film "{}"...'.format(raw_film))
token = raw_film + " film"
url = (url + token).replace(" ", "+")
res = requests.get(url)
html_page = res.content
soup = BeautifulSoup(html_page, 'html.parser')

try:
    film = soup.find_all("div", {"class": "BNeawe deIvCb AP7Wnd"})[0].text
    details = (soup.find_all("div", {"class": "BNeawe tAd8D AP7Wnd"})[
               0].text).split(" ‧ ")
    year = details[0]
    full_film = str(film) + ", " + str(year)
except:
    print(colored("Film not found on Google. Nothing changed.", "red"))
    exit()
try:
    z = int(year)
except:
    print(colored("Specific film not found on Google. Try putting the film's number from its series. - Example: \"How to train your dragon 1\".", "red"))
    exit()

ans = input("Is {} the film you're looking for?\n[(y)es / (n)o / see (d)etails]: ".format(
    colored(full_film, "blue"))).lower()

# Used to sterilize film_name to be appropriate


def sterilizer(film_name):
    film_name = film_name.lower().replace(",", "").replace(" ", "-")
    film_name = film_name.replace(":", "").replace("!", "")
    film_name = film_name.replace("&", "")
    film_name = film_name.replace("--", "-").replace("---", "")
    return film_name


if ans == "y" or "":
    full_film = sterilizer(full_film)
elif ans == "d":
    print("\nExtra info:")
    for detail in details:
        print(colored(detail, "blue"))
    if input("Is this the film you're looking for?\n[(y)es / (n)o]: ").lower() == "y":
        full_film = sterilizer(full_film)
    else:
        print(colored(
            "Try repeating the search using the film's full name and/or its release date.", "red"))
        exit()
else:
    print(colored("Try repeating the search using the film's full name and/or its release date.", "red"))
    exit()

# print(full_film)
url = "https://yst.am/movie/{}".format(full_film)
res = requests.get(url)
html_page = res.content
soup = BeautifulSoup(html_page, 'html.parser')

ans = 0

downloads = soup.find_all("p", {"class": "hidden-xs hidden-sm"})
downloads = str(downloads).split("\"")
torrents = [
    torrents for torrents in downloads if "/torrent/download/" in torrents]
sizes = [sizes for sizes in downloads if "Download " in sizes]
if len(torrents) == 0 and len(sizes) == 0:
    empty = True
    print(colored("\nFilm not found on YTS!", "red"))
else:
    empty = False
n = 0
quality_list = list()
for size in sizes:
    quality = re.sub("[^0-9]", "", str(size))
    if quality and quality not in quality_list:
        quality_list.append(quality)
        print(str(colored(n, "blue")) + ": " + quality)
        n += 1
while not empty:
    ans = input(
        "Select the resolution you want to download from the list above.\n[(0) -> {} / ...]: ".format(re.sub("[^0-9]", "", str(sizes[0]))))
    try:
        ans = int(ans)
    except:
        print(colored("Not a number. You must select a number that's on the list.", "red"))
        continue
    if ans < n:
        break
    else:
        print(colored("Out of range. You must select a number that's on the list.", "red"))

try:
    path = "/home/abdo/Downloads"
    torrent = "https://yst.am" + torrents[ans]
    print("Got torrent's URL: " + colored(torrent, "green"))

    user_opinion = input(
        "Open and download torrent now?\n[(y)es / (n)o]: ")
    if user_opinion == "y":
        try:
            urllib.request.urlretrieve(
                torrent, path + full_film + ".torrent")
        except:
            print(colored(
                "Error while downloading the torrent. However, you can try opening manually the URL above.", "red"))
        try:
            # Open torrent file with appropriate software
            os.system("xdg-open {}.torrent".format(path + full_film))
        except:
            print(colored(
                "Error while opening the torrent. However, it has been saved in " + path, "red"))
    else:
        print('Nothing changed.')
        exit()


except:
    print(colored("Torrent error. Nothing changed.", "red"))
    exit()

print('Done :)')
exit()
