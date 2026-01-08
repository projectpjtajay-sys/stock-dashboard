import requests

class MCPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_user_context(self):
        response = requests.get(f"{self.base_url}/context")

        if response.status_code != 200:
            raise Exception("Failed to fetch user context")

        return response.json()
