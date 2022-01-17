from app.services.api.entities.slide import Slide
from app.models.entities.user import User
from app.services.api.entities.conference import Conference
from app.services.api.base_resource import BaseResource


class ConferenceApiService(BaseResource):
    def create_entity(self, **kwargs):
        return Conference(**kwargs)

    def get_uri(
        self, course=None, channel=None, orphan_conferences=None, params=None, **kwargs
    ):
        params = params if params else {}
        if course:
            params["course"] = course
        if channel:
            params["channel"] = channel
        if orphan_conferences:
            params["orphan_conferences"] = True
        return "/api/conferences/", {**kwargs, **{"params": params}}

    def evaluate(self, evaluation, user: User, conference: Conference):
        url, _ = self.get_uri()
        return self.request.post(
            f"{url}{conference.id}/evaluate/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
            data={"evaluation": evaluation},
        )

    def statistics(self, conference_id, user: User):
        url, _ = self.get_uri()
        return self.request.get(
            f"{url}{conference_id}/statistics/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
        )

    def get_slide_by_position(self, conference_id, index, user: User):
        url, _ = self.get_uri()
        response = self.request.get(
            f"{url}{conference_id}/by-position/{index}/",
            headers=self.request.get_user_headers(user_id=user.backend_id),
        ).json()
        return Slide(**response["data"]), response["is_last"]
