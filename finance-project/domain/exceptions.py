class InvalidUsername(Exception):
    pass


class InvalidTicker(Exception):
    pass


class NonExistentUserId(Exception):
    pass


class DuplicateUser(Exception):
    pass


class DuplicateAsset(Exception):
    def __init__(self, *args: object):
        super().__init__(args)
        self.ticker = None

    pass


class InvalidPersistenceType(Exception):
    pass


class FileError(Exception):
    pass


class InvalidPersistenceInfo(Exception):
    pass


class NonExistentAsset(Exception):
    pass


class UserIdNotFound(Exception):
    pass


class UserIDNotFound(Exception):
    pass


class InvalidPersistence(Exception):
    pass


class InvalidUserIdFormat(Exception):
    pass

class EntityNotFoundException:
    pass