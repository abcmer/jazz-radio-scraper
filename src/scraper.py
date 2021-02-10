from abc import ABC

from bs4 import BeautifulSoup
import requests

class WDCBWebScraper:
	"""Scrapes data from https://wdcb.org/playlist."""
	def __init__(self):
		self.html_data = None
		self.playlist_data = None

	@staticmethod
	def fetch_html_data():
		url = "https://wdcb.org/playlist"
		response = requests.get(url)
		assert response.status_code == 200
		return response.text

	@staticmethod
	def parse_date_string(date_str_long):
		try:
			# Parse Year from date_str_long
			year = date_str_long.split(', ')[1]

			# Parse Month string and convert it to integer
			# Ex. January=1, February=2			
			month_str = date_str_long.split(' - ')[1].split(' ')[0]
			months_to_ints = {
				"January": 1,
				"February": 2,
				"March": 3,
				"April": 4,
				"May": 5,
				"June": 6,
				"July": 7,
				"August": 8,
				"September": 9,
				"October": 10,
				"November": 11,
				"December": 12
			}
			month = str(months_to_ints[month_str]).zfill(2)

			# Parse Day
			day = date_str_long.split(' ')[3].replace(',','')

			return f'{year}-{month}-{day}'

		except:
			print("date_str_long not valid")

	@staticmethod
	def transform_data_record(record):
		return {
			'time': record.split('TIME: ')[1].split(' TITLE')[0],
			'title': record.split('TITLE: "')[1].split('\n')[0][0:-1],
			'artist': record.split('ARTIST: ')[1].split(' \n')[0],
			'album': record.split('ALBUM: ')[1].split('\n')[0]
		}

	def set_html_data(self):
		self.html_data = WDCBWebScraper.fetch_html_data()
		return self

	def parse_html_data(self):
		# Create soup object
		soup = BeautifulSoup(self.html_data, 'html.parser')

		# Parse date string
		date_str_long = str(soup.h1).split('<h1>Daily Playlist for:<br/>')[1].replace('</h1>', '')
		date_str = WDCBWebScraper.parse_date_string(date_str_long)

		# Parse songs
		table = soup.find('table', attrs={'class':'table table-striped'})
		rows = table.find_all('tr')
		data = []
		for row in rows:
			values = row.find_all('td')
			values = [ele.text.strip() for ele in values]

			# Transform data record
			record = WDCBWebScraper.transform_data_record(values[0])
			# import pdb; pdb.set_trace()	
			record['date'] = date_str			
			data.append(record)
		self.playlist_data = data
	

if __name__ == '__main__':
	scraper = WDCBWebScraper()
	scraper.set_html_data()
	scraper.parse_html_data()
