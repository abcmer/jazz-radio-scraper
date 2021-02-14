from src.daily_playlist import WCDBDailyPlaylist

def test_date_parser():
	date_str = WCDBDailyPlaylist.parse_date_string('Tuesday - February 09, 2021')
	assert date_str == '2021-02-09'	