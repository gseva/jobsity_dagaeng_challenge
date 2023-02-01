
import os
import psycopg2
import logging

from flask import Flask, request

import queries
from notifications import send_email


app = Flask('trips_api')


def get_database_connection():
    return psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'),
        dbname=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
    )


@app.route('/trips', methods=['POST'])
def upload_trips():
    if request.method == 'POST':
        if 'file' not in request.files:
            return {'error': 'you must upload a file'}, 400
        conn = get_database_connection()
        with conn:
            with conn.cursor() as curs:
                curs.execute(queries.TEMPORARY_TABLE_STATEMENT)

                f = request.files['file']
                # I'm using explicit copy statement to ignore header
                curs.copy_expert(queries.COPY_STATEMENT, f)
                curs.execute(queries.INSERT_STATEMENT)
                rows = curs.fetchone()[0]

    if os.environ.get('ENABLE_EMAIL_NOTIFICATION'):
        try:
            send_email(rows)
        except Exception as e:  # TODO: catch this exception more strictly
            logging.error('Error sending email: ' + str(e))

    return {'message': f'file uploaded successfully, inserted {rows} rows'}, 200


@app.route('/trips/weekly_average')
def get_weekly_trips():
    bounding_box_params = ['xmin', 'ymin', 'xmax', 'ymax']
    if all(arg in request.args for arg in bounding_box_params):
        query = queries.WEEKLY_AVG_BY_BOUNDING_BOX_QUERY
        parameters = tuple(request.args[arg] for arg in bounding_box_params)
    elif 'region' in request.args:
        query = queries.WEEKLY_AVG_BY_REGION_QUERY
        parameters = (request.args['region'],)
    else:
        error_msg = ('please specify either "region" or a bounding box using '
                     '"xmin", "ymin", "xmax", "ymax" url parameters')
        return {'error': error_msg}, 400

    conn = get_database_connection()
    with conn:
        with conn.cursor() as curs:
            curs.execute(query, parameters)
            result = curs.fetchone()[0]
    return {'weekly_average': result}, 200


if __name__ == '__main__':
    app.run()
