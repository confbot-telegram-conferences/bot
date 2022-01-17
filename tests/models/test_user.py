from app.core.exception import EntityNotFoundException
from app.models.repositories.user_repository import UserRepository


def test_entity_not_found(injector, clear_collections):
    clear_collections(["users"])
    try:
        injector.get(UserRepository).get({"telegram_id": "not_found"})
        assert False
    except EntityNotFoundException:
        assert True


def test_get_or_create(injector, clear_collections):
    clear_collections(["users"])
    entity, _ = injector.get(UserRepository).get_or_create(
        {"telegram_id": "tele_11"}, telegram_id="tele_11", name="Jon"
    )
    assert entity.get("_id")
    other = injector.get(UserRepository).get({"telegram_id": "tele_11"})
    assert other == entity
