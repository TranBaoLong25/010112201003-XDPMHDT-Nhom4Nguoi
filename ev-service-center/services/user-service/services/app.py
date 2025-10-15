from flask import Flask, send_from_directory
from flask_cors import CORS
from controllers.user_controller import user_bp
import os

app = Flask(__name__,
            static_folder="../frontend",
            static_url_path="/")

CORS(app)
app.register_blueprint(user_bp, url_prefix="/api")

@app.route('/')
def serve_index():
    return send_from_directory("../frontend/customer", "login.html")

@app.route('/<path:path>')
def serve_frontend(path):
    return send_from_directory("../frontend", path)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
