from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from geoalchemy2.types import Geography
from sqlalchemy import func
from datetime import datetime, timedelta
import json
import os
import time
from psycopg2.errorcodes import NOT_NULL_VIOLATION
from psycopg2 import errors

db = SQLAlchemy()

basedir = os.path.abspath(os.path.dirname(__file__))

class VesselPosition(db.Model):
    __tablename__ = "vessel_positions"

    id = db.Column(db.Integer, primary_key=True)
    vessel_id = db.Column('vessel_id', db.Integer, nullable=False, index=True)
    latitude = db.Column('latitude', db.Numeric(precision=12, scale=9,asdecimal=True), nullable=False)
    longitude = db.Column('longitude',db.Numeric(precision=12, scale=9,asdecimal=True), nullable=False)
    geom = db.Column(Geography(geometry_type='POINT', srid=4326))
    received_time_utc = db.Column('received_time_utc', db.DateTime, nullable=False)

    # Indexes
    __table_args__ = (
        db.Index('vessel_positions_received_time_utc_vessel_id_idx', received_time_utc.desc(), vessel_id),
    )

    def __init__(self, vessel_id: int, latitude: str, longitude: str, received_time_utc: datetime):
        self.vessel_id = vessel_id
        self.latitude = latitude
        self.longitude = longitude
        self.geom = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)
        self.received_time_utc = received_time_utc

    @staticmethod
    def load_data(config):
        csv_file_path = os.path.join(basedir, 'data-fs-exercise.csv')
        with open(csv_file_path, 'r') as f:    
            conn = create_engine(config['DATABASE_URL_COPY']).raw_connection()
            cursor = conn.cursor()
            cmd = 'COPY vessel_positions(vessel_id, received_time_utc, latitude, longitude) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'
            try:
                cursor.copy_expert(cmd, f)
                cursor.execute("UPDATE vessel_positions SET geom = ST_SetSRID(ST_MakePoint(longitude::double precision, latitude::double precision), 4326)")
                conn.commit()
            except errors.lookup(NOT_NULL_VIOLATION) as e:
                print(e)
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def create(vessel_id, latitude, longitude, received_time_utc):  # Insert a new vessel's position
        new_position = VesselPosition(
            vessel_id,
            latitude,
            longitude,
            received_time_utc
        )
        db.session.add(new_position)
        db.session.commit()
        return new_position

    @staticmethod
    def get_vessels(dateFrom, dateTo):  # return list of vessel positions
        try:
            conn = create_engine('postgresql://postgres:kpler01#@kp-backend-postgres:5432/gis').raw_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT vessel_id, json_agg(json_build_array(longitude, latitude)) AS trip FROM vessel_positions
                WHERE received_time_utc::date >= %s and received_time_utc::date < %s
                GROUP BY vessel_id;
            """, ( dateFrom.date(), dateTo.date() ))
            rows = cursor.fetchall()
            positions = []
            for row in rows:
                positions.append({
                    'vessel_id': row[0],
                    'data': row[1]
                })

            cursor.close()
            return { "positions": positions }
        except Exception as error:
            print("Failed to read vessel trips: ", error)
        finally:
            if conn:
                conn.close()
