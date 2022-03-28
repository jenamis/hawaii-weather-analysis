# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Set up database engine for Flask application
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect database
Base = automap_base()

# Reflect tables
Base.prepare(engine, reflect = True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link from Python to DB
session = Session(engine)

# Define Flask app
app = Flask(__name__)

# Define welcome route
@app.route("/")

# Create function to add routing information for additional routes
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<br/>
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/temp/start/end
    ''')

if __name__ == '__main__':
   app.run()

# Create precipitation route
@app.route("/api/v1.0/precipitation")

# Create precipitation function
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
     filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Create stations route
@app.route("/api/v1.0/stations")

# Create stations function
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations = stations)

# Create temperature observations route
@app.route("/api/v1.0/tobs")

# Create temperature observations function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    results = session.query(Measurement.tobs).\
     filter(Measurement.station == "USC00519281").\
     filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps = temps)

# Create statistics route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Create statistics function
def stats(start = None, end = None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
         filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    results = session.query(*sel).\
     filter(Measurement.date >= start).\
     filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)