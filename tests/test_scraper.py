from src.scraper import WDCBWebScraper

def test_date_parser():
	date_str_long = 'Tuesday - February 09, 2021'
	date_str = WDCBWebScraper.parse_date_string(date_str_long)	
	assert str(date_str) == '2021-02-09 00:00:00'