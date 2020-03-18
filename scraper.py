import sys
import requests
import re
import pandas as pd

from time import localtime, strftime
from bs4 import BeautifulSoup


# URL to be scraped
url = 'https://github.com/torvalds/linux'
page = requests.get(url)

# Terminate Script if status code is not successful
if page.status_code != 200:
    sys.exit()

soup = BeautifulSoup(page.text, 'html.parser')


# Get current system time
currenttime = strftime("%X|%d:%m:%Y", localtime())


# Get number of commits
commitsraw: str = str(soup.find_all(class_='num text-emphasized')[0])
# Filter out everything but integers from commitsraw string
regex = re.findall(r'\d+', commitsraw)
cleancommits = ''.join([str(x) for x in regex])


# Pandas to extract data from csv
commitpanda = pd.read_csv("commits.csv")
# Get next ID ( ID is one if no entry exists)
ids = commitpanda.id
idList = ids.tolist()
try:
    nextid = str((idList[-1] + 1))
except IndexError:
    nextid = "1"


# Get new commits difference (new will be 0 if no entry exists)
new = commitpanda.commits
newList = new.tolist()
try:
    newcommits = str(int(cleancommits) - newList[-1])
except IndexError:
    newcommits = "0"


# Replace 'commits.csv' with desired path
# !!! csv file needs to have: 'id,commits,new,time' as first line before first script execution !!!
with open('commits.csv', 'a') as csvfile:
    csvfile.write(nextid + "," + cleancommits + "," + newcommits + f",{currenttime}\n")

# Replace 'commits.txt' with desired path
with open('commits.txt', 'a') as textfile:
    textfile.write(nextid + "\t" + cleancommits + "\t" + newcommits + f"\t {currenttime}\n")
