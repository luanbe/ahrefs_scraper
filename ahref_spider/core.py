import shutil
import logging
import re
import time
import pandas as pd
import sys

from . import ahrefs_pages
from . import ahrefs_xpath
from .browser import set_selenium_session
from .utils import random_sleep, load_cookie, save_cookie, check_and_create_file
from .ahref_helpers import scrape_backlinks, scrape_batch_analysis

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from logging.handlers import RotatingFileHandler





class ASpider:

    def __init__(
        self,
        username: str = None,
        password: str = None,
        page_delay: int = 25,
        action_delay: tuple = (1,5),
        request_delay: tuple = (5,10),
        batch_analysis_limit: int = 200,
        show_logs: bool = True,
        user_agent: str = None,
        proxy_address: str = None,
        proxy_port: str = None,
        proxy_username: str = None,
        proxy_password: str = None,
        headless_browser: bool = True,
        disable_image_load: bool = False,
        geckodriver_log_level: str = "info",  # "info" by default
    ):
        self.page_delay = page_delay
        self.action_delay = action_delay
        self.request_delay = request_delay
        self.batch_analysis_limit = batch_analysis_limit
        self.proxy_address = proxy_address
        self.proxy_port = proxy_port
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
        self.headless_browser = headless_browser
        self.disable_image_load = disable_image_load
        self.geckodriver_log_level = geckodriver_log_level
        self.show_logs = show_logs


        if username is None:
            raise Exception('Please add username!')
        else:
            self.username = username

        if password is None:
            raise Exception('Please add password!')
        else:
            self.password = password

        if user_agent is None:
            self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'

        ############ Browser Settings ############
        # Add profile browser path
        self.browser_profile_path = None

        # Add geckodriver path
        if sys.platform == 'win32':
            self.geckodriver_path = shutil.which('assets/windows/geckodriver.exe')
        elif sys.platform == 'darwin':
            self.geckodriver_path = shutil.which('assets/macos/geckodriver')
        else:
            self.geckodriver_path = shutil.which('assets/linux/geckodriver')

        # Add custom browser version path
        # self.browser_executable_path = 'assets/FirefoxPortable/App/Firefox64/firefox.exe'
        self.browser_executable_path = None

        # logs path
        self.logfolder = 'logs/'
    
        # Add logger
        self.logger = self.get_logger(self.show_logs)
        self.browser = set_selenium_session(
                        self.proxy_address,
                        self.proxy_port,
                        self.proxy_username,
                        self.proxy_password,
                        self.headless_browser,
                        self.browser_profile_path,
                        self.disable_image_load,
                        self.page_delay,
                        self.geckodriver_path,
                        self.browser_executable_path,
                        self.logfolder,
                        self.logger,
                        self.geckodriver_log_level,
                        self.user_agent
        )

    def login_status(self):
        try:
            login_satus = WebDriverWait(self.browser, 30).until(
                EC.presence_of_element_located((By.XPATH, ahrefs_xpath.LOGIN_STATUS))
            )
            if login_satus:
                return True

        except TimeoutException:
            return False

    def login_account(self):
        self.logger.info('Go to login page...')
        self.browser.get(ahrefs_pages.LOGIN_PAGE)
        login_page_identification = self.browser.find_element(By.XPATH, ahrefs_xpath.LOGIN_PAGE_IDENTIFICATION)
        
        # If find login page 
        if login_page_identification:
            self.logger.info('Processing to login account...')
            random_sleep(self.action_delay)
            # Get & send username
            email_field = self.browser.find_element(By.XPATH, ahrefs_xpath.LOGIN_PAGE_EMAIL_FIELD)
            email_field.send_keys(self.username)

            random_sleep(self.action_delay)
            # Get & send password
            password_field = self.browser.find_element(By.XPATH, ahrefs_xpath.LOGIN_PAGE_PASSWORD_FIELD)
            password_field.send_keys(self.password)

            random_sleep(self.action_delay)
            submit_button = self.browser.find_element(By.XPATH, ahrefs_xpath.LOGIN_PAGE_SUBMIT_BUTTON)
            submit_button.click()

            if self.login_status():
                self.logger.info('Login Successful...')
                save_cookie(self.browser, self.username, self.logger)
            else:
                login_page_error = self.browser.find_element(By.XPATH, ahrefs_xpath.LOGIN_PAGE_ERROR)
                if login_page_error:
                    self.logger.warning(f'Account login error: {login_page_error.text}')
                else:
                    self.logger.warning('Can\'t find errors on login page. Check logs to check it.')

                return False
           
        else:
            self.logger.warn('Don\'t find login page...')
            return False

    def session_load(self):
        self.logger.info('### SESSION LOAD ###')
        cookie_status = load_cookie(ahrefs_pages.DASHBOARD_PAGE, self.browser, self.username, self.logger)
        if cookie_status:
            self.browser.get(ahrefs_pages.DASHBOARD_PAGE)
            if self.login_status():
                self.logger.info('Login Successful...')
            else:
                self.login_account()
        else:
            self.login_account()

    def session_quit(self):
        if self.login_status():
            save_cookie(self.browser, self.username, self.logger)
        self.logger.info('### SESSION QUIT ###')
        self.browser.quit()
        
    def get_logger(self, show_logs: bool, log_handler=None):
        """
        Handles the creation and retrieval of loggers to avoid
        re-instantiation.
        """
        # initialize and setup logging system for the InstaPy object
        logger = logging.getLogger(self.username)
        logger.setLevel(logging.DEBUG)
        # log name and format
        general_log = "{}general.log".format(self.logfolder)
        check_and_create_file(general_log)

        file_handler = logging.FileHandler(general_log)
        # log rotation, 5 logs with 10MB size each one
        file_handler = RotatingFileHandler(
            general_log, maxBytes=10 * 1024 * 1024, backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        extra = {"username": self.username}
        logger_formatter = logging.Formatter(
            "%(levelname)s [%(asctime)s] [%(username)s]  %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(logger_formatter)
        logger.addHandler(file_handler)

        # add custom user handler if given
        if log_handler:
            logger.addHandler(log_handler)

        if show_logs is True:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(logger_formatter)
            logger.addHandler(console_handler)

        logger = logging.LoggerAdapter(logger, extra)
        return logger

    def search_backlinks(self, input_file_name, output_file_name, protocol=None, index_mode=None):
        df_data = pd.DataFrame()
        # read file excel
        self.logger.info(f'Begin to read file {input_file_name}')
        
        input_data = pd.read_excel(f'./data/{input_file_name}')

        # try:
        #     input_data = pd.read_excel(f'./data/{input_file_name}', engine='openpyxl')
        # except FileNotFoundError:
        #     self.logger.warning(f'Not found file in data/{input_file_name}')
        #     input_data = pd.DataFrame()
        
        if len(input_data) > 0:
            first_row = True
            self.logger.info(f'Scraper begin to crawl backlink data...')
            for row in input_data.values.tolist():
                url = row[0]
                # Remove ULR protocol
                url = re.sub(r'^https?\:\/\/?', '', url)
            
                # Choose protocol
                if protocol:
                    if protocol != 'http':
                        protocol = 'http://'
                    elif protocol != 'https':
                        protocol = 'https://'
                    else:
                        protocol = ''
                else:
                    protocol = ''

                # Choose index mode
                if index_mode:
                    if index_mode == 'e':
                        mode = 'exact'
                    elif index_mode == 'p':
                        mode = 'prefix'
                    elif index_mode == 'd':
                        mode = 'domain'
                    else:
                        mode = 'subdomains'
                else:
                    mode = 'subdomains'

                result = scrape_backlinks(url, self.username, self.user_agent, self.logger, protocol=protocol, mode=mode, request_deplay=self.request_delay)
                self.logger.info(f'Starting to crawl url {url}')
                if result:
                    for data in result:
                        # print(data)
                        if first_row == True:
                            for key, value in data.items():
                                df_data[key] = value
                        else:
                            rows = [
                                data['Total Backlinks'],
                                data['Domain Rating'],
                                data['URL Rating'],
                                data['Ref domains Dofollow'],
                                data['Target'],
                                data['Referring Page Title'],
                                data['Internal Links Count'],
                                data['Backlinks Text'],
                                data['Link URL'],
                                data['TextPre'],
                                data['Link Anchor'],
                                data['TextPost'],
                                data['Type'],
                                data['Backlink Status'],
                                data['First Seen'],
                                data['Last Check'],
                                data['Day Lost'],
                                data['Language'],
                                data['Traffic'],
                                data['Keywords'],
                                data['Js rendered'],
                                data['Linked Domains']
                            ]
                            length = len(df_data)
                            df_data.loc[length] = rows
                        first_row = False
            if len(df_data) > 0:
                df_data.to_excel(f'data/{output_file_name}')
                self.logger.info(f'Completed to scrape data with {length} backlinks and exported to data/{output_file_name}')
            else:
                self.logger.info(f'Not found backlink data from urls in file {input_file_name}')
        else:
            self.logger.warning(f'Not found rows in your file Excel. Please add data and run script again')

    def batch_analysis(self, input_file_name, output_file_name, protocol=None, index_mode=None, index_type=None):
        df_data = pd.DataFrame()
        limit = self.batch_analysis_limit - 1
        # read file excel
        self.logger.info(f'Begin to read file {input_file_name}')
        try:
            input_data = pd.read_excel(f'./data/{input_file_name}')
        except FileNotFoundError:
            self.logger.warning(f'Not found file in data/{input_file_name}')
            input_data = 0
        
        index_currently = 0
        index_end = limit
        if len(input_data) > 0:
            first_row = True
            while True:
               
                # find data with first and end data
                input_rows = input_data.loc[index_currently:index_end]

                if len(input_rows) > 0:
                    self.logger.info(f'Starting to scrape url from {index_currently} to {index_end} batch analysis page...')
                    new_rows = []
                    for input_row in input_rows.values.tolist():
                        new_rows.append(input_row[0])

                    # Get list urls to fill search
                    list_urls = '\n'.join([str(url) for url in new_rows])

                    # Choose protocol
                    if protocol:
                        if protocol != 'http':
                            protocol = ahrefs_xpath.BA_SEARCH_PROTOCOL_HTTP
                        elif protocol != 'https':
                            protocol = ahrefs_xpath.BA_SEARCH_PROTOCOL_HTTPS
                        else:
                            protocol = ahrefs_xpath.BA_SEARCH_PROTOCOL_HTTP_HTTPS
                    else:
                        protocol = ahrefs_xpath.BA_SEARCH_PROTOCOL_HTTP_HTTPS

                    # Choose index mode
                    if index_mode:
                        if index_mode == 'a':
                            mode = ahrefs_xpath.BA_SEARCH_AUTO_MOD
                        elif index_mode == 'p':
                            mode = ahrefs_xpath.BA_SEARCH_PREFIX_MOD
                        elif index_mode == 'd':
                            mode = ahrefs_xpath.BA_SEARCH_DOMAIN_MOD
                        elif index_mode == 's':
                            mode = ahrefs_xpath.BA_SEARCH_SUBDOMAINS_MOD
                        else:
                            mode = ahrefs_xpath.BA_SEARCH_EXACT_MOD
                    else:
                        mode = ahrefs_xpath.BA_SEARCH_EXACT_MOD

                    # Type Index
                    if index_type:
                        if index_type == 'r':
                            itype = ahrefs_xpath.BA_SEARCH_RECENT_TYPE
                        elif index_type == 'h':
                            itype = ahrefs_xpath.BA_SEARCH_HISTORICAL_TYPE
                        else:
                            itype = ahrefs_xpath.BA_SEARCH_LIVE_TYPE
                    else:
                        itype = ahrefs_xpath.BA_SEARCH_LIVE_TYPE


                    # Begin to start URL
                    self.browser.get(ahrefs_pages.BATCH_ANALYSIS_PAGE)

                    # Fill URLs to search field
                    search_field = self.browser.find_element(By.XPATH, ahrefs_xpath.BA_SEARCH_URLS_FIELD)
                    search_field.send_keys(list_urls)
                    random_sleep(self.action_delay)

                    # Choose protocol list
                    protocol_field = self.browser.find_element(By.XPATH, ahrefs_xpath.BA_SEARCH_PROTOCOL_FIELD)
                    protocol_field.click()
                    random_sleep(self.action_delay)
                    self.browser.find_element(By.XPATH, protocol).click()
                    random_sleep(self.action_delay)

                    # Choose target mod list
                    mod_field = self.browser.find_element(By.XPATH, ahrefs_xpath.BA_SEARCH_INDEX_MOD_FIELD)
                    mod_field.click()
                    random_sleep(self.action_delay)
                    self.browser.find_element(By.XPATH, mode).click()
                    random_sleep(self.action_delay)

                    # Choose target mod list
                    type_field = self.browser.find_element(By.XPATH, ahrefs_xpath.BA_SEARCH_INDEX_TYPE_FIELD)
                    type_field.click()
                    random_sleep(self.action_delay)
                    self.browser.find_element(By.XPATH, itype).click()
                    random_sleep(self.action_delay)

                    # Submit to search data
                    self.browser.find_element(By.XPATH, ahrefs_xpath.BA_SEARCH_BUTTON).click()

                    # Wait data show
                    try:
                        result_element = WebDriverWait(self.browser, 30).until(
                            EC.presence_of_element_located((By.XPATH, ahrefs_xpath.BA_DATA_SHOW))
                        )
                        random_sleep(self.action_delay)
                        result = scrape_batch_analysis(self.browser.page_source, self.logger)
                        if result:
                            for data in result:
                                # print(data)
                                if first_row == True:
                                    for key, value in data.items():
                                        df_data[key] = value
                                else:
                                    rows = [
                                        data['Target'],
                                        data['Mode'],
                                        data['IP'],
                                        data['Keywords'],
                                        data['Traffic'],
                                        data['URL Rating'],
                                        data['Domain Rating'],
                                        data['Ahrefs Rank'],
                                        data['Ref domains Dofollow'],
                                        data['Dofollow'],
                                        data['Ref domains Governmental'],
                                        data['Ref domains Educational'],
                                        data['Ref IPs'],
                                        data['Ref SubNets'],
                                        data['Linked Domains'],
                                        data['Total Backlinks'],
                                        data['Backlinks Text'],
                                        data['Backlinks NoFollow'],
                                        data['Backlinks Redirect'],
                                        data['Backlinks Image'],
                                        data['Backlinks Frame'],
                                        data['Backlinks Form'],
                                        data['Backlinks Governmental'],
                                        data['Backlinks Educational'],
                                    ]
                                    length = len(df_data)
                                    df_data.loc[length] = rows
                                first_row = False
                    except TimeoutException:
                        self.logger.info(f'Ahrefs Batch Analysis didn\'t showed backlinks')
                        break
                else:
                    self.logger.info(f'All urls in file {input_file_name} to crawled.')
                    break


                if index_currently > 0:
                    index_currently = index_currently + limit
                else:
                    index_currently = index_currently + limit + 1
                index_end += limit

            if len(df_data) > 0:
                df_data.to_excel(f'data/{output_file_name}')
                self.logger.info(f'Completed to scrape data with {length} backlinks and exported to data/{output_file_name}')
                return True
            else:
                self.logger.info(f'Not found backlink data from urls in file {input_file_name}')
                return False
        else:
            self.logger.warning(f'Not found rows in your file Excel. Please add data and run script again')
            return False


    def merge_data(self, file_output_name_1, file_output_name_2, file_output_name_3):
        try:
            df_1 = pd.read_excel(f'./data/{file_output_name_1}')
            file_ok = True
        except FileNotFoundError:
            file_ok = False
        
        if file_ok:
            self.logger.info(f'Starting to merge two file {file_output_name_1} and {file_output_name_2}')
            df_2 = pd.read_excel(f'./data/{file_output_name_2}')
            result = df_1.append(df_2)

            result.drop("Unnamed: 0", inplace=True, axis=1)
            result.to_excel(f'data/{file_output_name_3}')

            self.logger.info(f'Completed to merge files and output to file {file_output_name_3}')
        else:
            self.logger.warning(f'Not found file in data/{file_output_name_1}')