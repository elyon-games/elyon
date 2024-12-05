import uuid
import datetime
from peewee import (CharField, ForeignKeyField, BooleanField, DecimalField, TextField, DateTimeField)
from server.database.db import BaseModel

class File(BaseModel):
    id = CharField(primary_key=True, max_length=50, unique=True, default=lambda: str(uuid.uuid4()))
    name = CharField(max_length=255)
    path = CharField(max_length=500)
    type = CharField(max_length=50, null=True)
    size = CharField(max_length=50, null=True)
    description = TextField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        super().save(*args, **kwargs)

class Badge(BaseModel):
    id = CharField(primary_key=True, max_length=50, unique=True, default=lambda: str(uuid.uuid4()))
    name = CharField(max_length=100, unique=True)
    description = TextField(null=True)

    @classmethod
    def get_all(cls):
        return cls.select()

    @classmethod
    def get_by_name(cls, name):
        return cls.get_or_none(cls.name == name)

class User(BaseModel):
    id = CharField(primary_key=True, max_length=50, unique=True, default=lambda: str(uuid.uuid4()))
    username = CharField(max_length=50)
    identifiant = CharField(max_length=50, unique=True)
    email = CharField(max_length=100, unique=True)
    password = CharField(max_length=100)
    created_at = DateTimeField(default=datetime.datetime.now)
    money = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    avatar = ForeignKeyField(File, backref='users', null=True)
    bio = TextField(null=True, default="")
    admin = BooleanField(default=False)

    def save(self, *args, **kwargs):
        if len(self.username) < 3:
            raise ValueError("Le username doit comporter au moins 3 caractères.")
        if len(self.identifiant) < 5:
            raise ValueError("L'identifiant doit comporter au moins 3 caractères.")
        return super().save(*args, **kwargs)

    def add_badge(self, badge):
        if not isinstance(badge, Badge):
            raise ValueError("Le badge doit être une instance de Badge.")
        try:
            user_badge = UserBadge.create(user=self, badge=badge)
            return user_badge
        except Exception as e:
            raise Exception(f"Erreur lors de l'ajout du badge: {e}")

    def set_avatar(self, avatar_file):
        if not isinstance(avatar_file, File):
            raise ValueError("L'avatar doit être une instance de File.")
        self.avatar = avatar_file
        try:
            self.save()
        except Exception as e:
            raise Exception(f"Erreur lors de l'ajout de l'avatar: {e}")

    def update_bio(self, new_bio):
        if not isinstance(new_bio, str):
            raise ValueError("La bio doit être une chaîne de caractères.")
        self.bio = new_bio
        try:
            self.save()
        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour de la bio: {e}")

    def update_money(self, new_money):
        if not isinstance(new_money, (int, float)) or new_money < 0:
            raise ValueError("Le montant doit être un nombre positif.")
        self.money = new_money
        try:
            self.save()
        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour de l'argent: {e}")

    def update_username(self, new_username):
        if not isinstance(new_username, str) or len(new_username) < 3:
            raise ValueError("Le nom d'utilisateur doit être une chaîne de caractères de minimum 3 caractères.")
        if User.select().where(User.username == new_username).exists():
            raise ValueError("Ce nom d'utilisateur est déjà pris.")
        self.username = new_username
        try:
            self.save()
        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour du nom d'utilisateur: {e}")

    def update_identifiant(self, new_identifiant):
        if not isinstance(new_identifiant, str) or len(new_identifiant) < 5:
            raise ValueError("L'identifiant doit être une chaîne de caractères de minimum 5 caractères.")
        if User.select().where(User.identifiant == new_identifiant).exists():
            raise ValueError("Cet identifiant est déjà pris.")
        self.identifiant = new_identifiant
        try:
            self.save()
        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour de l'identifiant: {e}")

    def update_password(self, new_password):
        if not isinstance(new_password, str) or len(new_password) < 8:
            raise ValueError("Le mot de passe doit être une chaîne de caractères de minimum 8 caractères.")
        self.password = new_password
        try:
            self.save()
        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour du mot de passe: {e}")

class UserBadge(BaseModel):
    id = CharField(primary_key=True, max_length=50, unique=True, default=lambda: str(uuid.uuid4()))
    user = ForeignKeyField(User, backref='badges')
    badge = ForeignKeyField(Badge, backref='users')
    created_at = DateTimeField(default=datetime.datetime.now)

class ActivitySession(BaseModel):
    id = CharField(primary_key=True, max_length=50, unique=True, default=lambda: str(uuid.uuid4()))
    user = ForeignKeyField(User, backref='sessions')
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    data = TextField(null=True)

    def save(self, *args, **kwargs):
        if not self.user:
            raise ValueError("La session doit être associée à un utilisateur.")
        self.updated_at = datetime.datetime.now()
        return super().save(*args, **kwargs)


