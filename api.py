from app.app import app
from routes.routes import routes

app.register_blueprint(routes, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
