class UserError(Exception):
    def __init__(self, message):
        self.message = message


class InvalidEmailError(UserError):
    pass


class UserAlreadyRegisteredError(UserError):
    pass


class UserNotFoundError(UserError):
    pass

class IncorrectPasswordError(UserError):
    pass