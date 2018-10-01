## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required, DataRequired
import requests

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

def fetch_iTunes(term):
    baseurl = "https://itunes.apple.com/search"
    params = {  "term":  term,
                "media": 'music'}
    response    = requests.get(baseurl, params = params).json()
    return response['results']


####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
    album = StringField('Enter the name of an album:', validators=[Required()])

    options =[('1',1),('2',2),('3',3)]

    like   = RadioField('How much do you like this album? (1 low, 3 high)', validators=[Required()], choices = options)

    submit = SubmitField('Submit')


####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)




@app.route('/artistform')
def artistform():
    return render_template('artistform.html')

@app.route('/artistinfo', methods = ['GET'])
def artistinfo():
    artist = request.args.get("artist")
    results = fetch_iTunes(artist)
    return render_template('artist_info.html', objects = results)

@app.route('/artistlinks')
def artistlinks():
    return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def specific_artist(artist_name):
    results = fetch_iTunes(artist_name)
    return render_template('specific_artist.html', results = results)






@app.route('/album_entry')
def album_entry():
    form = AlbumEntryForm()
    return render_template('album_entry.html', form = form)


@app.route('/album_result', methods=['POST','GET'])
def album_result():
    form = AlbumEntryForm()    
    if form.validate_on_submit():
        return render_template('album_data.html', form=form)
    else:
        return "Sorry, try again!"
        print(form.errors)




if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
