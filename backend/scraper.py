import requests
from bs4 import BeautifulSoup

ROOT = 'https://collegearts.yale.edu'

def download_productions_page(number):
    """
    Download the HTML content of the page with the given number.
    :param number: Number of page to download. Note that this is zero-indexed.
    """
    cookies = {}
    headers = {}
    data = {
        'page': str(number),
        'view_name': 'shows_and_screenings',
        'view_display_id': 'block_1',
        'pager_element': '0',
    }

    response = requests.post(ROOT + '/views/ajax', cookies=cookies, headers=headers, data=data)
    return response.json()[2]['data']

def download_production_page(path):
    html = requests.get(ROOT + production_url).text
    return html


page_number = 0
production_urls = []
while True:  # TODO: clean this up
    # TEMPORARY early exit
    if page_number == 1:
        break

    page_html = download_productions_page(page_number)
    soup = BeautifulSoup(page_html, 'html.parser')
    production_rows = soup.find_all('div', {'class': 'views-row'})
    production_urls_page = [row.find('a')['href'] for row in production_rows]
    if len(production_urls_page) == 0:
        print(f'Found 0 productions on page {page_number}; terminating loop.')
        break
    production_urls += production_urls_page
    print(f'Scraped page {page_number} and located {len(production_urls_page)} productions (total {len(production_urls)}).')
    page_number += 1

productions = {}
for production_url in production_urls:
    production = {
        'id': production_url.replace('/events/shows-screenings/', ''),
    }
    page_html = download_production_page(production_url)
    soup = BeautifulSoup(page_html, 'html.parser')
    soup = soup.find('div', {'id': 'zone-content'})
    production['title'] = soup.find('h1').text.strip()
    date_section = soup.find('div', {'class': 'group-performance-date-'})
    date_section_rows = date_section.findChildren()
    parse_mode = None
    dates = []
    for row in date_section_rows:
        if row.name == 'h2':
            parse_mode = row.text.strip()
        elif parse_mode == 'Performance Dates & Times':
            # Note: we are throwing out time data here.
            # We probably don't need it but we could get it if we want.
            dt = datetime.datetime.strptime(row.text.strip(), '%B %e, %Y - %l%P')
            dates.append(dt.strftime('%Y-%m-%d')))

