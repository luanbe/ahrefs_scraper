from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as Firefox_Options

def set_selenium_session(
    proxy_address,
    proxy_port,
    proxy_username,
    proxy_password,
    headless_browser,
    browser_profile_path,
    disable_image_load,
    page_delay,
    geckodriver_path,
    browser_executable_path,
    logfolder,
    logger,
    geckodriver_log_level,
    user_agent
):
    """Starts local session for a selenium server.
    Default case scenario."""

    browser = None

    firefox_options = Firefox_Options()

    if headless_browser:
        firefox_options.add_argument("-headless")

    if browser_profile_path is not None:
        firefox_profile = webdriver.FirefoxProfile(browser_profile_path)
    else:
        firefox_profile = webdriver.FirefoxProfile()

    if browser_executable_path is not None:
        firefox_options.binary = browser_executable_path

    # set "info" by default
    # set "trace" for debubging, Development only
    firefox_options.log.level = geckodriver_log_level

    # set English language
    firefox_profile.set_preference("intl.accept_languages", "en-US")

    # set User-Agent
    if user_agent is not None:
        firefox_profile.set_preference("general.useragent.override", user_agent)

    if disable_image_load:
        # permissions.default.image = 2: Disable images load,
        # this setting can improve pageload & save bandwidth
        firefox_profile.set_preference("permissions.default.image", 2)

    if proxy_address and proxy_port:
        firefox_profile.set_preference("network.proxy.type", 1)
        firefox_profile.set_preference("network.proxy.http", proxy_address)
        firefox_profile.set_preference("network.proxy.http_port", int(proxy_port))
        firefox_profile.set_preference("network.proxy.ssl", proxy_address)
        firefox_profile.set_preference("network.proxy.ssl_port", int(proxy_port))

    # mute audio while watching stories
    firefox_profile.set_preference("media.volume_scale", "0.0")

    # prevent Hide Selenium Extension: error
    firefox_profile.set_preference("dom.webdriver.enabled", False)
    firefox_profile.set_preference("useAutomationExtension", False)
    firefox_profile.set_preference("general.platform.override", "iPhone")
    firefox_profile.update_preferences()

    # geckodriver log in specific user logfolder
    geckodriver_log = "{}geckodriver.log".format(logfolder)

    browser = webdriver.Firefox(
        firefox_profile=firefox_profile,
        executable_path=geckodriver_path,
        log_path=geckodriver_log,
        options=firefox_options,
    )


    # authenticate with popup alert window
    if proxy_username and proxy_password:
        proxy_authentication(browser, logger, proxy_username, proxy_password)

    browser.implicitly_wait(page_delay)

    # Set maximum windows
    browser.maximize_window()

    return browser

def proxy_authentication(browser, logger, proxy_username, proxy_password):
    """ Authenticate proxy using popup alert window """

    # FIXME: https://github.com/SeleniumHQ/selenium/issues/7239
    # this feauture is not working anymore due to the Selenium bug report above
    logger.warning(
        "Proxy Authentication is not working anymore due to the Selenium bug "
        "report: https://github.com/SeleniumHQ/selenium/issues/7239"
    )

    try:
        # sleep(1) is enough, sleep(2) is to make sure we
        # give time to the popup windows
        sleep(2)
        alert_popup = browser.switch_to_alert()
        alert_popup.send_keys(
            "{username}{tab}{password}{tab}".format(
                username=proxy_username, tab=Keys.TAB, password=proxy_password
            )
        )
        alert_popup.accept()
    except Exception:
        logger.warning("Unable to proxy authenticate")