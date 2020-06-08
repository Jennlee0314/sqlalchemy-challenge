import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    #  Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    #dictionaty comprehension, it gives dict that return below
    PRCP = {date:prcp for date, prcp in results}

    # Convert list of tuples into normal list
    return jsonify(PRCP)


@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Return a JSON list of stations from the dataset.
    results = session.query(Station.station).all()

    session.close()
    result = list(np.ravel(results))

    return jsonify(result)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query the dates and temperature observations of the most active station for the last year of data.
    #Return a JSON list of temperature observations (TOBS) for the previous year.
    previous_date = dt.date(2017,8,23)-dt.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.date >= previous_date).\
        filter(Measurement.station=='USC00519281').all()

    session.close()
    result = list(np.ravel(results))

    return jsonify(result)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature
#for a given start or start-end range.
def stats(start=None, end=None):
    # Create our session (link) from Python to the DB
    


    #start_date = dt.date("2010.01.01")-dt.timedelta(days=365)
    if not end:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    else:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(<=end).all()

    session.close()
    result = list(np.ravel(results))

    return jsonify(result)




#Return a JSON list of the minimum temperature, the average temperature, and the max temperature
#for a given start or start-end range.
def end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

   
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()


    session.close()
    result = list(np.ravel(results))

    return jsonify(result)
if __name__ == '__main__':
    app.run(debug=True)

