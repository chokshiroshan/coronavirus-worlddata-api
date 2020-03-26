from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import bs4
import requests as rq

app = Flask(__name__)
api = Api(app)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


def scrap():
    link = "https://www.worldometers.info/coronavirus/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }

    data = rq.get(link, headers=headers)

    soup = bs4.BeautifulSoup(data.content, "html.parser")

    table = soup.find("table")

    c_names = []
    d = {}
    for row in table.find_all("tr"):
        r = []
        for data in row.find_all("td"):
            r.append(data.text.strip())
        try:
            d[r[0].replace("Total:", "Total").lower()] = {
                "total": r[1],
                "deaths": r[3],
                "cured": r[5],
                "active": r[6],
            }
        except:
            continue
        c_names.append(r[0].replace("Total:", "Total").lower())
    return d, c_names


def country(cn, d, c_names):
    if cn in c_names:
        return d[cn]
    else:
        return "ErroR"


class UserAPI(Resource):
    def get(self, cn=None):
        d, c_names = scrap()
        if cn is None:
            return jsonify(d)
        else:
            cn = str(cn)
            return jsonify(country(cn, d, c_names))


api.add_resource(UserAPI, "/all", endpoint="")
api.add_resource(UserAPI, "/<cn>", endpoint="country")

if __name__ == "__main__":
    app.run()
