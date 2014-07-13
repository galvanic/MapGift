import os
from flask import Flask, render_template, send_from_directory

# initialization
app = Flask(__name__)
app.config.update(
    DEBUG = True,
)

# helper functions
import mapgift

# controllers
@app.route('/style.css')
def css():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'css/style.css')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    return render_template('index.html',
    		providers   = mapgift.PROVIDERS,
    		next_map_id = 1)

@app.route("/assemble")
def assemble(map_id):
	return render_template('assemble.html')

@app.route("/archive")
def archive():
	return render_template('archive.html')

# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)