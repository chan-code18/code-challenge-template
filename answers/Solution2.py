import mysql.connector as mysql
import os
import time
import re


def station_id_in_db(station_id, cursor):
    # Function to avoid duplicate entry
    q = 'SELECT COUNT(station_id) FROM weather_station WHERE station_id = {};'.format(station_id)
    cursor.execute(q)
    results = cursor.fetchall()
    return results[0][0] > 0


def date_id_in_db(station_id, date, cursor):
    # Function to avoid duplicate entry
    q = 'SELECT COUNT(date) FROM weather_data WHERE date = {} and station_id= {};'.format(date, station_id)
    cursor.execute(q)
    results = cursor.fetchall()
    return results[0][0] > 0


mydb = mysql.connect(
    host="localhost",
    user="root",
    password="srinath",
    database="weather_challenge"
)

# initialize the connection
cursor = mydb.cursor()
num_records = 0
start_time = time.time()
#Loop through the files in the directory
for filename in os.listdir('wx_data'):
    station_id = filename.split('.')[0]
    print(station_id)
    station_id = int(re.findall(r'\d+',station_id)[0])
    with open(f'wx_data/{filename}', 'r') as file:
        station_id_present = station_id_in_db(station_id, cursor)
        if not station_id_present:
            # if the station id is not already present in the weather_station table, insert
            cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
            cursor.execute(
                'INSERT INTO weather_station (station_id, name, location) '
                'VALUES (%s, %s, %s)',
                (station_id, filename, "")
            )
            mydb.commit()
            for line in file:
                data = line.strip().split('\t')
                date = data[0]
                max_temp = float(data[1]) / 10
                min_temp = float(data[2]) / 10
                precipitation = float(data[3]) / 10
                date_id_present = date_id_in_db(station_id,date, cursor)
                num_records = num_records + 1
                if not date_id_present:
                    # if the date and station id is not already present in the weather_data table, insert
                    cursor.execute(
                        'INSERT INTO weather_data (station_id, date, max_temp, min_temp, precipitation) '
                        'VALUES (%s, %s, %s, %s, %s)',
                        (station_id, date, max_temp, min_temp, precipitation)
                    )
                else:
                    print("Record already exists. {} {}".format(station_id,date))
        else:
            print("Record already exists. {}".format(station_id))
end_time = time.time()
mydb.commit()
print("Total time taken {}mins".format(round((end_time-start_time)/60), 2))
print("#Number of records: {}".format(num_records))


