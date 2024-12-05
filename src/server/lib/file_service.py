from server.database.models import File

def create_file(name, path, type=None, size=None, description=None):
    """Crée un fichier dans la base de données."""
    file = File.create(
        name=name,
        path=path,
        type=type,
        size=size,
        description=description
    )
    return file

def get_all_files():
    """Récupère tous les fichiers."""
    return File.select()

def get_file_by_id(file_id):
    """Récupère un fichier par son ID."""
    return File.get_or_none(File.id == file_id)

def update_file(file_id, **kwargs):
    """Met à jour les informations d'un fichier."""
    file = get_file_by_id(file_id)
    if not file:
        return None
    for key, value in kwargs.items():
        if hasattr(file, key):
            setattr(file, key, value)
    file.save()
    return file

def delete_file(file_id):
    """Supprime un fichier par son ID."""
    file = get_file_by_id(file_id)
    if file:
        file.delete_instance()
        return True
    return False
