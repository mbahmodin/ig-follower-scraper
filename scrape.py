import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import logging
from os.path import exists, join, abspath, dirname
from os import getenv, stat
from dotenv import load_dotenv

BASEDIR = abspath(dirname(__file__))
load_dotenv(join(BASEDIR, '.env'))

logging.getLogger()
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
# logging.disable

chrome_options = Options()
# chrome_options.add_argument("--headless")
s = Service('chromedriver.exe')
driver = webdriver.Chrome(service=s, options=chrome_options)

driver.get(
    'https://www.instagram.com/accounts/login/')

cookies_file = "cookies.pkl"

if not exists(f"{cookies_file}"):
    # create cookies.pkl if it doesn't exist
    fpkl = open(f"{cookies_file}", 'x')
    fpkl.close()

if stat(f"{cookies_file}").st_size > 0:
    # open the cookies jar
    cookies = pickle.load(open(f"{cookies_file}", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

if WebDriverWait(driver, 30).until(expected_conditions.visibility_of_all_elements_located(
    (By.NAME, "username")
    )):

    driver.find_element(By.NAME, "username").click
    driver.find_element(By.NAME, "username").send_keys(getenv("LOGIN_USERNAME"))
    driver.find_element(By.NAME, "password").click
    driver.find_element(By.NAME, "password").send_keys(
        getenv("LOGIN_PASSWORD"))
    driver.find_element(By.CSS_SELECTOR, ".\\_acan > .\\_ab8w").click()

    if WebDriverWait(driver, 30).until(expected_conditions.url_changes(
        "https://www.instagram.com/accounts/login/"
    )):
        logging.info("Login success!")
        pickle.dump(driver.get_cookies(), open(f"{cookies_file}", "w+b"))


# open the profiles followers list
ig_username = getenv("IG_USERNAME")
driver.get(f"https://www.instagram.com/{ig_username}/followers/")

# wait for it to load
WebDriverWait(driver, 30).until(expected_conditions.visibility_of_all_elements_located(
    (By.CSS_SELECTOR, ".\\_ab8y")
))

# get the last scroll value
last_scroll_height = driver.execute_script(
    "return document.getElementsByClassName('_aano')[0].scrollHeight"
    )


def get_username(i):
    username = driver.find_elements(
        By.CSS_SELECTOR, ".\\_ab8y")[i].text
    if username == "":
        username = "Null"
    return username

def write_username_to_file(username):
    f = "username.txt"
    fw = open(f, "a")
    fw.write(f"{username}\n")
    fw.close


def get_username_total():
    username = driver.find_elements(
        By.CSS_SELECTOR, ".\\_ab8y")
    return len(username)


count = 0
while count < get_username_total():

    username_total = get_username_total()
    username = get_username(count)
    logging.info(f"{username}\t{count}\t{username_total}")
    write_username_to_file(f"{username}")

    if count % 10 == 0:

        driver.execute_script(
            "document.getElementsByClassName('_aano')[0].scrollTop = document.getElementsByClassName('_aano')[0].scrollHeight;"
            )

        time.sleep(2)

        new_scroll_height = driver.execute_script(
            "return document.getElementsByClassName('_aano')[0].scrollHeight;")

        logging.info(f"You're now at scroll height: {new_scroll_height}")
        if new_scroll_height == last_scroll_height:
            logging.info(f"You're at the last scroll: {new_scroll_height}")
            break
        last_scroll_height = new_scroll_height

    count += 1