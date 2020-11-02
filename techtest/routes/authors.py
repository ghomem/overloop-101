import json

from flask import abort, jsonify, request

from techtest.baseapp import app
from techtest.connector import db_session_wrap
from techtest.models.author import Author
from techtest.routes.common import *

@app.route('/authors', methods=['GET'])
@db_session_wrap
def get_authors(session):
    query = session.query(
        Author
    ).order_by(
        Author.first_name
    )
    return jsonify([author.asdict() for author in query.all()])

# usage note:
# curl -X POST  http://localhost:5000/add_author --form username=USERNAME --form password=PASSWORD --form 'content={"first_name":"Al","last_name":"Packa"}'

@app.route('/add_author', methods=['POST'])
@db_session_wrap
def add_author(session):
    
    try:
        password = request.form['password']
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
            return add_author (session, first_name, last_name)
        else:
            return TECH_ERR , HTTP_FORB
    else:
        return TECH_ERR, HTTP_FORB
    
def add_author(session, first_name, last_name):
    
    if check_author(session, first_name, last_name):
        return TECH_MSG_AUTHOR_EXISTS, HTTP_OK
    else:
        session.add_all([ Author( first_name=first_name, last_name=last_name, ) ] )
        return TECH_MSG_AUTHOR_ADDED, HTTP_OK

def check_author(session, first_name, last_name):
    
    query = session.query( Author ).filter( Author.first_name == first_name ).filter( Author.last_name == last_name )
    result = query.all()
    if len(result) == 0:
        return False
    else:
        return True
    
