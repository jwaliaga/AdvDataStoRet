import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/precipitation<br/>"
        f"/api/station<br/>"
        f"/api/temperature<br/>"
        f"/api/<start><br/>"
        f"/api/<start>/<end>"
    )

# /api/precipitation
# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/precipitation")
def precipitation():
    # Query all the results
        
    results = session.query(Measurement.date,Measurement.prcp)
    
    # Create a dictionary form the row data and append to a list
    all_data = []
    for date,prcp in results:
        data_dict = {}
        data_dict["date"] = date
        data_dict["prcp"] = prcp
        all_data.append(data_dict)

    return jsonify(all_data)

# /api/temperature
# query for the dates and temperature observations from a year from the last data point.
@app.route("/api/temperature")
def temperature():

    query_date = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date >= query_date).all()

    all_data = []
    for date,tobs in results:
        data_dict = {}
        data_dict["date"] = date
        data_dict["tobs"] = tobs
        all_data.append(data_dict)

    return jsonify(all_data)

# /api/station
# Return a JSON list of stations from the dataset.
@app.route("/api/station")
def station():
    # Query all the results
    results = session.query(Station.station,Station.name).all()

    # Create a dictionary form the row data and append to a list
    all_data = []
    for station,name in results:
        data_dict = {}
        data_dict["station"] = station
        data_dict["name"] = name
        all_data.append(data_dict)

    return jsonify(all_data)

# /api/<start>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# Hint: You may want to look into how to create a defualt value for your route variable.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/<start>")
def api_start(start):    

    #sel = [Station.name,
    #  func.min(Measurement.tobs),
    #  func.max(Measurement.tobs),
    #  func.avg(Measurement.tobs)]

    #results = session.query(*sel).\
    #    filter(Measurement.date>=start).\
    #    filter(Measurement.station==Station.station).\
    #    group_by(Measurement.station).\
    #    order_by(Measurement.date).all()

    sel = [func.min(Measurement.tobs),
      func.max(Measurement.tobs),
      func.avg(Measurement.tobs)]

    results = session.query(*sel).\
        filter(Measurement.date>=start).\
        order_by(Measurement.date).all()

    all_results = list(np.ravel(results))

    return jsonify(all_results)

# /api/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# Hint: You may want to look into how to create a defualt value for your route variable.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/<start>/<end>")
def api_start_end(start,end):

#    sel = [Measurement.station,
#      func.min(Measurement.tobs),
#      func.max(Measurement.tobs),
#      func.avg(Measurement.tobs)]

#    results = session.query(*sel).\
#        filter(Measurement.date>=start).\
#        filter(Measurement.date<=end).\
#        group_by(Measurement.station).\
#        order_by(Measurement.date).all()

    sel = [func.min(Measurement.tobs),
      func.max(Measurement.tobs),
      func.avg(Measurement.tobs)]

    results = session.query(*sel).\
        filter(Measurement.date>=start).\
        filter(Measurement.date<=end).all()

    all_results = list(np.ravel(results))

    return jsonify(all_results)

if __name__ == '__main__':
    app.run(debug=True)