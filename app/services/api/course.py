from app.services.api.entities.course import Course
from app.services.api.base_resource import BaseResource


class CourseApiService(BaseResource):
    def create_entity(self, **kwargs):
        return Course(**kwargs)

    def get_uri(self, channel=None, params=None, **kwargs):
        params = params if params else {}
        if channel:
            params["channel"] = channel
        return "/api/courses/", {**kwargs, **{"params": params}}
