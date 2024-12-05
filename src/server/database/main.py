from server.database.db import db
from server.database.models import User, File, Badge, UserBadge, ActivitySession
import common.utils as utils
from werkzeug.security import generate_password_hash, check_password_hash

def initDB():
    db.connect()
    db.create_tables([File, Badge, User, UserBadge, ActivitySession], safe=True)

def initDefaultDB(config):
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
        defaults={
            "username": "Admin",
            "identifiant": "admin",
            "email": config["admin"]["email"],
            "password": generate_password_hash(config["admin"]["password"]),
            "admin": True
        }
    )

    dev_badge = Badge.get(Badge.id == "dev")
    if not admin_user.badges.where(UserBadge.badge == dev_badge).exists():
        UserBadge.create(user=admin_user, badge=dev_badge)

    if utils.getDevModeStatus():
        admin_session = ActivitySession(admin_user)

    print("Initialisation terminée.")
