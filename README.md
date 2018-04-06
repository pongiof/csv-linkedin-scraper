# csv-linkedin-scraper

Given an input CSV with a list of Linkedin profile URLs, scrapes education and work experience and dumps the data into an output CSV.

The input CSV must contain the profile URLs in the first column, any other column will be copied in the output CSV.

## Dependencies

The code uses:
- Python 3
- [Linkedin Scraper library](https://github.com/joeyism/linkedin_scraper/tree/master/linkedin_scraper)
- Selenium + WebDriver + Chrome Driver

## Usage

`scrappy.py -i <inputfile> -o <outputfile> -u <user> -p <password>`

- By default open Chrome browser, use `-j` option to use headless Chrome driver.
- use `-n <count>` to pause scraping every **<count>** profiles.
