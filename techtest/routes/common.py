import pam

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
TECH_MSG_AUTHOR_EXISTS  = 'That author already exists'
TECH_MSG_AUTHOR_ADDED   = 'Author added'
TECH_ERR_JSON_IMPORT    = 'Error importing JSON input'
TECH_ERR_CONTENT_IMPORT = 'Error on JSON content'
TECH_ERR_FORM_INPORT    = 'Error obtaining form input'

# some helper functions

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


