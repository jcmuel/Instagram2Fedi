import hashlib


def already_posted(identifier, path):
    with open(path) as file:
        content = file.read().split("\n")
        sha1 = hashlib.sha1(bytes(identifier, "utf-8")).hexdigest()
        if sha1 in content:
            return True
        return False


def mark_as_posted(identifier, path):
    with open(path, "a") as file:
        sha1 = hashlib.sha1(bytes(identifier, "utf-8")).hexdigest()
        file.write(sha1 + "\n")
