class Song:
	def __init__(self, title, artist, album):
		self.title = title
		self.artist = artist
		self.album = album

class SongPlay:
	def __init__(self, datetime_played, song: Song):
		self.datetime_played = datetime_played,
		self.song = song
