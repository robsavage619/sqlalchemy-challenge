# Importing dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# Creating engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflecting
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# Variables set-up
first_date = session.query(Measurement.date).order_by((Measurement.date)).limit(1).all()

last_date = session.query(Measurement.date).order_by((Measurement.date).desc()).limit(1).all()

session.close()
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
        f"Welcome to the Climate App! Please select a directory below:<br/>"
        f"<a href='/api/v1.0/precipitation'>Precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>Stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>TOBS</a><br/>"
        f"<a href='/api/v1.0/2016-8-24'>Start</a><br/>"
        f"<a href='/api/v1.0/2016-8-24/2017-8-23'>StartEnd</a><br/>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():

    print("Precipitation data processing...")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Creating variables
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    N = 365
    one_year = dt.date(2017,8,23) - dt.timedelta(days=N)

    start = dt.date(2017,8,23)

    # Query the results
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
                        filter(Measurement.date > one_year).\
                        order_by(Measurement.date).all()

    print(prcp_results)
    print("hi")
    # Close the session for housekeeping purposes
    session.close()

    # Creating list to store
    prcp_data_list = []

    # Appending data to a dictionary
    for data in prcp_results:
        prcp_data_dict = {}
        prcp_data_dict["Date"] = data.date
        prcp_data_dict["Precipitation"] = data.prcp
        prcp_data_list.append(prcp_data_dict)

    return jsonify(prcp_data_list)

@app.route("/api/v1.0/stations")
def stations():

    print("Stations data processing...")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the results
    station_results = session.query(Station.station).all()

    # Close the session for housekeeping purposes
    session.close()

    # Coverting List
    stations_list = list(np.ravel(station_results))

    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():

    print("TOBS data processing...")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the results
    USC00519281_results = session.query(Measurement.tobs, Measurement.date).\
        filter(Measurement.station == 'USC00519281').all()

    # Close the session for housekeeping purposes
    session.close()

    # Coverting List
    USC00519281_list = list(np.ravel(USC00519281_results))

    return jsonify(USC00519281_list)

@app.route("/api/v1.0/2016-8-24")
def tobs_date(start):

    print("TOBS date data processing...")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Setting up variables
    tobs_date = dt.datetime.strptime(start,'%Y-%m-%d').date()
    last_date_route = (dt.datetime.strptime(last_date[0][0],'%Y-%m-%d')).date()
    first_date_route = (dt.datetime.strptime(first_date[0][0],'%Y-%m-%d')).date()

    if start_date > last_date_route or start_date < first_date_route:
	       return(f"Select a date range between {first_date[0][0]} and {last_date[0][0]}")

    else:
     start_min_max_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
       func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
     tart_date_data = list(np.ravel(start_min_max_temp))
    return jsonify(start_date_data)

    # Close the session for housekeeping purposes
    session.close()

@app.route("/api/v1.0/2016-8-24/2017-8-23")
def tobs_date_range(start, end):

    print("TOBS range data processing...")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    tobs_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    tobs_date_range = dt.datetime.strptime(end, '%Y-%m-%d').date()
    last_date_route = (dt.datetime.strptime(last_date[0][0], '%Y-%m-%d')).date()
    first_date_route = (dt.datetime.strptime(first_date[0][0], '%Y-%m-%d')).date()

    if tobs_date > last_date_route or tobs_date < first_date_route or end_date > last_date_route or\
	 					end_date < first_date_route:
       return(f"Select a date range between {first_date[0][0]} and {last_date[0][0]}")

    else:
      start_end_min_max_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)).\
      filter(Measurement.date >= tobs_date).filter(Measurement.date <= end_date).all()
      start_end_data = list(np.ravel(start_end_min_max_temp))
    return jsonify(start_end_data)

    # Close the session for housekeeping purposes
    session.close()


if __name__ == '__main__':
    app.run(debug=True)
