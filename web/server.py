from app.database import set_database_config
from app.controller import UrlController
from app.forms.ShortForm import ShortForm
from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app = set_database_config(app)

mysql = MySQL()
mysql.init_app(app)

csrf = CSRFProtect(app)

url_controller = UrlController()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ShortForm(request.form)
    if request.method == "POST":
        status, message = url_controller.post_url(request, mysql)

        if status == "used":
            app.logger.info("URL used")
            return render_template('index.html', form = form, message = message)
        
        if status == "error":
            app.logger.info("Validation form fails")
            return render_template('index.html', form = form ,message = message)

        if status == "found":
            app.logger.info("Inserting data to database")
            return render_template('after_short.html', url_message = message)
        
    return render_template('index.html', form = form)
    
    
@app.route('/<string:shorturl>/', methods=['GET'])
def shortenurl(shorturl):
    result = url_controller.get_short_url(mysql, shorturl)
    if result == "":
        app.logger.info("URL not found")
        return render_template('404.html')
    else:
        app.logger.info("Redirecting to %s", result)
        return redirect(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
	