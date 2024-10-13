from django.conf import settings
import requests


class Paystack:
    """
    Payment verification
    """

    PAYSTACK_SK = settings.PAYSTACK_SECRET_KEY
    base_url = "https://api.paystack.co/"

    def verify_payment(self, ref, *args, **kwargs):
        path = f"transaction/verify/{ref}"
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SK}",
            "Content-Type": "application/json",
        }

        url = self.base_url + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            print(
                response_data, "this is the response data----------/-------------------"
            )
            return response_data["status"], response_data["data"]

        return False, response.text
