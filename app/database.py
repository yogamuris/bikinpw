def set_database_config(app):
    app.config['MYSQL_DATABASE_HOST'] = "localhost"
    app.config['MYSQL_DATABASE_PORT'] = 3306
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = 'bikinpw_shortener'
    app.config['SECRET_KEY'] = 'willbegreatapp'
    
    return app