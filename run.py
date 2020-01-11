from employeewebsite import db, app
""" This is where the application gets ran, database table is created, and app hosting"""

if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "5791628bb0b13ce0c676dfde280ba681"
    app.run(host='0.0.0.0')
