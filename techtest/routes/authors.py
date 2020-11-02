import json

from flask import abort, jsonify, request

from techtest.baseapp import app
from techtest.connector import db_session_wrap
from techtest.models.author import Author
from techtest.routes.common import *

# Helper functions

def do_add_author(session, first_name, last_name):
    
    if check_author(session, first_name, last_name):
        return TECH_MSG_AUTHOR_EXISTS, HTTP_OK
    else:
        session.add_all([ Author( first_name=first_name, last_name=last_name, ) ] )
        return TECH_MSG_AUTHOR_ADDED, HTTP_OK

def do_edit_author(session, id, first_name, last_name):
    
    if check_author_by_id(session, id):
        session.query( Author ).filter( Author.id == id ).update ( { Author.first_name: first_name, Author.last_name: last_name } )
        return TECH_MSG_AUTHOR_UPDATED, HTTP_OK
    else:
        return TECH_MSG_NX_AUTHOR, HTTP_OK

def check_author(session, first_name, last_name):
    
    query = session.query( Author ).filter( Author.first_name == first_name ).filter( Author.last_name == last_name )
    result = query.all()
    if len(result) == 0:
        return False
    else:
        return True

def check_author_by_id(session, id):
    
    query = session.query ( Author ).filter ( Author.id == id )
    result = query.all()
    if len(result) == 0:
        return False
    else:
        return True    

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
