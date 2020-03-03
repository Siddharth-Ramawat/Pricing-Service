from dataclasses import dataclass, field
from typing import Dict
import uuid
from models.model import Model
from common.utils import Utils
import models.user.errors as UserErrors


@dataclass()
class User(Model):
    collection: str = field(init=False, default='users')
    email: str
    password: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email) -> "User":
        try:
            return cls.find_one_by("email", email)
        except TypeError:
            raise UserErrors.UserNotFoundError("A user with this email was not found")

    @classmethod
    def is_login_valid(cls, email: str, password: str) -> bool:
        user = cls.find_by_email(email)

        if not Utils.check_hashed_password(password, user.password):
            raise UserErrors.IncorrectPasswordError("The password you entered was incorrect")

        return True

    @classmethod
    def register_user(cls, email, password) -> bool:
        if not Utils.is_valid_email(email):
            raise UserErrors.InvalidEmailError("The email address provided is not valid")

        try:
            cls.find_by_email(email)
            raise UserErrors.UserAlreadyRegisteredError("The User has already registered")
        except UserErrors.UserNotFoundError:
            User(email, Utils.hash_password(password)).save_to_mongo()

        return True