# Login page
LOGIN_PAGE_IDENTIFICATION = '//h1[text()="Sign in to Ahrefs"]'
LOGIN_PAGE_EMAIL_FIELD = '//input[@name="email"]'
LOGIN_PAGE_PASSWORD_FIELD = '//input[@name="password"]'
LOGIN_PAGE_SUBMIT_BUTTON = '//button[@type="submit"]'

# login page error
LOGIN_PAGE_ERROR = '//div[text()="Incorrect email or password"]'

# Login status
LOGIN_STATUS = '//div[@id="userMenuDropdown"]'
# Logout button
LOGOUT_BUTTON = '//div[contains(@class, "css-1mutql4-content") and contains(text(), "Sign out")]'

# Site Explorer
SE_SEARCH_PROTOCOL_FIELD = '//div[contains(@class,"input-group-addon")]/div[@class="dropdown"]'
SE_SEARCH_PROTOCOL_HTTP_HTTPS = '//div[@class="dropdown-menu"]//a[@data-scheme="http-https"]'
SE_SEARCH_PROTOCOL_HTTP = '//div[@class="dropdown-menu"]//a[@data-scheme="http"]'
SE_SEARCH_PROTOCOL_HTTPS = '//div[@class="dropdown-menu"]//a[@data-scheme="https"]'
SE_SEARCH_URL_FIELD = '//input[@id="se_index_target"]'
SE_SEARCH_INDEX_MOD_FIELD = '//div[contains(@class, "input-group-addon clickable")]'
SE_SEARCH_EXACT_MOD = '//div[@class="dropdown-menu"]//a[@data-mode="exact"]'
SE_SEARCH_PREFIX_MOD = '//div[@class="dropdown-menu"]//a[@data-mode="prefix"]'
SE_SEARCH_DOMAIN_MOD = '//div[@class="dropdown-menu"]//a[@data-mode="domain"]'
SE_SEARCH_SUBDOMAINS_MOD = '//div[@class="dropdown-menu"]//a[@data-mode="subdomains"]'
SE_SEARCH_BUTTON = '//button[@id="se_index_start_analysing"]'

SE_DATA_SHOW = '//table[@id="main_se_data_table"]'

# Batch Analysis
BA_SEARCH_URLS_FIELD = '//form[@id="form_analysis"]//textarea'

BA_SEARCH_PROTOCOL_FIELD = '(//form[@id="form_analysis"]//div[@class="dropdown clickable"])[1]'
BA_SEARCH_PROTOCOL_HTTP_HTTPS = '//form[@id="form_analysis"]//a[@name="ba_protocol_mode_switcher_links"][1]'
BA_SEARCH_PROTOCOL_HTTP = '//form[@id="form_analysis"]//a[@name="ba_protocol_mode_switcher_links"][2]'
BA_SEARCH_PROTOCOL_HTTPS = '//form[@id="form_analysis"]//a[@name="ba_protocol_mode_switcher_links"][3]'


BA_SEARCH_INDEX_MOD_FIELD = '(//form[@id="form_analysis"]//div[@class="dropdown clickable"])[2]'
BA_SEARCH_AUTO_MOD = '//form[@id="form_analysis"]//div[@name="ba_mode_switcher_links"][1]'
BA_SEARCH_EXACT_MOD = '//form[@id="form_analysis"]//div[@name="ba_mode_switcher_links"][2]'
BA_SEARCH_PREFIX_MOD = '//form[@id="form_analysis"]//div[@name="ba_mode_switcher_links"][3]'
BA_SEARCH_DOMAIN_MOD = '//form[@id="form_analysis"]//div[@name="ba_mode_switcher_links"][4]'
BA_SEARCH_SUBDOMAINS_MOD = '//form[@id="form_analysis"]//div[@name="ba_mode_switcher_links"][5]'

BA_SEARCH_INDEX_TYPE_FIELD = '//form[@id="form_analysis"]//div[@class="dropdown"]'
BA_SEARCH_LIVE_TYPE = '//form[@id="form_analysis"]//a[@name="ba_history_mode_switcher_links"][1]'
BA_SEARCH_RECENT_TYPE = '//form[@id="form_analysis"]//a[@name="ba_history_mode_switcher_links"][2]'
BA_SEARCH_HISTORICAL_TYPE = '//form[@id="form_analysis"]//a[@name="ba_history_mode_switcher_links"][3]'

BA_SEARCH_BUTTON = '//form[@id="form_analysis"]//button[@id="startAnalysisButton"]'

BA_DATA_SHOW = '//div[@id="batch_data_container"]'