
from flask import send_from_directory, request
from router.route import app


@app.route('/robots.txt', methods=("GET",))
@app.route('/sitemap.xml', methods=("GET",))
@app.route('/service-worker.js', methods=("GET",))
@app.route('/offline.html', methods=("GET",))
def pre_defined_links():
    return send_from_directory(app.static_folder, request.path[1:])
