import uuid
from sqlalchemy import String


class UUID_F(String):
    UUID_SIZE = 36

    def __init__(self, *args, **kwargs):
        # We need to put this because of Cythonization issue that we had in CPD-6412 where
        # Thhe sqlalchemy doing some reflecation logic that tries to invoke the constructor with some additional arguments
        # That we want to ignore
        _ = args
        _ = kwargs

        super().__init__(self.UUID_SIZE)

    @staticmethod
    def uuid_allocator():
        return str(uuid.uuid4())