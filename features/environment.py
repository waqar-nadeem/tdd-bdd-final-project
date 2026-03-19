"""
Environment for Behave Testing
"""
from os import getenv
from selenium import webdriver

WAIT_SECONDS = int(getenv("WAIT_SECONDS", "30"))
BASE_URL = getenv("BASE_URL", "http://localhost:8080")  # adjust if your app runs on 8080
DRIVER = getenv("DRIVER", "firefox").lower()


def before_all(context):
    """Executed once before all tests"""
    print(">>> before_all executed, setting base_url =", BASE_URL)
    context.base_url = BASE_URL
    context.wait_seconds = WAIT_SECONDS

    # Select either Chrome or Firefox
    if "firefox" in DRIVER:
        context.driver = get_firefox()
    else:
        context.driver = get_chrome()

    context.driver.implicitly_wait(context.wait_seconds)
    context.config.setup_logging()


def after_all(context):
    """Executed after all tests"""
    print(">>> after_all executed, quitting driver")
    context.driver.quit()


######################################################################
# Utility functions to create web drivers
######################################################################
def get_chrome():
    """Creates a headless Chrome driver"""
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def get_firefox():
    """Creates a headless Firefox driver"""
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    return webdriver.Firefox(options=options)