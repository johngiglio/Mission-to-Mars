from flask import Flask, jsonify, render_template
import pymongo


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_scrape_db



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    mars_info = list(db.mars.find())
    print(mars_info)
    return render_template("index.html", dict=mars_info)

@app.route("/scrape")
def scrapemars():
    import scrape_mars
    results = scrape_mars.scrape()
    print('Mars Scraped')
    db.mars.drop()
    print('Mars Dropped')
    db.mars.insert_one(results)
    print('Mars Inserted')
    return 'Hello Mars'



if __name__ == '__main__':
    app.run(debug=True)