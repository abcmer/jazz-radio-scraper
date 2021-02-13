from datetime import datetime

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
	def parse_date_string(date_string):		
		try:
			return datetime.strptime(date_string, "%A - %B %d, %Y")
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
			record['date'] = date_str			
			data.append(record)
		self.playlist_data = data
	

if __name__ == '__main__':
	scraper = WDCBWebScraper()
	scraper.set_html_data()
	scraper.parse_html_data()
