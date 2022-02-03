from flask import Flask
from flask_restful import Resource, Api

from jazz_radio_scraper.scraper import WCDBDailyPlaylist

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        playlist = WCDBDailyPlaylist("2021-01-20")
        print(len(playlist.data))
        return playlist.data

api.add_resource(HelloWorld, '/today')

if __name__ == '__main__':
    app.run(debug=True)