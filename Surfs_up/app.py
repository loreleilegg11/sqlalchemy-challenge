# Import the dependencies.
from unittest import result
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

## Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


## Create our session (link) from Python to the DB
session = Session(engine)


#home 
@app.route("/")
def home():
    return(
        f"<center><h2>Hawaii Climate API"
        f"<center><h3> Select from Available route: <h3></center>"
        f"<center>/api/v1.0/precipitation</center>"
        f"<center>/api/v1.0/stations</center>"
        f"<center>/api/v1.0/tobs</center>"
        f"<center>/api/v1.0/start/end</center>"
    )
#################################################
# Flask Routes
#################################################

## /api/v1.0/precipitation
@app.route('/api/v1.0/precipitation')
def precip():
   # Calculate the date one year from the last date in data set.
    previousYR =dt.date(2017,8,23) -dt.timedelta(days =365)
    #previousYR
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previousYR).all()

    session.close()
# dict with date as key and prcp as value
    precipitation = {date: prcp for date, prcp in results}

# convert to json 
    return jsonify(precipitation)
#'/api/v1.0/stations'
@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station).all()
    session.close()
# station list
    stationlist = list(np.ravel(results))
 ## convert to json 
    return jsonify(stationlist)

# '/api/v1.0/tobs' route
@app.route('/api/v1.0/tobs')
def Temperatures():
    previousYR =dt.date(2017,8,23) -dt.timedelta(days =365)

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= previousYR).all()
    session.close()

 # temp list
    templist = list(np.ravel(results))
# jsonify 
    return jsonify(templist)

# /api/v1.0/start/end route
@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def startendstats(start=None, end=None):
    
    Selection = [func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)]

    if not end:
        
        startdate= dt.datetime.strptime(start,"%m%d%Y")

        results = session.query(*Selection).filter(Measurement.date >= startdate).all()

        session.close()

        templist = list(np.ravel(results))

        return jsonify(templist)
 
    else:
        startdate= dt.datetime.strptime(start,"%m%d%Y")
        enddate= dt.datetime.strptime(end,"%m%d%Y")
       
        results = session.query(*Selection)\
            .filter(Measurement.date >= startdate)\
            .filter(Measurement.date <= enddate).all()

        session.close()

        templist = list(np.ravel(results))

        return jsonify(templist)


## lauch app
if __name__ == '__main__':
    app.run(debug=True)

