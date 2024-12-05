from server.database.db import db
from server.database.models import User, File, Badge, UserBadge
import common.utils as utils
from werkzeug.security import generate_password_hash, check_password_hash

def initDB():
    db.connect()
    db.create_tables([User, Badge, UserBadge, File], safe=True)

def initDefaultDB():
    if utils.getDevModeStatus():
        print("Initialisation des données par défaut...")

    default_badges = [
        {"id": "dev", "name": "Développeur", "description": "Badge attribué aux développeurs."},
        {"id": "admin", "name": "Administrateur", "description": "Badge pour les administrateurs."},
        {"id": "newbie", "name": "Nouveau", "description": "Badge attribué aux nouveaux utilisateurs."},
        {"id": "vip", "name": "VIP", "description": "Badge attribué aux utilisateurs VIP."}
    ]

    for badge_data in default_badges:
        Badge.get_or_create(id=badge_data["id"], defaults=badge_data)

    admin_user, created_user = User.get_or_create(
        username="admin",
        defaults={
            "identifiant": "admin",
            "email": "elyon@younity-mc.fr",
            "password": generate_password_hash("admin"),
            "admin": True
        }
    )

    dev_badge = Badge.get(Badge.id == "dev")
    if not admin_user.badges.where(UserBadge.badge == dev_badge).exists():
        UserBadge.create(user=admin_user, badge=dev_badge)

    if utils.getDevModeStatus():
        print("Initialisation terminée.")
