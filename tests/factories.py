import faker
from factory import Faker, Factory
from app.core.context import UserContext
from app.models.entities import User

fake = faker.Faker()


def user_context() -> UserContext:
    return UserContext(1, fake.first_name_male(), fake.last_name(), "11", "en")


# def message_context(text=None) -> MessageContext:
#     return MessageContext(text if text else fake.text())


# TODO: The factories need to register the entities in the database
class UserFactory(Factory):
    class Meta:
        model = User

    name = Faker("name")
