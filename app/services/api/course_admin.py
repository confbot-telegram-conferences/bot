from app.services.api.entities.course import Course
from app.services.api.base_resource import BaseResource


class CourseAdminApiService(BaseResource):
    def create_entity(self, **kwargs):
        return Course(**kwargs)

    def get_uri(self, **kwargs):
        return "/api/admin/courses/"
