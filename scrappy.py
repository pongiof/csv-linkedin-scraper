#!/usr/bin/python3

import sys, getopt, csv, time
from selenium import webdriver
from linkedin_scraper import Person
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TIME_TO_SLEEP = 5

def pause(driver):
    print('Pause fetching for ' + str(TIME_TO_SLEEP) + ' seconds')
    driver.get('http://www.google.com/')
    element = WebDriverWait(driver, 10).until(EC.title_contains('Google'))
    time.sleep(TIME_TO_SLEEP * 6) # 6 times the standard time.

def processProfile(driver, data, index, pause_cnt):
    if pause_cnt and index % pause_cnt == 0:
        pause(driver)
    csv_output = []
    try:
        print('Processing profile ' + str(index) + ' ... ' + str(data[0]))
        profile = Person(data[0], driver = driver, scrape = False)
        profile.experiences = [] # Needed due to a bug in the library
        profile.educations = [] # Needed due to a bug in the library
        profile.scrape(close_on_complete=False)
        for ed in profile.educations:
            new_row = data[1:] # Dump any eventual pre-existing cols
            new_row.extend(['education',
                ed.institution_name,
                ed.from_date[38:], # Needed due to a bug in the library
                ed.to_date])
            csv_output.append(new_row)
        for w in profile.experiences:
            new_row = data[1:] # Dump any eventual pre-existing cols
            new_row.extend(['work',
                w.institution_name,
                w.position_title,
                w.description,
                w.from_date[15:], # Needed due to a bug in the library
                w.to_date])
            csv_output.append(new_row)
    except:
        e = sys.exc_info()[0]
        print('Error processing ' + str(data[0]) + ' error: ' + str(e))
        csv_output.append([data[0], 'error', e])
        pass
    return csv_output

def login(user, password, headless):
    print('Logging into Linkedin...')
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('http://www.linkedin.com/')
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-email')))
        element = driver.find_element_by_id('login-email')
        element.send_keys(user)
        element = driver.find_element_by_id('login-password')
        element.send_keys(password, Keys.ENTER)
    except:
        print('Error logging into Linkedin')
        sys.exit(2)
    return driver

def main(argv):
    usage = 'scrappy.py -i <inputfile> -o <outputfile> -u <user> -p <password> [-j] [-n <count>]'
    headless = False
    pause_cnt = 0
    try:
        opts, args = getopt.getopt(argv,"hjn:i:o:u:p:")
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt == '-i':
            inputfile = arg
        elif opt == '-o':
            outputfile = arg
        elif opt == '-u':
            user = arg
        elif opt == '-p':
            password = arg
        elif opt == '-j':
            # Chrome will be in headless mode
            headless = True
        elif opt == '-n':
            # Add a pause every <count> profiles to avoid throttling by Linkedin
            pause_cnt = int(arg)
    driver = login(user, password, headless)
    output = []
    # Process input
    with open(inputfile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        profiles = list(reader)
    profile_num = len(profiles)
    print('Processing ' + str(profile_num) + ' profiles')
    for index, row in enumerate(profiles):
        output.extend(processProfile(driver, row, index + 1, pause_cnt))
        time.sleep(TIME_TO_SLEEP) # Always sleep a bit between one profile and another.
    # Create output
    with open(outputfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ')
        writer.writerows(output)

if __name__ == "__main__":
   main(sys.argv[1:])
