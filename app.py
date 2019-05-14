# Import dependencies 
from flask import Flask, render_template, redirect 
import pymongo
import scrape_mars

app = Flask(__name__)
conn = 'mongodb://localhost:27017/mission_mars'
mongo = pymongo.MongoClient(conn)

# Home route
@app.route("/")
def home(): 

    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Scrape function route
@app.route("/scrape")
def scrape(): 

    # functions related to different elements
    mars = mongo.db.mars
    marsD = scrape_mars.marsNews()
    marsD = scrape_mars.marsImage()
    marsD = scrape_mars.marsWeather()
    marsD = scrape_mars.marsFacts()
    marsD = scrape_mars.marsHemispheres()
    mars.update({}, marsD, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug=True)