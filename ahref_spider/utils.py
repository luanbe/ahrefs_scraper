import random
import time
import pickle
import os

from sys import exit as clean_exit
from contextlib import contextmanager


def highlight_print(
    username=None, message=None, priority=None, level=None, logger=None
):
    """ Print headers in a highlighted style """
    # can add other highlighters at other priorities enriching this function

    # find the number of chars needed off the length of the logger message
    output_len = 28 + len(username) + 3 + len(message) if logger else len(message)
    show_logs = Settings.show_logs
    upper_char = None
    lower_char = None

    if priority in ["initialization", "end"]:
        # OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
        # E.g.:          Session started!
        # oooooooooooooooooooooooooooooooooooooooooooooooo
        upper_char = "O"
        lower_char = "o"

    elif priority == "login":
        # ................................................
        # E.g.:        Logged in successfully!
        # ''''''''''''''''''''''''''''''''''''''''''''''''
        upper_char = "."
        lower_char = "'"

    elif priority == "feature":  # feature highlighter
        # ________________________________________________
        # E.g.:    Starting to interact by users..
        # """"""""""""""""""""""""""""""""""""""""""""""""
        upper_char = "_"
        lower_char = '"'

    elif priority == "user iteration":
        # ::::::::::::::::::::::::::::::::::::::::::::::::
        # E.g.:            User: [1/4]
        upper_char = ":"
        lower_char = None

    elif priority == "post iteration":
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # E.g.:            Post: [2/10]
        upper_char = "~"
        lower_char = None

    elif priority == "workspace":
        # ._. ._. ._. ._. ._. ._. ._. ._. ._. ._. ._. ._.
        # E.g.: |> Workspace in use: "C:/Users/El/InstaPy"
        upper_char = " ._. "
        lower_char = None

    if upper_char and (show_logs or priority == "workspace"):
        print("{}".format(upper_char * int(ceil(output_len / len(upper_char)))))

    if level == "info":
        if logger:
            logger.info(message)
        else:
            print(message)

    elif level == "warning":
        if logger:
            logger.warning(message)
        else:
            print(message)

    elif level == "critical":
        if logger:
            logger.critical(message)
        else:
            print(message)

    if lower_char and (show_logs or priority == "workspace"):
        print("{}".format(lower_char * int(ceil(output_len / len(lower_char)))))

@contextmanager
def smart_run(session):
    try:
        session.session_load()
        yield
    except KeyboardInterrupt:
        clean_exit("You have exited successfully.")
    finally:
        session.session_quit()

def random_sleep(random_time):
    action_time = random.randint(random_time[0], random_time[1])
    time.sleep(action_time)
    return action_time

def load_cookie(url, browser, username, logger):
    cookie_file_path = f'assets/cookies/{username}.pkl'
    try:
        logger.info(f'Loading cookie file {cookie_file_path}')
        cookies = pickle.load(open(cookie_file_path, "rb"))
        browser.delete_all_cookies()
        # have to be on a page before you can add any cookies, any page - does not matter which
        browser.get("https://google.com" if url is None else url)

        for cookie in cookies:
            if isinstance(cookie.get('expiry'), float): #Checks if the instance expiry a float 
                cookie['expiry'] = int(cookie['expiry']) # it converts expiry cookie to a int 
            browser.add_cookie(cookie)
        return True
    except IOError:
        logger.info(f'Not find cookie file at {cookie_file_path}')
        return False

def save_cookie(browser, username, logger):
    cookie_file_path = f'assets/cookies/{username}.pkl'
    pickle.dump(browser.get_cookies() , open(cookie_file_path,"wb"))
    logger.info(f'Saved cookie file at {cookie_file_path}')

def check_and_create_file(file_path):
    if os.path.isfile(file_path) is not True:
        f = open(file_path, "w")
        f.close()
    