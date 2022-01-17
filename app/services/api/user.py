from injector import inject
from app.request import Request


class UserApiService:
    @inject
    def __init__(self, request: Request) -> None:
        self.request = request

    def get_or_create_response(self, external_id, data):
        response = self.request.post(
            f"/api/users/get-or-create/{external_id}/",
            data={
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "is_bot": data["is_bot"],
                "language_code": data["language_code"],
            },
        )
        return response

    def get_or_create(self, *args, **kwargs):
        response = self.get_or_create_response(*args, **kwargs)
        return response.json()
