import requests
import pickle

from .utils import random_sleep
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

def scrape_backlinks(url, username, user_agent, logger, *args, **kwargs):
    if kwargs.get('mode'):
        mode = kwargs.get('mode')
    else:
        mode = 'subdomains'

    if kwargs.get('protocol'):
        protocol = kwargs.get('protocol')
    else:
        protocol = ''

    if kwargs.get('request_deplay'):
        request_deplay = kwargs.get('request_deplay')
    else:
        request_deplay = (1,5)
    cookie_file_path = f'assets/cookies/{username}.pkl'

    cookies = pickle.load(open(cookie_file_path, "rb"))
    jar = requests.cookies.RequestsCookieJar()
    for cookie in cookies:
        if isinstance(cookie.get('expiry'), float): #Checks if the instance expiry a float 
            cookie['expiry'] = int(cookie['expiry']) # it converts expiry cookie to a int 

        jar.set(
                cookie.get('name'),
                cookie.get('value'),
                domain=cookie.get('domain'),
                path=cookie.get('path'),
                secure=cookie.get('secure'),
                rest={'HttpOnly': cookie.get('httpOnly')},
                expires=cookie.get('expiry'),
            )

    session = requests.Session()
    session.cookies = jar
    session.headers = {
        'user-agent': user_agent,
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest'
    }
    current_page = 1
    first = True
    while True:
        # Query URL
        query_url = f'https://ahrefs.com/site-explorer/backlinks/v7/external-similar-links/{mode}/live/en/all/dofollow/{current_page}/ahrefs_rank_desc?target={protocol}{url}'
        r = session.get(query_url)
        rows = r.json()
        current_page = int(rows['pager']['currentPage'])
        total_pages = int(rows['pager']['totalPages'])
        logger.info(f'Crawling data...in page: {current_page}')

        if rows.get('result'):
            if first:
                logger.info(f'Find backlinks in Ahrefs|No. Pages: {total_pages}')
            for row in rows['result']:
                yield {
                    'Total Backlinks': row['TotalBacklinks'],
                    'Domain Rating': row['DomainRating'],
                    'URL Rating': row['ahrefs_rank'],
                    'Ref domains Dofollow': row['refdomains'],
                    'Target': row['url_from'],
                    'Referring Page Title': row['title'],
                    'Internal Links Count': row['links_internal'],
                    'Backlinks Text': row['links_external'],
                    'Link URL': url,
                    'TextPre': row['text_pre'],
                    'Link Anchor': row['anchor'],
                    'TextPost': row['text_post'],
                    'Type': row['link_type'],
                    'Backlink Status': row['backlink_status'],
                    'First Seen': row['first_seen'],
                    'Last Check': row['last_visited'],
                    'Day Lost': row['lost_redirect_reason'],
                    'Language': row['Language'],
                    'Traffic': row['traffic'],
                    'Keywords': row['positions'],
                    'Js rendered': row['isJsRendered'],
                    'Linked Domains': row['linked_root_domains'],
                }
        else:
            logger.info(f'Not found backlinks in URL: {url}')
            break
            return False
        
        time_sleep = random_sleep(request_deplay)
        logger.info(f'Sleeped in {time_sleep}\'s')
        
        if current_page == total_pages:
            break
        else:
            current_page += 1
        
        first = False

def scrape_batch_analysis(source, logger):
    parse_only = SoupStrainer(id='batch_data_container')
    soup = BeautifulSoup(source, 'lxml', parse_only=parse_only)
    if soup.text:
        tbody = soup.find('tbody')
        list_tr = tbody.find_all('tr')
        
        for tr in list_tr:
            td = tr.find_all('td')
            yield {
                'Target': td[0].find('a')['href'],
                'Mode': td[1].text.strip(),
                'IP': td[2].text.strip(),
                'Keywords': td[3].text.strip(),
                'Traffic': td[4].text.strip(),
                'URL Rating': td[5].text.strip(),
                'Domain Rating': td[6].text.strip(),
                'Ahrefs Rank': td[7].text.strip(),
                'Ref domains Dofollow': td[9].text.strip(),
                'Dofollow': td[10].text.strip(),
                'Ref domains Governmental': td[11].text.strip(),
                'Ref domains Educational': td[12].text.strip(),
                'Ref IPs': td[14].text.strip(),
                'Ref SubNets': td[15].text.strip(),
                'Linked Domains': td[17].text.strip(),
                'Total Backlinks': td[19].text.strip(),
                'Backlinks Text': td[20].text.strip(),
                'Backlinks NoFollow': td[21].text.strip(),
                'Backlinks Redirect': td[22].text.strip(),
                'Backlinks Image': td[23].text.strip(),
                'Backlinks Frame': td[24].text.strip(),
                'Backlinks Form': td[25].text.strip(),
                'Backlinks Governmental': td[26].text.strip(),
                'Backlinks Educational': td[27].text.strip(),
            }
    else:
        return False
        
        
            