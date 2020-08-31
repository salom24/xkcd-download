#!/usr/bin/env python3
# kxcd.py - Download the comics from XKCD.

import requests, os, bs4

base = "http://xkcd.com"

# Check the folders
path = os.path.join(os.environ["HOME"], "Pictures")
if not os.path.isdir(path):
    os.makedirs(path)

path = os.path.join(path, "XKCD")
if not os.path.isdir(path):
    os.makedirs(path)

def download(url):
    # Download page and parse
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "lxml")

    # Find title
    title = soup.find(id="ctitle").string + ".png"
    title = title.replace("/", "-")
    title = title.replace("\\", "-")

    # If not downloaded, do the magic!
    if not os.path.exists(os.path.join (path, title)):
        # Get and next image url
        nexturl = base + soup.find(rel="prev")["href"]
        # Download if there is an image
        if soup.find(id="comic").img:
            imgUrl = "http:" + soup.find(id="comic").img["src"]
            imgFile = open(os.path.join(path, title), "wb")

            # Download and save image
            print("Downloading ", title)
            res = requests.get(imgUrl)
            res.raise_for_status()
            for chunk in res.iter_content(100000):
                imgFile.write(chunk)
            imgFile.close()
            del res

        # Iterate to next image
        download(nexturl)

# Start loop
download(base)
print("Up to date!")
