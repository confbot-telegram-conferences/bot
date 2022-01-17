import json
from app.core.exception import BackendException
from injector import inject
import requests
from app.config import Config


class Request:
    @inject
    def __init__(self, config: Config) -> None:
        self.app_key = config.APP_KEY
        self.BACKEND_URL = config.BACKEND_URL
        session = requests.Session()
        session.headers.update({"Content-Type": "application/json"})
        self.session = session

    def _get_authorization_headers(self, user_id=None):
        return {
            "Authorization": json.dumps({"app_key": self.app_key, "user_id": user_id}),
        }

    def get_user_headers(self, user_id):
        return self._get_authorization_headers(user_id=user_id)

    def _request(self, method, url, headers=None, *args, **kwargs):
        headers = headers if isinstance(headers, dict) else {}
        headers = {**self._get_authorization_headers(), **headers}
        response = self.session.request(
            method, f"{self.BACKEND_URL}{url}", headers=headers, *args, **kwargs
        )
        if not response.ok:
            raise BackendException(
                response_data=response.json(),
                status_code=response.status_code,
                uri=f"{method} {url}",
                headers=headers,
                *args,
                **kwargs,
            )
        return response

    def get(self, uri, *args, **kwargs):
        return self._request("GET", uri, *args, **kwargs)

    def post(self, uri, data, *args, **kwargs):
        return self._request("POST", uri, data=json.dumps(data), *args, **kwargs)

    def patch(self, uri, data, *args, **kwargs):
        return self._request("PATCH", uri, data=json.dumps(data), *args, **kwargs)

    def delete(self, uri, *args, **kwargs):
        return self._request("DELETE", uri, *args, **kwargs)
