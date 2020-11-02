import json

from flask import abort, jsonify, request

from techtest.baseapp import app
from techtest.connector import db_session_wrap
from techtest.models.article import Article
from techtest.models.region import Region
from techtest.routes.common import *

@app.route('/articles', methods=['GET'])
@db_session_wrap
def get_articles(session):
    query = session.query(
        Article
    ).order_by(
        Article.id
    )
    return jsonify([
        article.asdict(follow=['regions', 'authors']) for article in query.all()
    ])

# usage note:
# curl -X POST  http://localhost:5000/add_article --form username=USERNAME --form password=PASSWORD --form 'content={"title":"R0 versus 2020","content":"exponentially spreading literature lala"}'

@app.route('/add_article', methods=['POST'])
@db_session_wrap
def add_article(session):

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
        article_title    = jcontent['title']
        article_content  = jcontent['content']
    except:
        return TECH_ERR_CONTENT_IMPORT, HTTP_ERR

    article_authors = []
    article_regions = []

    try:
        article_authors = jcontent['authors']
        article_regions = jcontent['regions']
    except:
        print('OK, no region or author data')

    if ( checkstr_usr( username ) and checkstr_pwd( password ) ):
        if do_pam_auth ( username, password ):
            return do_add_article (session, article_title, article_content, article_authors, article_regions)
        else:
            return TECH_ERR_AUTHENTICATION , HTTP_FORB
    else:
        return TECH_ERR, HTTP_FORB

# usage note:
# curl -X POST  http://localhost:5000/edit_article --form username=gustavo --form password=floripa0   --form 'content={ "id":"3453455", "title":"R0 versus 2020","content":"exponentially spreading literature blala"}'

@app.route('/edit_article', methods=['POST'])
@db_session_wrap
def edit_article(session):

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
        id               = jcontent['id']
        article_title    = jcontent['title']
        article_content  = jcontent['content']
    except:
        return TECH_ERR_CONTENT_IMPORT, HTTP_ERR

    article_authors = []
    article_regions = []

    try:
        article_authors = jcontent['authors']
        article_regions = jcontent['regions']
    except:
        print('OK, no region or author data')

    if ( checkstr_usr( username ) and checkstr_pwd( password ) ):
        if do_pam_auth ( username, password ):
            return do_edit_article (session, id, article_title, article_content, article_authors, article_regions )
        else:
            return TECH_ERR_AUTHENTICATION , HTTP_FORB
    else:
        return TECH_ERR, HTTP_FORB
