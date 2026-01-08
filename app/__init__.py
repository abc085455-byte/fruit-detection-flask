from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

    # ================= CONFIG =================
    app.config['UPLOAD_FOLDER'] = os.path.join(
        BASE_DIR, 'static', 'uploads'
    )

    app.config['RESULT_FOLDER'] = os.path.join(
        BASE_DIR, 'static', 'results'
    )

    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

    # Ensure folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

    # ================= ROUTES =================
    from .routes import main
    app.register_blueprint(main)

    return app
