from flask import abort, jsonify, request

from techtest.baseapp import app
from techtest.connector import db_session_wrap
from techtest.models.region import Region


@app.route('/regions', methods=['GET'])
@db_session_wrap
def get_regions(session):
    query = session.query(
        Region
    ).order_by(
        Region.id
    )
    return jsonify([region.asdict() for region in query.all()])
