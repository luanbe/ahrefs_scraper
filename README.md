# ahrefs_scraper
3 scripts that I will be able to run from my local computer (details below)
- The first script will take input from input.xls and will generate the output file output-1.xls
- The second script will take input from input.xls and will generate the output file output-2.xls
- Then merge output-1.xls and output-2.xls to one file >> output-3.xls
- The third script will take output-3.xls and will generate the output file output-4.xls
################################################
1. Install Python on your windows system
- Link download Python: https://www.python.org/downloads/
- Please choose new version 3.9.x

################################################
2. Install package for your projects
- Open Command Line: Hold down Shift and right click on your project folder => Click to choose "Open PowerShell window here"
- Install package: Copy "pip install -r requirements.txt" and paste to your command line => Press Enter


################################################
3. Config settings file
- Open settings.py file in your folder project and choose edit with your editor. 
- Fill your Ahrefs account
- Fill others (optional)

################################################
If you completed steps above, you don't need to repeat it.
4. Run your script
- Open Command Line: Hold down Shift and right click on your project folder => Click to choose "Open PowerShell window here"
- Run script 1: Copy "python ahref_get_backlink.py" and paste to your command line => Press Enter
- After complete script 1, run script 2: Copy "python ahref_batch_analysis.py" and paste to your command line => Press Enter
- After complete script 2, run script 3: Copy "python filter_data.py" and paste to your command line => Press Enter

NOTES:
- You need have files "input.xlsx" and "blacklist keywords.txt" in folder "data" to run your script