# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///hawaii.sqlite")
base = automap_base()

# reflect the tables
base.prepare(engine, reflect=True)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

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
    # Calculate the date one year ago from the last date in the database
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query precipitation data for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)

# Define a route to retrieve a list of stations
@app.route("/api/v1.0/stations")
def stations():
    # Query and return a list of stations
    results = session.query(Station.station).all()
    station_list = [station[0] for station in results]

    return jsonify(station_list)

# Define a route to retrieve temperature observations for the last year for the most-active station
@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date one year ago from the last date in the database
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query temperature observations for the last year for the most-active station
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a list of dictionaries
    temperature_data = [{"date": date, "tobs": tobs} for date, tobs in results]

    return jsonify(temperature_data)

# Define a route to retrieve temperature statistics for a specified start date or start-end range
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start, end=None):
    # Query temperature statistics based on the specified start and end date (if provided)
    if end:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()

    # Convert the query results to a list of dictionaries
    temperature_stats = [{"min": result[0], "avg": result[1], "max": result[2]} for result in results]

    return jsonify(temperature_stats)

# Run the app if the script is executed
if __name__ == "__main__":
    app.run(debug=True)



#################################################
# Flask Routes
#################################################