from colorama import Fore, Style
import datetime

color_dict = {
    "red": Fore.RED,
    "green": Fore.GREEN,
    "blue": Fore.BLUE,
    "yellow": Fore.YELLOW,
    "white": Fore.WHITE,
}


def print_log(message, color="white"):
    if color not in color_dict:
        raise ValueError("Unknown log color: " + color)
    print(
        f"[{datetime.datetime.now()}] " + color_dict[color] + message + Style.RESET_ALL
    )
