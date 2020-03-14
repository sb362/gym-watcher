#!/usr/bin/env python3
import logging
import time
import re
from functools import partial
from threading import Timer

import requests
from bs4 import BeautifulSoup

from twisted.internet import task, reactor


logging.basicConfig(format="%(asctime)s %(filename)s:%(lineno)d (%(funcName)s) %(levelname)s : %(message)s")


def call_delayed(delay, f, *args, **kwargs):
	Timer(delay, f, args=args, kwargs=kwargs).start()


def query(url: str, tag: str, pattern: str, on_success: callable, retries: int = 5):
	r = requests.get(url)
	if r.status_code == requests.codes.ok:
		soup = BeautifulSoup(r.text, "html.parser")

		for h3 in soup.find_all(tag):
			if match := re.match(pattern, str(h3)):
				on_success(match)
				return True

		logging.error(f"{url} - could not match {pattern}.")

	else:
		logging.error(f"{url} - failed with code {r.status_code}, retries left: {retries}")

		if retries > 0:
			call_delayed(30, query, url, pattern, on_success, retries - 1)

	return False


def watch_me_roll(match):
	occupancy = int(match.group(1))
	logging.debug(f"Occupancy: {occupancy}%")

	with open("occupancy.csv", mode="a") as f:
		f.write(f"{time.time()},{occupancy}\n")


crank_that = partial(query, "https://www.st-andrews.ac.uk/sport/", "h3", r"<h3>Occupancy: ([0-9]+)%</h3>", watch_me_roll)

loop = task.LoopingCall(crank_that)
loop.start(60. * 3)

reactor.run()
