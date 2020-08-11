# Import dependencies
import sys
from flask import Flask, render_template, redirect
# from flask_pymongo import PyMongo
from pymongo import MongoClient
from Missions_to_Mars import scrape_mars


sys.setrecursionlimit(2000)
app = Flask(__name__)

# app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)


conn = "mongodb://localhost:27017"
client = MongoClient(conn)

db = client.mars_app

# Drop collection if exists
db.mars_data.drop()


collection = db.mars_data


@app.route("/")
def index():
    data = collection.find()
    return render_template("index.html", data=data)


@app.route("/scrape")
def scrape():
    data = collection
    mars_data = scrape_mars.scrape_latest_details()
    # collection.insert_many(mars_data)
    data.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
