# -*- coding: utf-8 -*-
"""Script to cross-post from Instagram to Mastodon/Pixelfed"""

import os
import sys
import time

from mastodon import Mastodon

from arguments import process_arguments
from network import get_new_posts
from util import print_log

default_settings = {
    "instance": None,
    "instagram-user": None,
    "user-name": None,
    "user-password": None,
    "token": "user_credentials.secret",
    "check-interval": 3600,
    "post-interval": 60,
    "fetch-count": 10,
    "carousel-limit": 4,
    "scheduled": False,
    "verbose": False,
}

settings = process_arguments(sys.argv, default_settings)

verbose = settings["verbose"]

if verbose:
    print_log(f"SETTINGS {settings}")

agree = [1, True, "true", "True", "yes", "Yes"]
if os.environ.get("USE_DOCKER"):
    ID_FILENAME = "/app/already_posted.txt"
elif os.environ.get("USE_KUBERNETES"):
    ID_FILENAME = "/data/already_posted.txt"
else:
    ID_FILENAME = "./already_posted.txt"

with open(ID_FILENAME, "a", encoding="utf-8") as f:
    f.write("\n")

fetched_user = settings["instagram-user"]
mastodon_instance = settings["instance"]
mastodon_token = settings["token"]

post_limit = settings["fetch-count"]
time_interval_sec = settings["check-interval"]  # 1d
post_interval = settings["post-interval"]  # 1m

using_mastodon = settings["carousel-limit"] > 0
mastodon_carousel_size = settings["carousel-limit"]
scheduled = settings["scheduled"]

user = {"name": settings["user-name"], "password": settings["user-password"]}

print_log("🚀 > Connecting to Mastodon/Pixelfed..", color="green")
mastodon_client = Mastodon(access_token=mastodon_token, api_base_url=mastodon_instance)

while True:
    get_new_posts(
        mastodon_client,
        mastodon_carousel_size,
        post_limit,
        ID_FILENAME,
        using_mastodon,
        mastodon_carousel_size,
        post_interval,
        fetched_user,
        user,
    )
    if scheduled:
        break
    time.sleep(time_interval_sec)
