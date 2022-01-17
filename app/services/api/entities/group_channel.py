from app.models.base_entity import BaseEntity


class GroupChannel(BaseEntity):
    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<GroupChannel {self.data}>"
