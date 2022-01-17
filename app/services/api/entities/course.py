from app.models.base_entity import BaseEntity

SHARE_ID_PREFIX = "co_"


class Course(BaseEntity):
    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Course {self.data}>"

    @property
    def share_id(self):
        return f"{SHARE_ID_PREFIX}{str(self.id)}"

    @staticmethod
    def get_share_id(id):
        return id[3:] if id.startswith(SHARE_ID_PREFIX) else None
