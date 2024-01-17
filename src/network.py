# -*- coding: utf-8 -*-

import time

import requests
from instaloader import Instaloader, Profile
from instaloader.exceptions import QueryReturnedBadRequestException

from already_posted import already_posted, mark_as_posted
from converters import split_array, try_to_get_carousel
from util import print_log


def get_instagram_user(user, fetched_user):
    loader = Instaloader()

    print_log("🚀 > Connecting to Instagram...", color="green")

    if user["name"] is not None:
        print_log("User " + user["name"])
        session_file = user["name"] + "_session.sqlite"
        try:
            loader.load_session_from_file(user["name"], session_file)
            try:
                assert user["name"] == loader.test_login()
            except QueryReturnedBadRequestException:
                print_log(
                    "Instagram requires a human verification... connect via a browser to solve a captcha.",
                    color="red",
                )
                input("Press ENTER once the captcha is solved.")
                assert user["name"] == loader.test_login()
            print_log("Restored the session")
        except FileNotFoundError:
            print_log(
                "Found no active session... authentication attempt", color="yellow"
            )
            loader.login(user["name"], user["password"])
            print_log("Authentication successful", color="green")
            loader.save_session_to_file(session_file)
    return Profile.from_username(loader.context, fetched_user)


def get_image(url):
    try:
        print_log("🚀 > Downloading Image... " + url, color="yellow")

        response = requests.get(url, timeout=60)
        response.raw.decode_content = True

        print_log("✨ > Downloaded!", color="green")

        return response.content
    except Exception as err:
        print_log("💥 > Failed to download image.", color="red")
        print_log(err)


def upload_image_to_mastodon(url, mastodon):
    try:
        print_log("🐘 > Uploading Image...", color="yellow")
        media = mastodon.media_post(
            media_file=get_image(url), mime_type="image/jpeg"
        )  # sending image to mastodon
        print_log("✨ > Uploaded!", color="green")
        return media["id"]
    except Exception as err:
        print_log("💥 > failed to upload image to mastodon", color="red")
        print_log(err)


def toot(urls, title, mastodon):
    try:
        print_log("🐘 > Creating Toot..." + title, color="yellow")
        ids = []
        for url in urls:
            ids.append(upload_image_to_mastodon(url, mastodon))
        post_text = str(title) + " #bot #crosspost" + "\n"  # creating post text
        post_text = post_text.replace("@", "[at]")
        post_text = post_text[0:1000]

        if ids:
            print_log("Post identifiers:" + str(ids))
            mastodon.status_post(post_text, media_ids=ids)

    except Exception as err:
        print_log("😿 > Failed to create toot", color="red")
        print_log(err)


def get_new_posts(
    mastodon,
    mastodon_carousel_size,
    post_limit,
    already_posted_path,
    using_mastodon,
    carousel_size,
    post_interval,
    fetched_user,
    user,
):
    # fetching user profile to get new posts
    profile = get_instagram_user(user, fetched_user)
    # get list of all posts
    posts = profile.get_posts()
    stupidcounter = 0
    for post in posts:
        url_arr = try_to_get_carousel([post.url], post)
        # checking only `post_limit` last posts
        if stupidcounter < post_limit:
            stupidcounter += 1
            if already_posted(str(post.mediaid), already_posted_path):
                print_log("🐘 > Already Posted            "+ post.url, color="yellow")
                break  # Do not need to go back further in time
            print_log("Posting... " + post.url)
            if using_mastodon:
                urls_arr = split_array(url_arr, carousel_size)
                for urls in urls_arr:
                    toot(urls, post.caption, mastodon)
            else:
                toot(url_arr, post.caption, mastodon)
            mark_as_posted(str(post.mediaid), already_posted_path)
            time.sleep(post_interval)
        else:
            break
    print_log("✨ > Fetched All", color="green")
