from app.services.api.entities.category import Category
from app.services.api.base_resource import BaseResource


class CategoryApiService(BaseResource):
    def create_entity(self, **kwargs):
        return Category(**kwargs)

    def get_uri(self, **kwargs):
        return "/api/categories/"

    def _process_list(self, data):
        return [self.create_entity(**item) for item in data]
