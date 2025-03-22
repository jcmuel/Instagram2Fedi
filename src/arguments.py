# -*- coding: utf-8 -*-
"""Functions to process the arguments and the environment variables."""

import os

from util import print_log

instagram_user = os.environ.get("I2M_INSTAGRAM_USER")
user_name = os.environ.get("I2M_USER_NAME")
user_password = os.environ.get("I2M_USER_PASSWORD")
instance = os.environ.get("I2M_INSTANCE")
token = os.environ.get("I2M_TOKEN")
check_interval = os.environ.get("I2M_CHECK_INTERVAL")  # 1 hour
post_interval = os.environ.get("I2M_POST_INTERVAL")  # 1 hour
use_mastodon = os.environ.get(
    "I2M_USE_MASTODON"
)  # max carousel is 4, if there's no limit set to -1
fetch_count = os.environ.get(
    "I2M_FETCH_COUNT"
)  # how many instagram posts to fetch per check_interval

# run continuously (if False) or a single time (if True)
SCHEDULED_RUN = os.environ.get("I2M_SCHEDULED", '').lower() == "true"
VERBOSE_OUTPUT = os.environ.get("I2M_VERBOSE", '').lower() == "true"

if VERBOSE_OUTPUT:
    print_log("instagram", instagram_user)
    print_log("instagram", instance)
    print_log(token)
    print_log(check_interval)
    print_log(post_interval)
    print_log(use_mastodon)
    print_log(fetch_count)
    print_log(user_name)
    print_log(user_password)
    print_log(SCHEDULED_RUN)
    print_log(VERBOSE_OUTPUT)


def flags(args, defaults):
    """Process the flags and update the setting dictionary."""
    count = 1

    while len(args) > count:
        if args[count] == "--instance":
            defaults["instance"] = args[count + 1]
        elif args[count] == "--instagram-user":
            defaults["instagram-user"] = args[count + 1]
        elif args[count] == "--token":
            defaults["token"] = args[count + 1]
        elif args[count] == "--check-interval":
            defaults["check-interval"] = int(args[count + 1])
        elif args[count] == "--post-interval":
            defaults["post-interval"] = int(args[count + 1])
        elif args[count] == "--fetch-count":
            defaults["fetch-count"] = int(args[count + 1])
        elif args[count] == "--use-mastodon":
            defaults["carousel-limit"] = int(args[count + 1])
        elif args[count] == "--use-docker":
            defaults["use-docker"] = args[count + 1]
        elif args[count] == "--user-name":
            defaults["user-name"] = args[count + 1]
        elif args[count] == "--user-password":
            defaults["user-password"] = args[count + 1]
        elif args[count] == "--scheduled":
            defaults["scheduled"] = True
            count -= 1
        elif args[count] == "--verbose":
            defaults["verbose"] = True
            count -= 1
        else:
            print_log("❗ -> Wrong Argument Name!...", color="red")

        count += 2
    return defaults


def process_arguments(args, defaults):
    """Process the arguments and update the setting dictionary."""

    if instance:
        defaults["instance"] = instance
    if instagram_user:
        defaults["instagram-user"] = instagram_user
    if user_name:
        defaults["user-name"] = user_name
    if user_password:
        defaults["user-password"] = user_password
    if token:
        defaults["token"] = token
    if check_interval:
        defaults["check-interval"] = int(check_interval)
    if post_interval:
        defaults["post-interval"] = int(post_interval)
    if fetch_count:
        defaults["fetch-count"] = int(fetch_count)
    if use_mastodon:
        defaults["carousel-limit"] = int(use_mastodon)
    if SCHEDULED_RUN:
        defaults["scheduled"] = SCHEDULED_RUN
    if VERBOSE_OUTPUT:
        defaults["verbose"] = VERBOSE_OUTPUT

    # Command line arguments more prioritized,
    # if smth has been written in .env and in cmd args,
    # then Instagram2Fedi will take values from `cmd args`
    new_defaults = flags(args, defaults)
    return new_defaults
