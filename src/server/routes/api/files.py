from flask import request, jsonify, Blueprint
from server.services.files import create_file, get_all_files, get_file_by_id, delete_file
from common.path import get_path
from server.middleware.auth import login_required
import os.path

route_files = Blueprint("files", __name__)

@route_files.route('/')
def upload_form():
    return '''
    <!doctype html>
    <title>Upload un fichier</title>
    <h1>Uploader un fichier</h1>
    <form method="post" enctype="multipart/form-data" action="/api/files/upload">
        <input type="file" name="file">
        <input type="submit" value="Uploader">
    </form>
    '''

@route_files.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return 'Aucun fichier sélectionné', 400

    file = request.files['file']

    if file.filename == '':
        return 'Aucun fichier sélectionné', 400

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return f'Fichier téléchargé avec succès : {filename}'

    return 'Type de fichier non autorisé', 400