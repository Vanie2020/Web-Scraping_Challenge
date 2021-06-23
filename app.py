# import necessary libraries
from flask import Flask, render_template,redirect
from flask_pymongo import PyMongo
import Mission_Scrape

# create instance of Flask app
app = Flask(__name__)
app.config["MONGO_URI"]="mongodb+srv://BiSeye:Ivorycoast1984@cluster0.wb2i1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongo=PyMongo(app)
mars_collection=mongo.db.mission_to_mars



# create route that renders index.html template
@app.route("/")
def index():
    mars = mars_collection.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    scraped_data = Mission_Scrape.scrape()
    mars_collection.update({}, scraped_data, upsert=True)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)


