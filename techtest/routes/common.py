import pam
import json

from techtest.models.article import Article
from techtest.models.region import Region
from techtest.models.author import Author

from flask import abort, jsonify, request

# limit strings to reasonables sizes
MAXSTR=2000
MINSTR=2
MAXUSR=20

# workout whitelists for usernames, passwords, cnames and emails
LOWERCASE="abcdefghijklmnopqrstuvwxyz"
UPPERCASE="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS="0123456789"
SYMBOLS="!?#$%&*@+-._=;:|/"
LETTERS = LOWERCASE + UPPERCASE
WHITELIST = NUMBERS + LETTERS + '.'
# restricted special chars to the most common ones - also on next.html and customvalidation.js
WHITELIST_PWD = SYMBOLS + NUMBERS + LETTERS
# usernames are ruby variable names, no other chars allowed or pupet will break
WHITELIST_USR = NUMBERS + LETTERS

# technical messages
TECH_OK = 'OK'
TECH_ERR = 'NOK'

# technical codes
HTTP_OK = 200
HTTP_FORB = 403
HTTP_ERR = 500

# and messages
TECH_MSG_AUTHOR_EXISTS        = 'That author already exists'
TECH_MSG_AUTHOR_ADDED         = 'Author added'
TECH_MSG_AUTHOR_UPDATED       = 'Author updated'
TECH_MSG_NX_AUTHOR            = 'No such author exists'
TECH_MSG_ARTICLE_EXISTS       = 'That article already exists'
TECH_MSG_ARTICLE_ADDED        = 'Article added'
TECH_MSG_ARTICLE_UPDATED      = 'Article updated'
TECH_MSG_ARTICLE_DELETED      = 'Article deleted'
TECH_MSG_NX_ARTICLE           = 'No such article exists'
TECH_MSG_AUTHORS_INCONSISTENT = 'One or more author ids do not exist'
TECH_MSG_REGIONS_INCONSISTENT = 'One or more region ids do not exist'
TECH_MSG_STR_INVALID          = 'Some of your input does not pass security validation'

TECH_ERR_JSON_IMPORT     = 'Error importing JSON input'
TECH_ERR_CONTENT_IMPORT  = 'Error on JSON content'
TECH_ERR_FORM_INPORT     = 'Error obtaining form input'
TECH_ERR_AUTHENTICATION  = 'Authentication error'

JSON_REPLY_LABEL         = 'reply'

# some helper functions

def mk_reply ( mystr ):
    return json.dumps ( { JSON_REPLY_LABEL:mystr } )

# checks wether the strings chars are acceptable - size range and no funny characters
def checkstr ( mystr, whitelist ):

    if ( len( mystr ) < MINSTR): return False
    if ( len( mystr ) > MAXSTR): return False

    if ( set( mystr ) <= set( whitelist ) ):
        return True
    else:
        return False

    return False

def checkstr_usr ( mystr ):
    return ( len (mystr) <= MAXUSR and checkstr ( mystr , WHITELIST_USR ) )

def checkstr_pwd ( mystr ):
    return checkstr ( mystr , WHITELIST_PWD )

def do_pam_auth ( username, password):
    return pam.authenticate(username, password)

# Author related

def do_add_author(session, first_name, last_name):

    if check_author(session, first_name, last_name):
        return mk_reply(TECH_MSG_AUTHOR_EXISTS), HTTP_OK
    else:
        session.add_all([ Author( first_name=first_name, last_name=last_name, ) ] )
        return mk_reply(TECH_MSG_AUTHOR_ADDED), HTTP_OK

def do_edit_author(session, id, first_name, last_name):

    if check_author_by_id(session, id):
        session.query( Author ).filter( Author.id == id ).update ( { Author.first_name: first_name, Author.last_name: last_name } )
        return mk_reply(TECH_MSG_AUTHOR_UPDATED), HTTP_OK
    else:
        return mk_reply(TECH_MSG_NX_AUTHOR), HTTP_OK

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

def get_author_by_id(session, id):

    query = session.query ( Author ).filter ( Author.id == id )

    return jsonify([author.asdict() for author in query.all()])

def check_authors (session, id_list):

    for id in id_list:
        if not check_author_by_id (session, id):
            return False

    return True

# Article related

def do_add_article(session, title, content, authors = [], regions = []):

    if check_article(session, title):
        return mk_reply(TECH_MSG_ARTICLE_EXISTS), HTTP_OK

    if not check_authors ( session, authors ):
        return mk_reply(TECH_MSG_AUTHORS_INCONSISTENT), HTTP_ERR

    if not check_regions ( session, regions ):
        return mk_reply(TECH_MSG_REGIONS_INCONSISTENT), HTTP_ERR

    # if it passed all validations
    obj_regions = []
    obj_authors = []
    for reg_id in regions:
       obj = session.query ( Region ).filter ( Region.id == reg_id ).all()[0]
       obj_regions.append(obj)

    for author_id in authors:
       obj = session.query ( Author ).filter ( Author.id == author_id ).all()[0]
       obj_authors.append(obj)

    session.add_all([ Article( title=title, content=content, authors = obj_authors, regions = obj_regions ) ] )
    return mk_reply(TECH_MSG_ARTICLE_ADDED), HTTP_OK

def do_edit_article(session, id, title, content, authors = [], regions = []):

    if not check_article_by_id(session, id):
        return mk_reply(TECH_MSG_NX_ARTICLE), HTTP_OK

    if not check_authors ( session, authors ):
        return mk_reply(TECH_MSG_AUTHORS_INCONSISTENT), HTTP_ERR

    if not check_regions ( session, regions ):
        return mk_reply(TECH_MSG_REGIONS_INCONSISTENT), HTTP_ERR

    # if it passed all validations
    obj_regions = []
    obj_authors = []
    for reg_id in regions:
       obj = session.query ( Region ).filter ( Region.id == reg_id ).all()[0]
       obj_regions.append(obj)

    for author_id in authors:
       obj = session.query ( Author ).filter ( Author.id == author_id ).all()[0]
       obj_authors.append(obj)

    # TODO it breaks if we try to update the regions and authors
    #session.query( Article ).filter( Article.id == id ).update ( { Article.title: title, Article.content: content } )
    #session.query( Article ).filter( Article.id == id ).update ( { Article.title: title, Article.content: content, Article.regions: obj_regions } )
    
    # this works but the article ID changes (it is incremented), would be better updating
    # the transaction handling is as recommended here
    # https://docs.sqlalchemy.org/en/13/orm/session_transaction.html
    try:
        session.query( Article ).filter( Article.id == id ).delete()
        session.add_all([ Article( title=title, content=content, authors = obj_authors, regions = obj_regions ) ] )
        session.commit()
    except:
        session.rollback()
        raise
    
    return mk_reply(TECH_MSG_ARTICLE_UPDATED), HTTP_OK

def do_delete_article(session, id):

    if not check_article_by_id(session, id):
        return mk_reply(TECH_MSG_NX_ARTICLE), HTTP_OK

    session.query( Article ).filter( Article.id == id ).delete()

    return mk_reply(TECH_MSG_ARTICLE_DELETED), HTTP_OK

def check_article(session, title):

    query = session.query( Article ).filter( Article.title == title )
    result = query.all()
    if len(result) == 0:
        return False
    else:
        return True

def check_article_by_id(session, id):

    query = session.query ( Article ).filter ( Article.id == id )
    result = query.all()
    if len(result) == 0:
        return False
    else:
        return True

def get_article_by_id(session, id):

    query = session.query ( Article ).filter ( Article.id == id )

    return jsonify([article.asdict() for article in query.all()])

# Region related

def check_region_by_id(session, id):

    query = session.query ( Region ).filter ( Region.id == id )
    result = query.all()
    if len(result) == 0:
        return False
    else:
        return True

def get_region_by_id(session, id):

    query = session.query ( Region ).filter ( Region.id == id )

    return jsonify([region.asdict() for region in query.all()])

def check_regions (session, id_list):

    for id in id_list:
        if not check_region_by_id (session, id):
            return False

    return True
