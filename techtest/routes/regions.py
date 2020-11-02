from flask import abort, jsonify, request

from techtest.baseapp import app
from techtest.connector import db_session_wrap
from techtest.models.region import Region
from techtest.routes.common import *

@app.route('/regions', methods=['GET'])
@db_session_wrap
def get_regions(session):
    query = session.query(
        Region
    ).order_by(
        Region.id
    )
    return jsonify([region.asdict() for region in query.all()])

@app.route('/region/<id>', methods=['GET'])
@db_session_wrap
def get_region(session,id):

    return get_region_by_id(session,id)
