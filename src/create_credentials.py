# Run this script once, to create the Mastodon login credentials for Instagram2Fedi.
# More info: https://mastodonpy.readthedocs.io/en/stable/
from mastodon import Mastodon

CLIENT_CREDENTIALS = '../client_credentials.secret'
USER_CREDENTIALS = '../user_credentials.secret'

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
