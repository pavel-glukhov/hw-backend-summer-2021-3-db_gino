import base64
from dataclasses import dataclass
from hashlib import sha256
from typing import Optional

import bcrypt

from app.store.database.gino import db


@dataclass
class Admin:
    id: int
    email: str
    password: Optional[str] = None

    def is_password_valid(self, password: str):
        hash_binary = base64.b64decode(self.password.encode('utf-8'))
        return bcrypt.checkpw(password.encode('utf-8'), hash_binary)

    @classmethod
    def from_session(cls, session: Optional[dict]) -> Optional["Admin"]:
        return cls(id=session["admin"]["id"], email=session["admin"]["email"])


class AdminModel(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)