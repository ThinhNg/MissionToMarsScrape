from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_Data")
mongo.db.collection.drop()

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    MartianData = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", Martian=MartianData)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    MartianData = mission_to_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, MartianData, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
