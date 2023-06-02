import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd

from flask import Flask, jsonify, render_template


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///data/titanic.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Passenger = Base.classes.passenger

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def main_page():
    """
    Render the main page of the webapp.
    Currently, the only api route accessed by the web page is 'passengersbyclass'.
    """
    return render_template('index.html')


@app.route("/api/v1.0/passengersbyclass")
def passengers_by_class():
    """
    Return a dictionary of summary data. Data are structured as follows:
    Data[Survived_or_Died][Class_1_2_or_3] = count_of_passengers_matching_this_description
    """
    
    session = Session(engine)
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, 
                            Passenger.sex, Passenger.pclass,
                            Passenger.survived).all()

    session.close()

    df = pd.DataFrame(results)
    results = {}
    results["Survived"] = df[df['survived']==1].groupby(['pclass'])['name'].count().to_dict()
    results["Died"] = df[df['survived']==0].groupby(['pclass'])['name'].count().to_dict()
    return jsonify(results)


# The following routes are not currently used by the application, 
# but can still be accessed when the flask app is running

@app.route("/api/v1.0/names")
def names():
    """Return a list of all passenger names"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all passengers
    results = session.query(Passenger.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/passengers")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, 
                            Passenger.sex, Passenger.pclass,
                            Passenger.survived).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex, pclass, survived in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        passenger_dict["class"] = pclass
        passenger_dict["survived"] = survived
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)

@app.route("/api/v1.0/passengerbyname/<name>")
def passenger_by_name(name):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).filter(Passenger.name == name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=False)
