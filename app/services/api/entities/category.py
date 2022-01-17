from app.models.base_entity import BaseEntity


class Category(BaseEntity):
    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Category {self.data}>"
