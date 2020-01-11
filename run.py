from employeewebsite import db, app
""" This is where the application gets ran, database table is created, and app hosting"""

if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')