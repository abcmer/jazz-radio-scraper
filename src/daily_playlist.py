from datetime import datetime
import pprint

from bs4 import BeautifulSoup
import requests

class WCDBDailyPlaylist:
	"""Scrapes data from https://wdcb.org/playlist."""
	def __init__(self, date):
		self.html_data = None
		self.data = None
		self.date = date
		self.set_data()

	def print(self):
		for song in self.data:
			print(song)
			
	def set_data(self):
		self.html_data = WCDBDailyPlaylist.fetch_html_data(self.date)
		self.data = self.parse_playist_from_html_data()	

	def get_data(self):
		return self.data	

	def parse_playist_from_html_data(self):
		# Create soup object
		soup = BeautifulSoup(self.html_data, 'html.parser')

		# Initialize DJ
		dj_name = None

		# Parse date string
		date_str_long = str(soup.h1).split('<h1>Daily Playlist for:<br/>')[1].replace('</h1>', '')
		date_str = WCDBDailyPlaylist.parse_date_string(date_str_long)

		# Parse songs
		table = soup.find('table', attrs={'class':'table table-striped'})
		rows = table.find_all('tr')
		playlist_data = []
		for row in rows:
			values = row.find_all('td')
			values = [ele.text.strip() for ele in values]

			# Conditional check of record type
			# Records are either of type song or djSet

			# Check for dj set
			if '\t\t\t\t\t\t\t\t' in values[0]:
				dj_name = WCDBDailyPlaylist.parse_dj_name(values[0])
				set_name = WCDBDailyPlaylist.parse_set_name(values[0])
			else:
				# Transform data record
				record = WCDBDailyPlaylist.transform_data_record(values[0])	
				record['date'] = date_str	
				record['dj_name'] = dj_name		
				playlist_data.append(record)
		return playlist_data
			

	@staticmethod
	def fetch_html_data(date=None):
		data = {
			'date': date,
			'submit': 'go'
		}
		headers = {
			"Content-Type": "application/x-www-form-urlencoded"
		}
		url = "https://wdcb.org/playlist"
		response = requests.post(url, headers=headers, data=data)
		assert response.status_code == 200
		return response.text

	@staticmethod
	def parse_date_string(date_string):		
		try:
			return str(datetime.strptime(date_string, "%A - %B %d, %Y"))[0:10]
		except:
			print("date_str_long not valid")

	@staticmethod
	def parse_dj_name(record):
		if ' with ' in record:
			return record.split('with ')[1].split('\r')[0]
		else:
			return None

	@staticmethod
	def parse_set_name(record):
		if ' with ' in record:
			return record.split(' with')[0]
		else:
			return record.split('\r')[0]

	@staticmethod
	def transform_data_record(record):
		return {
			'time': record.split('TIME: ')[1].split(' TITLE')[0],
			'title': record.split('TITLE: "')[1].split('\n')[0][0:-1],
			'artist': record.split('ARTIST: ')[1].split('\n')[0],
			'album': record.split('ALBUM: ')[1].split('\n')[0]
		}


if __name__ == '__main__':
	playlist = WCDBDailyPlaylist('2021-02-13')

