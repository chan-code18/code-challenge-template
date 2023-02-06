from flask import Flask, jsonify, request
import mysql.connector as mysql
# from flask_restplus import Api
# from werkzeug.utils import cached_property
# from flask_restplus import apidoc



app = Flask(__name__)
# api = Api(app, doc='/docs') # werkzeug import issues
# app.register_blueprint(apidoc.apidoc)

@app.route("/api/weather", methods=["GET"])
def get_all_weather_data():
    # fetch weather data based on query parameters (date, station ID)
    date = request.args.get("date")
    station_id = request.args.get("station_id")
    # retrieve data from database based on query parameters
    weather_data = retrieve_data_from_database(date, station_id)
    # paginate the data if needed
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    weather_data = weather_data[(page - 1) * per_page: page * per_page]
    # return the data as a JSON response
    return jsonify(weather_data)

@app.route("/api/weather/stats", methods=["GET"])
def get_weather_data_stats():
    # fetch statistics based on query parameters (date, station ID)
    station_id = request.args.get("station_id")
    # retrieve statistics from database based on query parameters
    stats = retrieve_stats_from_database(station_id)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    stats = stats[(page - 1) * per_page: page * per_page]
    # return the data as a JSON response
    return jsonify(stats)

def retrieve_data_from_database(date, station_id):
  # Function to retrieve data from database
    mydb = mysql.connect(
        host="localhost",
        user="root",
        password="srinath",
        database="weather_challenge"
    )

    cursor = mydb.cursor()
    q = 'SELECT * FROM weather_challenge.weather_data WHERE station_id = {} and date = {};'.format(station_id, date)
    cursor.execute(q)
    results = cursor.fetchall()
    return results[0][0]


def retrieve_stats_from_database(station_id):
    # Function to retrieve stats from database
    mydb = mysql.connect(
        host="localhost",
        user="root",
        password="srinath",
        database="weather_challenge"
    )

    cursor = mydb.cursor()
    q = 'SELECT * FROM weather_challenge.weather_stats WHERE station_id = {}'.format(station_id)
    cursor.execute(q)
    results = cursor.fetchall()
    return results


if __name__ == "__main__":
    app.run(debug=True)
