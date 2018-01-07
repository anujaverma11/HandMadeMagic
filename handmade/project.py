from flask import Flask, render_template, url_for, request, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Country, Region, Craft, HandiCraft, Photo, Video, Myart, Artist

from flask import session as login_session #importing flask version of sessions
import random, string #importing random and string python libraries which is used to create pseudo random string to identify each session

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
from flask import flash
import requests

CLIENT_ID = json.loads(open('client_secrets.json','r').read())['web']['client_id']

engine = create_engine('sqlite:///handmade.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login1')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    print ("The current session state is %s" % login_session['state'])
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/')
@app.route('/craft')
def showCrafts():
    crafts = session.query(Craft).all()
    return render_template('crafts.html', crafts = crafts)

@app.route('/craft/new')
def newCraft():
    return render_template('newCrafts.html', crafts = crafts)

@app.route('/craft/<int:craft_id>/edit')
def editCraft():
    return render_template('')

@app.route('/craft/<int:craft_id>/delete')
# def deleteCraft():

@app.route('/craft/<int:craft_id>/')
@app.route('/craft/<int:craft_id>/handicrafts')
def showSubCrafts(craft_id):
    craft = session.query(Craft).filter_by(id = craft_id).one()
    subCat = session.query(HandiCraft).filter_by(craft_id = craft_id)
    return render_template('handicrafts.html', craft=craft, subCat=subCat, craft_id=craft_id)



@app.route('/craft/<int:craft_id>/handicraft/new/')
def newSubCraft(craft_id):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editSubCraft function here


@app.route('/craft/<int:craft_id>/handicraft/<int:handicraft_id>/edit/')
def editSubCraft(craft_id, handicraft_id):
    return "page to edit a craft item. Task 2 complete!"

# Task 3: Create a route for deleteSubCraft function here


@app.route('/craft/<int:craft_id>/handicraft/<int:handicraft_id>/delete/')
def deleteSubCraft(craft_id, handicraft_id):
    return "page to delete a craft item. Task 3 complete!"

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)