from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, validators
from flask_wtf import FlaskForm
from flaskext.mysql import MySQL
from wtforms.validators import URL
from wtforms.fields.html5 import URLField

import string
import random

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = "localhost"
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'bikinpw_shortener'

mysql = MySQL()
mysql.init_app(app)

class ShortForm(Form):
    long_url = URLField("", [validators.DataRequired(), validators.URL()],render_kw={"placeholder":"Link to shorten", "autofocus":True})
    short_url = StringField("", render_kw={"placeholder":"bikin.pw/"})

def url_generator(size=6, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
	
@app.route('/', methods=['GET', 'POST'])
def test():
    form = ShortForm(request.form)
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = request.form['short_url']
        rnd_url = url_generator()
        
        conn = mysql.connect()
        cur = conn.cursor()

        result = cur.execute("SELECT shorturl FROM urlshortener where shorturl = %s", [short_url])
        '''
        if(long_url == ""):
            message = "Please input your URL"
            return render_template('index.html', form = form, message = message)
        '''
        
        if(result == 0):
            if(short_url == ""):
                cur.execute("INSERT INTO urlshortener(longurl, shorturl, tanggal) values (%s, %s, now())", (long_url, rnd_url))
                conn.commit()
                conn.close()
                url_message = rnd_url
                return render_template('after_short.html', url_message = url_message)
            elif(not short_url.isalnum()):
                message = "Use letters, numbers, or both for Custom URL"
                return render_template('index.html', form = form ,message = message)
            else:
                cur.execute("INSERT INTO urlshortener(longurl, shorturl, tanggal) values (%s, %s, now())", (long_url, short_url))
                conn.commit()
                conn.close()
                url_message = short_url
                return render_template('after_short.html', url_message = url_message)
        else:
            message = "This Custom URL is already used by someone"
            return render_template('index.html', form = form, message = message)
        
    return render_template('index.html', form = form)
    
    
@app.route('/<string:shorturl>/', methods=['GET','POST'])
def shortenurl(shorturl):
    conn = mysql.connect()
    cur = conn.cursor()
    result = cur.execute("SELECT longurl FROM urlshortener where shorturl = binary %s", [shorturl])
    
    if(result == 0):
        return render_template('404.html')
    else:
        longurl = cur.fetchone()
        url = longurl[0]
        return redirect(url)

@app.route('/404')
def eroor():
    return render_template('404.html')

@app.route('/after')
def after():
    return render_template('after_short.html')

if __name__ == '__main__':
    app.run(debug=True)
	