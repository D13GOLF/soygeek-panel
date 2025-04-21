from flask import Flask
from core.auth import auth_bp
from core.dashboard import dashboard_bp

app = Flask(__name__)
app.config.from_pyfile('config.py')

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(debug=True)
    
# ⚠️ Solo temporalmente para crear la base de datos en Render
if __name__ == '__main__':
    import init_db
    app.run()
