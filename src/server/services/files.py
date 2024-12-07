from server.database.db import files as Files

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_file(name, path, type=None, size=None):
    file = Files.upload(
        name=name,
        path=path,
        type=type,
        size=size
    )
    return file

def get_all_files():
    return Files.get_all()

def get_file_by_id(file_id):
    return Files.get_by_id(file_id)

def delete_file(file_id):
    file = get_file_by_id(file_id)
    if file:
        return True
    return False
