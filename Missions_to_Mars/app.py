from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_info")


# Do I need to define the collection? 
# db = client.nammeOfCollection

# If all of the data is stored into one collection... 
# then I can use this one route to fill in the index.html
# # or do I need a route for each section?
# @app.route("/")
# def index():

#     title = mongo.db.titles.find_one()
#     paragraph = mongo.db.paragraph.find_one()
#     featured_image_url = mongo.db.featured_image_url()
#     hemisphere_image_urls = mongo.db.hemisphere_image_urls()

#     listings = mongo.db.listings.find_one()
#     return render_template("index.html", listings=listings)


@app.route("/scrape")
def scraper():

    hemisphere_image_urls = scrape_mars.scrape_info()
    mongo.db.collection.update({}, hemisphere_image_urls, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)