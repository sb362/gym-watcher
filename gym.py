import re
import requests
import time

from bs4 import BeautifulSoup
from threading import Timer
from twisted.internet import task, reactor

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
headers = {'User-Agent': user_agent}

def fetch_url(url: str):
  r = requests.get(url, headers=headers)
  if r.status_code == requests.codes.ok:
    return r.text
  else:
    raise RuntimeError(f"request failed with error {r.status_code} ({r.reason})")

def find_tags(html: str, tag: str):
  return BeautifulSoup(html,"html.parser").findAll(tag)

def find_first_pattern(tags, regex):
  for tag in tags:
    if m := re.match(regex, tag.text):
      return m

  raise RuntimeError(f"no matches found in {len(tags)} tag(s)")

def fetch_occupancy():
  html = fetch_url("https://sport.wp.st-andrews.ac.uk/")
  tags = find_tags(html, "h3")
  match = find_first_pattern(tags, r"Occupancy: ([0-9]+)%")
  return int(match.group(1))

def fetch_and_save():
  t = time.time()
  try:
    occ = fetch_occupancy()
    print(t, occ)
    
    with open("occupancy.csv", mode="a") as f:
      f.write(f"{t},{occ}\n")
  except RuntimeError as err:
    print(t, err)

if __name__ == "__main__":
  interval = 5 * 60
  loop = task.LoopingCall(fetch_and_save)
  loop.start(interval)
  
  reactor.run()
