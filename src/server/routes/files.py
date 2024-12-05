from flask import request, jsonify, Blueprint
from server.lib.file_service import create_file, get_all_files, get_file_by_id, delete_file
from common.path import get_path

route_files = Blueprint("files", __name__)

@route_files.route("/files", methods=["GET"])
def get_files():
    """Récupère tous les fichiers."""
    files = get_all_files()
    files_list = [{
        "id": file.id,
        "name": file.name,
        "path": file.path,
        "type": file.type,
        "size": file.size,
        "description": file.description,
        "created_at": file.created_at,
        "updated_at": file.updated_at
    } for file in files]
    return jsonify(files_list)

@route_files.route("/files/<file_id>", methods=["GET"])
def get_file(file_id):
    """Récupère un fichier par son ID."""
    file = get_file_by_id(file_id)
    if not file:
        return jsonify({"error": "Fichier non trouvé"}), 404
    return jsonify({
        "id": file.id,
        "name": file.name,
        "path": file.path,
        "type": file.type,
        "size": file.size,
        "description": file.description,
        "created_at": file.created_at,
        "updated_at": file.updated_at
    })

@route_files.route("/files", methods=["POST"])
def upload_file():
    """Télécharge un nouveau fichier."""
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier n'a été fourni"}), 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({"error": "Le fichier doit avoir un nom valide"}), 400

    upload_path = f"/{get_path("server_files")}/{uploaded_file.filename}"
    uploaded_file.save(upload_path)

    file = create_file(
        name=uploaded_file.filename,
        path=upload_path,
        type=uploaded_file.content_type,
        size=str(len(uploaded_file.read())),
        description=request.form.get("description"),
    )

    return jsonify({"message": "Fichier téléchargé avec succès", "file_id": file.id}), 201

@route_files.route("/files/<file_id>", methods=["DELETE"])
def delete_file_route(file_id):
    """Supprime un fichier."""
    success = delete_file(file_id)
    if not success:
        return jsonify({"error": "Fichier non trouvé"}), 404
    return jsonify({"message": "Fichier supprimé avec succès"})
