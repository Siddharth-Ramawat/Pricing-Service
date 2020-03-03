import re
from passlib.hash import pbkdf2_sha512


class Utils():
    @staticmethod
    def is_valid_email(email: str):
        email_address_matcher = re.compile(r'^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password: str):
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password ,hashed_password):
        return pbkdf2_sha512.verify(password, hashed_password)
