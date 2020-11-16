import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
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
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/'startdate'<br/>"
        f"startdate format = YYYY-MM-DD and the date range from 2010-01-01 to 2017-08-23<br/>"
        f"/api/v1.0/'startdate'/'enddate'<br/>"
        f"startdate and enddate format = YYYY-MM-DD and the date range from 2010-01-01 to 2017-08-23"
    )

#################################################
# precipitation
#################################################

@app.route('/api/v1.0/precipitation')
def precipitation():

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    pre = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).order_by(measurement.date).all()

    # Create a list of dicts with `date` and `prcp'
    prelist = []
    for result in pre:
        row = {}
        row["date"] = pre[0]
        row["prcp"] = pre[1]
        prelist.append(row)
 
    return jsonify(pre)

#################################################
# stations
#################################################

@app.route('/api/v1.0/stations')
def stations():

    stations = session.query(station.station).all()

    return jsonify(stations)

################################################
# Tobs
#################################################

@app.route('/api/v1.0/tobs') 
def tobs():  
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    last_year = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= year_ago).order_by(measurement.tobs).all()
    
    return jsonify(last_year)

#################################################
# Start
##################################################

@app.route('/api/v1.0/<start>') 
def start(start=None):

    start = dt.date(2010,1,1)
    end = dt.date(2017,8,23)
    tobs = session.query(measurement.tobs).filter(measurement.date.between(start,end)).all()
    
    df = pd.DataFrame(tobs)

    tavg = df["tobs"].mean()
    tmax = df["tobs"].max()
    tmin = df["tobs"].min()
    
    return jsonify(tavg, tmax, tmin)

#################################################
# Start & End
##################################################

@app.route('/api/v1.0/<start>/<end>') 
def startend(start=None, end=None):

    start = dt.date(2010,1,1)
    end = dt.date(2017,8,23)
    tobs = session.query(measurement.tobs).filter(measurement.date.between(start, end)).all()
    
    df = pd.DataFrame(tobs)

    tavg = df["tobs"].mean()
    tmax = df["tobs"].max()
    tmin = df["tobs"].min()
    
    return jsonify(tavg, tmax, tmin)

if __name__ == "__main__":
    app.run(debug=True)