from views import create_app, db
from flask import Flask
from views import forms, routes, api_routes



app = create_app()



from views.models import User

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
