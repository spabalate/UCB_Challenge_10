# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

#################################################
# Database Setup
#################################################

# reflect an existing database into a new model
engine = create_engine("sqlite:////Users/sam/Desktop/MY_UC_BERK/CHALLENGES/CHALLENGE_10/Resources/hawaii.sqlite")
base = automap_base()

# reflect the tables
base.prepare(engine, reflect=True)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

#Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

def get_session():
    engine = create_engine("sqlite:////Users/sam/Desktop/MY_UC_BERK/CHALLENGES/CHALLENGE_10/Resources/hawaii.sqlite")
    base = automap_base()
    base.prepare(engine, reflect=True)
    session = Session(engine)
    return session

#################################################
# Flask Routes
#################################################

# Define the root route
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

# Define a route to retrieve precipitation data for the last 12 months
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = get_session()
    
    # Calculate the date one year ago from the last date in the database
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query precipitation data for the last 12 months
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}
    
    # Close the session to release the connection
    session.close()

    return jsonify(precipitation_data)

# Define a route to retrieve a list of stations
@app.route("/api/v1.0/stations")
def stations():
    session = get_session()
    
    # Query and return a list of stations
    results = session.query(station.station).all()
    station_list = [station[0] for station in results]
    
    # Close the session to release the connection
    session.close()

    return jsonify(station_list)

# Define a route to retrieve temperature observations for the last year for the most-active station
@app.route("/api/v1.0/tobs")
def tobs():
    session = get_session()
    
    # Calculate the date one year ago from the last date in the database
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query temperature observations for the last year for the most-active station
    results = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= one_year_ago).all()

    # Convert the query results to a list of dictionaries
    temperature_data = [{"date": date, "tobs": tobs} for date, tobs in results]
    
    # Close the session to release the connection
    session.close()

    return jsonify(temperature_data)

# Define a route to retrieve temperature statistics for a specified start date or start-end range
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start, end=None):
    session = get_session()

    # Convert start and end dates to datetime objects
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    
    if end:
        end_date = dt.datetime.strptime(end, "%Y-%m-%d")
        results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    else:
        results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start_date).all()

    # Convert the query results to a list of dictionaries
    temperature_stats = [{"min": result[0], "avg": result[1], "max": result[2]} if result[0] is not None else {"min": None, "avg": None, "max": None} for result in results]

    
    # Close the session to release the connection
    session.close()

    return jsonify(temperature_stats)

# Run the app if the script is executed
if __name__ == "__main__":
    app.run(debug=True)