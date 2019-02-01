import psycopg2
import csv
from time import sleep
from time import strftime

conn = psycopg2.connect(host='192.168.42.100', user='hu', database='ptw', password='password')
cur = conn.cursor()

def insert_database():
    while True:
        tijd = strftime("%H:%M:%S")
        seconden = int(tijd[6:])
        print(seconden)
        sleep(1)
        if seconden == 30:
            with open('/home/pi/PTW/Feedbacklamp/metingen.csv', 'r') as csvFile:
                file  = csv.reader(csvFile, delimiter=',')
                for row in file:
                    datum = row[0]
                    tijd = row[1]
                    locatie = row[2]
                    decibel = row[3]
                    query = """INSERT INTO metingen VALUES (%s, %s, %s, %s)"""
                    values = (datum, tijd, decibel, locatie)
                    cur.execute(query, values)
                    conn.commit()
        else:
            pass
insert_database()
