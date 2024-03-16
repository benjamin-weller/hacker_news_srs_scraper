import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re


def get_hn_articles(driver):
    hn_articles = set()
    for page_index in range(12):
        driver.get(
            f"https://hn.algolia.com/?dateRange=all&page={page_index}&prefix=false&query=spaced%20repetition&sort=byPopularity&type=story"
        )
        soup = BeautifulSoup(driver.page_source)
        for anchor_link in soup.findAll("a"):
            if anchor_link["href"] and (
                match := re.match(
                    r".*?news\.ycombinator\.com\/item\?id=\d+", anchor_link["href"]
                )
            ):
                # Remember that match 0 is the entire string and then it goes up from there
                hn_articles.add(match.group(0))
        time.sleep(2)
    return hn_articles


def extract_users_from_article(articles):
    users = set()
    for article in articles:
        response = requests.get(article)
        soup = BeautifulSoup(response.text)
        for user in soup.findAll("a", {"class": "hnuser"}):
            users.add(user.text)
    return users


def main():
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)  # Setting a max ten second wait time
    articles = get_hn_articles(driver)
    users = extract_users_from_article(articles)
    for x in users:
        print(x)


if __name__ == "__main__":
    main()
