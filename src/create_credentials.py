"""
Run this script once, to create the Mastodon login credentials for Instagram2Fedi.
More info: https://mastodonpy.readthedocs.io/en/stable/
"""
import os
from mastodon import Mastodon

CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config"))
CLIENT_CREDENTIALS = os.path.join(CONFIG_DIR, "client_credentials.secret")
USER_CREDENTIALS = os.path.join(CONFIG_DIR, "user_credentials.secret")


if __name__ == "__main__":
    os.makedirs(CONFIG_DIR, exist_ok=True)

    base_url = input("Enter the Mastodon base URL (e.g. mastodon.social):")
    Mastodon.create_app(
        'Instagram2Fedi',
        api_base_url=f'https://{base_url}',
        to_file=CLIENT_CREDENTIALS
    )

    mastodon = Mastodon(client_id=CLIENT_CREDENTIALS, )
    print("Open the following URL in the browser and paste the code you get:")
    print(mastodon.auth_request_url())

    mastodon.log_in(
        code=input("Enter the OAuth authorization code:"),
        to_file=USER_CREDENTIALS
    )

    print(f"Client and user credentials stored in: {CONFIG_DIR}")
