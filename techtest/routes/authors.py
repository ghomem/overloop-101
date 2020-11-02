from flask import abort, jsonify, request

from techtest.baseapp import app
from techtest.connector import db_session_wrap
from techtest.models.region import Region


@app.route('/authors', methods=['GET'])
@db_session_wrap
def get_authors(session):
    query = session.query(
        Author
    ).order_by(
        Author.first_name
    )
    return jsonify([author.asdict() for author in query.all()])
