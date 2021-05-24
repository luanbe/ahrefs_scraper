import pandas as pd
import settings
import re


if __name__ == '__main__':
    file_path = f'data/{settings.OUTPUT_3_FILE_NAME}'
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        
        # remove duplicate URLs from the column named “Referring Page URL”
        df = df.drop_duplicates(subset=['Target'])
        print('Complete to remove duplicate URL')
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        # remove URLs from “Referring Page URL” that contain any keyworks from a list of blacklist keywords.
        blacklist_kw_file_path = f'data/{settings.BACKLIST_KEYWORDS_FILE}'
        try:
            with open(blacklist_kw_file_path, 'r') as f:
                content_bls = f.read()
            blacklist_kws = content_bls.split('\n')
            for blacklist_kw in blacklist_kws:
                for index, rows in df.iterrows():
                    if not pd.isna(rows['Target']):
                        if blacklist_kw in rows['Target']:
                            url = rows['Target']
                            df = df.drop(index)
                            print(f'Remove URL {url} from blacklist keywords')
            print('Complete to remove URL from blacklist keywords')
        except FileNotFoundError:
            print('Not found file in {blacklist_kw_file_path}')
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')

        # Remove URLs that have more than 3 hyphens. Example: www.xyz.com/qwe-qwe-qwe-qwe-qwe
        for index, rows in df.iterrows():
            if not pd.isna(rows['Target']):
                hyphen_data = rows['Target'].split('-')
                count_hyphen_data = len(hyphen_data) - 1
                if count_hyphen_data > 3:
                    url = rows['Target']
                    df = df.drop(index)
                    print(f'Remove URL {url} have more than 3 hyphens')
        print('Complete to remove URLs have more than 3 hyphens')
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')

        # Remove URLs that have more than 20 characters after a query string. Query sting starts with “?”.  Example: www.xyz.com/?category=sdfsdfsdf&asdasdas&asdasdasd&asdasdasd
        for index, rows in df.iterrows():
            if not pd.isna(rows['Target']):
                url = rows['Target']
                search = re.search(r'.+\?(.+)', url)
                if search:
                    if len(search.group(1)) > 20:
                        df = df.drop(index)
                        print(f'Remove URL {url} with a query string have more than 20 characters')
        print('Complete to remove URLs with a query string have more than 20 characters')
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        output_file_path = f'data/{settings.OUTPUT_4_FILE_NAME}'
        df.to_excel(output_file_path, engine='openpyxl', index=False)
        print(f'Complete to filter data and export to file {output_file_path}')
    except FileNotFoundError:
        print(f'Not found file in {file_path}')