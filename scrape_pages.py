import os
import time

import bs4

from selenium import webdriver
from selenium_stealth import stealth

BASE_URL = "https://www.hltv.org"


def create_webdriver():
    """Create a stealth webdriver to fetch web pages and bypass detection.

    :return: the stealth web driver.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver


def scrape_match_hrefs(path: str):
    """Load in the saved HTML pages from the given path, parse the pages as soup objects, and extract the links to the
    individual match pages contained inside. Each page has within 0 to 100 links. Returned links must be appended to
    HLTV base URL to be absolute.

    :param path: path to directory containing scraped match result pages.
    :return: the hrefs for each match page.
    """
    match_hrefs = []
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), "r") as f:
            soup = bs4.BeautifulSoup(f, "lxml")
            if results_div := soup.find("div", {"class": "results-all"}):
                anchor_tags = results_div.find_all("a", href=True)
                hrefs = [tag["href"] for tag in anchor_tags]
                match_hrefs += [href for href in hrefs if "/matches/" in href]
    return match_hrefs


def scrape_match_page(url: str, base_url: str = BASE_URL):
    """Given a local match href, scrape the page and extract the link to download the demo file.

    :param url: local match href.
    :param base_url: base URL, defaults to HLTV base URL.
    :return: the demo href.
    """
    driver = create_webdriver()
    driver.get(base_url + url)
    html = driver.page_source
    driver.quit()
    soup = bs4.BeautifulSoup(html, "lxml")
    anchor_tags = soup.find_all("a", href=True)
    for anchor in anchor_tags:
        href = anchor["href"]
        if "/download/demo/" in href:
            return href


def main():
    # get 974 match hrefs to scrape
    scraped_hrefs = scrape_match_hrefs("res/match_results")

    # if you paused halfway through, you can pick up from where you left off
    start_idx = 1
    for i, match_href in enumerate(scraped_hrefs, start=start_idx):
        demo_href = scrape_match_page(match_href)

        # print index and demo href to stdout, just copy-paste into a file
        print(i, demo_href)

        # wait a few extra seconds between each request, so we don't get ip banned
        time.sleep(2)


if __name__ == "__main__":
    main()
