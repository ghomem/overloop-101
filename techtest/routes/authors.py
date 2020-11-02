import json

from flask import abort, jsonify, request

from techtest.baseapp import app
from techtest.connector import db_session_wrap
from techtest.models.author import Author
from techtest.routes.common import *

# Flask routes

@app.route('/authors', methods=['GET'])
@db_session_wrap
def get_authors(session):
    query = session.query(
        Author
    ).order_by(
        Author.id
    )
    return jsonify([author.asdict() for author in query.all()])

@app.route('/author/<id>', methods=['GET'])
@db_session_wrap
def get_author(session,id):

    return get_author_by_id(session,id)


# usage note:
# curl -X POST  http://localhost:5000/add_author --form username=USERNAME --form password=PASSWORD --form 'content={"first_name":"Al","last_name":"Packa"}'

@app.route('/add_author', methods=['POST'])
@db_session_wrap
def add_author(session):

    try:
        password  = request.form['password']
        username  = request.form['username']
        content   = request.form['content']
    except:
        return TECH_ERR_FORM_INPORT, HTTP_ERR
    
    try:
        jcontent = json.loads(content)
    except:
        return TECH_ERR_JSON_IMPORT, HTTP_ERR
    
    try:
        first_name = jcontent['first_name']
        last_name  = jcontent['last_name']
    except:
        return TECH_ERR_CONTENT_IMPORT, HTTP_ERR
        
    if ( checkstr_usr( username ) and checkstr_pwd( password ) ):
        if do_pam_auth ( username, password ):
            return do_add_author (session, first_name, last_name)
        else:
            return TECH_ERR_AUTHENTICATION , HTTP_FORB
    else:
        return TECH_ERR, HTTP_FORB

# usage note:
# curl -X POST  http://localhost:5000/add_author --form username=USERNAME --form password=PASSWORD --form 'content={ "id:9898989", "first_name":"Al","last_name":"Packa"}' 

@app.route('/edit_author', methods=['POST'])
@db_session_wrap
def edit_author(session):  
    
    try:
        password  = request.form['password']
        username  = request.form['username']
        content   = request.form['content']
    except:
        return TECH_ERR_FORM_INPORT, HTTP_ERR
    
    try:
        jcontent = json.loads(content)
    except:
        return TECH_ERR_JSON_IMPORT, HTTP_ERR
    
    try:
        id         = jcontent['id']
        first_name = jcontent['first_name']
        last_name  = jcontent['last_name']
    except:
        return TECH_ERR_CONTENT_IMPORT, HTTP_ERR
    
    if ( checkstr_usr( username ) and checkstr_pwd( password ) ):
        if do_pam_auth ( username, password ):
            return do_edit_author (session, id, first_name, last_name)
        else:
            return TECH_ERR_AUTHENTICATION , HTTP_FORB
    else:
        return TECH_ERR, HTTP_FORB
