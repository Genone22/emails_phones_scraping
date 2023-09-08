#!/usr/bin/env python3

import coloredlogs
import logging
from threading import Thread
from queue import Queue
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests_random_user_agent

requests.packages.urllib3.disable_warnings()

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)
coloredlogs.install(logger=logger)


# Function to remove duplicates
def remove_dup_email(x):
	return list(dict.fromkeys(x))


def remove_dup_phone(x):
	return list(dict.fromkeys(x))


# Functions to get information
def get_email(html):
    try:
        email = re.findall("[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}", html)
        nodup_email = remove_dup_email(email)
        return [i.strip() for i in nodup_email]
    except Exception as e:
        logger.error(f"Email search error: {e}")



def get_phone(html):
	try:
		phone_pattern = r"(?:(?:8|\+7)[\- ]?)?(?:\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}"
		phone = re.findall(phone_pattern, html)
		nodup_phone = remove_dup_phone(phone)
		return [i.strip() for i in nodup_phone]
	except Exception as e:
		logger.error(f"Phone search error: {e}")


def read_file():
	urls = []
	with open('web_urls.txt', 'r') as f:
		for line in f.readlines():
			url = line.strip()
			if not url.startswith('http'):
				url = 'https://' + url
			urls.append(url)
	return urls


def crawl(q, result):
	while not q.empty():
		url = q.get()
		try:
			url_utf8 = url[1].encode('utf-8')
			res = requests.get(url_utf8, verify=False)
			logger.info(f'Searched home URL: {res.url}')

			if res.status_code != 200:
				result[url[0]] = {}
				logger.warning(f"{url[1]} Status code: {res.status_code}")
				continue

			info = BeautifulSoup(res.content, 'lxml',
			                     from_encoding=res.encoding)
			emails_home = get_email(info.get_text())
			phones_home = get_phone(info.get_text())

			contacts_f = {'website': res.url, 'Email': '', 'Phone': ''}

			try:
				contact_element = info.find('a', string=re.compile('contact',
				                                                 re.IGNORECASE))
				if contact_element:
					contact = contact_element.get('href')
					if 'http' in contact:
						contact_url = contact
					else:
						contact_url = res.url[0:-1] + "/" + contact

					res_contact = requests.get(contact_url, verify=False)
					contact_info = BeautifulSoup(res_contact.content,
					                             'lxml',
					                             from_encoding=res_contact.encoding).get_text()

					logger.info(f'Searched contact URL: {res_contact.url}')

					emails_contact = get_email(contact_info)
					phones_contact = get_phone(contact_info)

					emails_f = emails_home + emails_contact
					phones_f = phones_home + phones_contact

				else:
					emails_f = emails_home
					phones_f = phones_home

				emails_f = remove_dup_email(emails_f)
				phones_f = remove_dup_phone(phones_f)

				contacts_f['Email'] = emails_f[0] if emails_f else ''
				contacts_f['Phone'] = phones_f[0] if phones_f else ''

				result[url[0]] = contacts_f

			except Exception as e:
				logger.error(f'Error in contact URL: {e}')
				result[url[0]] = {}

		except Exception as e:
			logger.error(f"Request error in threads: {e}")
			result[url[0]] = {}
		finally:
			q.task_done()
			logger.debug(f"Queue task no {url[0]} completed.")
	return True


def main():
	urls = read_file()

	q = Queue(maxsize=0)
	num_threads = min(50, len(urls))
	results = [{} for x in urls]

	for i in range(len(urls)):
		q.put((i, urls[i]))

	for i in range(num_threads):
		logger.debug(f"Starting thread: {i}")
		worker = Thread(target=crawl, args=(q, results))
		worker.daemon = True
		worker.start()

	q.join()

	df = pd.DataFrame(results)
	excel_file = 'websites_info.xlsx'
	df.to_excel(excel_file, index=False)


if __name__ == "__main__":
	main()
