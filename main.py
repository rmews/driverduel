import http.server
import requests
import os
import threading
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Driver, Track, RaceResult

app = Flask(__name__)

engine = create_engine('sqlite:///nascarstats.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def frontPage():
    return render_template('main.html')

@app.route('/tracks/')
def showTracks():
    tracks = session.query(Track).all()
    # pass all track data to template
    return render_template('tracks.html', tracks=tracks)

@app.route('/drivers/')
def showDrivers():
    drivers = session.query(Driver).all()
    # pass all driver data to template
    return render_template('drivers.html', drivers=drivers)

@app.route('/tracks/<track_name>/')
def showTrack(track_name):
    track = session.query(Track).filter_by(name=track_name).one()
    results = (
        session.query(
                    Driver.name,
                    func.avg(RaceResult.start).label("avg_start"),
                    func.avg(RaceResult.finish).label("avg_finish"),
                    func.avg(RaceResult.laps_led).label("avg_laps_led"),
                    func.avg(RaceResult.fastest_laps).label("avg_fastest_laps"),
                    func.avg(RaceResult.points_finish).label("avg_points_finish"),
                    func.avg(RaceResult.points_differential).label("avg_points_differential"),
                    func.avg(RaceResult.points_led).label("avg_points_led"),
                    func.avg(RaceResult.points_fastest).label("avg_points_fastest"),
                    func.avg(RaceResult.points_total).label("avg_points_total"))
                .group_by(RaceResult.driver_id)
                .filter(Driver.id == RaceResult.driver_id)
                .filter(RaceResult.track == track)
                .order_by(desc("avg_points_total"))
    )
    return render_template('track.html', track=track, results=results)

@app.route('/drivers/<driver_name>/')
def showDriver(driver_name):
    driver = session.query(Driver).filter_by(name=driver_name).one()
    results = (
        session.query(
                    Track.name,
                    Track.track_type,
                    func.avg(RaceResult.start).label("avg_start"),
                    func.avg(RaceResult.finish).label("avg_finish"),
                    func.avg(RaceResult.laps_led).label("avg_laps_led"),
                    func.avg(RaceResult.fastest_laps).label("avg_fastest_laps"),
                    func.avg(RaceResult.points_finish).label("avg_points_finish"),
                    func.avg(RaceResult.points_differential).label("avg_points_differential"),
                    func.avg(RaceResult.points_led).label("avg_points_led"),
                    func.avg(RaceResult.points_fastest).label("avg_points_fastest"),
                    func.avg(RaceResult.points_total).label("avg_points_total"))
                .group_by(RaceResult.track_id)
                .filter(Track.id == RaceResult.track_id)
                .filter(RaceResult.driver == driver)
                .order_by(desc("avg_points_total"))
    )
    return render_template('driver.html', driver=driver, results=results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))    # Use PORT if it's there.
    server_address = ('', port)

# if __name__ == '__main__':
#     app.run(debug=True, use_reloader=True)
#     app.debug = True
#     app.run(host='0.0.0.0', port=5000)