# -*- coding: utf-8 -*-

from util import print_log


def split_array(arr, size):
    count = len(arr) // size + 1
    new_arr = []
    for i in range(count):
        new_arr.append(arr[i * size : (i + 1) * size])
    return new_arr


def try_to_get_carousel(array, post):
    try:
        node = vars(post)["_node"]
        if "edge_sidecar_to_children" in node:
            try:
                urls = list(
                    map(
                        lambda arr: arr["node"]["display_url"],
                        node["edge_sidecar_to_children"]["edges"],
                    )
                )
                print_log("🎠 > Found carousel!", color="green")
                return urls
            except KeyError as err:
                print_log("🎠💥 > No carousel ", color="red")
                print_log(err)
                return array
        else:
            print_log("🎠💥 > No carousel", color="yellow")

        # We can also have video in a separate key
        if "is_video" in node and node["is_video"]:
            try:
                urls = [node["video_url"]]
                print_log("🎞 > Found video!", color="green")
                return urls
            except KeyError as err:
                print_log("🎞💥 > No video :(", color="red")
                print_log(err)
                return array
        else:
            print_log("🎠💥 > No video", color="yellow")

    except KeyError as err:
        print_log("😱💥 > No node :(", color="red")
        print_log(err)
        return array
    return array
