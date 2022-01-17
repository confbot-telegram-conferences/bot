from app.models.base_entity import BaseEntity


class Slide(BaseEntity):
    def __init__(self, **kwargs):
        return super().__init__(**{**{"text": "", "image": "", "voice": ""}, **kwargs})

    def __str__(self):
        return f'{self.position}: {self.text if self.text else ""}'

    def __repr__(self):
        return f"<Slide {self.data}>"
