from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import bs4
import requests as rq

app = Flask(__name__)
api = Api(app)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
       "origins": "*"
    }
})
def scrap():
    link = "https://www.worldometers.info/coronavirus/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }

    data = rq.get(link, headers=headers)

    soup = bs4.BeautifulSoup(data.content, "html.parser")

    table = soup.find("table")

    d = {}
    for row in table.find_all("tr"):
        r = []
        for data in row.find_all("td"):
            r.append(data.text.strip())
        # print(r)
        try:
            d[r[0]] = {'total': r[1], 'deaths': r[3], 'cured': r[5], 'active': r[6]}
        except:
            continue

    return d

class UserAPI(Resource):
    def get(self):
        d = scrap()
        return jsonify(d)

api.add_resource(UserAPI, '/')

if __name__ == '__main__':
    app.run()
