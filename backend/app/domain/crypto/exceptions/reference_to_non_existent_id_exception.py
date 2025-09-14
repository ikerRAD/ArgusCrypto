class ReferenceToNonExistentIdException(Exception):
    def __init__(self, attr: str, attr_id: int):
        super().__init__(f"{attr} '{attr_id}' is non-existent")
