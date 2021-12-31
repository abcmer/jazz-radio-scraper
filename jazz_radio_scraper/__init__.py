from datetime import datetime, date

from bs4 import BeautifulSoup
import requests

class WCDBDailyPlaylist:
    """Scrapes data from https://wdcb.org/playlist."""
    def __init__(self, date):
        self.__html_data = None
        self.data = None
        self.date = date
        self.set_data()

    def print(self):
        for song in self.data:
            print(f"TIME: {song['time']}")
            print(f"TITLE: {song['title']}")
            print(f"ARTIST: {song['artist']}")
            print(f"ALBUM: {song['album']}")
            print(f"DJ: {song['dj_name']}")
            print(f"SET_NAME: {song['set_name']}")
            print(f"SET_TIMEFRAME: {song['set_timeframe']}")
            print('\n')

    def set_data(self):
        self.__html_data = WCDBDailyPlaylist.fetch_html_data(self.date)
        self.data = self.parse_playist_from_html_data()	

    def get_data(self):
        return self.data	

    def parse_playist_from_html_data(self):
        # Create soup object
        soup = BeautifulSoup(self.__html_data, 'html.parser')

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
            # Initialize a new empty record
            set_name = None
            dj_name = None
            set_timeframe = None

            # Find and clean table data values
            values = row.find_all('td')
            values = [ele.text.strip() for ele in values]
            record_raw = values[0]

            # Conditional check of record type
            # Records are either of type song or djSet

            # Check for dj set
            if '\t\t\t\t\t\t\t\t' in values[0]:
                dj_name = WCDBDailyPlaylist.parse_dj_name(record_raw)
                set_name = WCDBDailyPlaylist.parse_set_name(record_raw)
                set_timeframe = WCDBDailyPlaylist.parse_set_timeframe(record_raw)

            # Else record is type song
            # Parse song details
            else:
                time = WCDBDailyPlaylist.parse_time_from_songplay_record(record_raw)
                title = WCDBDailyPlaylist.parse_title_from_songplay_record(record_raw)
                artist = WCDBDailyPlaylist.parse_artist_from_songplay_record(record_raw)
                album = WCDBDailyPlaylist.parse_album_from_songplay_record(record_raw)
                # Update details of empty record
                playlist_data.append({
                    'date': date_str,
                    'time': time,
                    'dj_name': dj_name,
                    'set_name': set_name or None,
                    'set_timeframe': set_timeframe,
                    'title': title,
                    'artist': artist,
                    'album': album					
                    })
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
        return str(datetime.strptime(date_string, "%A - %B %d, %Y"))[0:10]

    @staticmethod
    def parse_dj_name(record):
        if ' with ' in record:
            return record.split('with ')[1].split('\r')[0]
        else:
            return None

    @staticmethod
    def parse_set_timeframe(record):
        return record.split('\t')[-1]

    @staticmethod
    def parse_set_name(record):
        return record.split(' with')[0]

    @staticmethod
    def parse_time_from_songplay_record(record):
        return (record.split('TIME: ')[1].split(' TITLE')[0] 
            if 'TIME:' in record else None)

    @staticmethod
    def parse_title_from_songplay_record(record):
        return record.split('TITLE: "')[1].split('\n')[0][0:-1]

    @staticmethod
    def parse_artist_from_songplay_record(record):
        return record.split('ARTIST: ')[1].split('\n')[0]

    @staticmethod
    def parse_album_from_songplay_record(record):
        return record.split('ALBUM: ')[1].split('\n')[0]


if __name__ == '__main__':
    today = str(date.today())
    playlist = WCDBDailyPlaylist(today)
    playlist.print()

