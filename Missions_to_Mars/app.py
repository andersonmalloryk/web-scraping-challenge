from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_info")

@app.route("/")
def index():

    features = mongo.db.features.find_one()
    return render_template("index.html", features = features)


@app.route("/scrape")
def scraper():

    features = mongo.db.features
    scrape_content = scrape_mars.scrape_info()
    features.update({}, scrape_content, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)