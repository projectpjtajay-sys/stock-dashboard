import requests

class OutlookMCPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_upcoming_events(self, user_email: str):
        response = requests.get(
            f"{self.base_url}/calendar/events",
            params={"email": user_email}
        )

        if response.status_code != 200:
            raise Exception("Failed to fetch calendar events")

        return response.json()
