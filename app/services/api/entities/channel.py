from app.models.base_entity import BaseEntity


class Channel(BaseEntity):
    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Channel {self.data}>"
