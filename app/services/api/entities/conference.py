from app.models.base_entity import BaseEntity


SHARE_ID_PREFIX = "c_"


class Conference(BaseEntity):
    def __init__(self, slides=None, active=False, **kwargs):
        super().__init__(**kwargs)
        self.slides = slides if slides else []
        self.active = active

    @property
    def share_id(self):
        return f"{SHARE_ID_PREFIX}{str(self.id)}"

    @staticmethod
    def get_share_id(id):
        return id[2:] if id.startswith(SHARE_ID_PREFIX) else None

    def __str__(self):
        return self.get("name") if self.get("name") else ""

    def __repr__(self):
        return f"<Conference {self.data}>"
