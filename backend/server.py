from flask import Flask
from flask_cors import CORS
from routes import etl_bp, index_bp, pokemon_bp, filter_bp

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(etl_bp)
app.register_blueprint(index_bp)
app.register_blueprint(pokemon_bp)
app.register_blueprint(filter_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
