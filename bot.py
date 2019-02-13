import scenario
import sys
import random
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from scenario import scenario_list, attack_scenario_list
from selenium import webdriver
import config

def create_driver(url):
    driver = webdriver.Chrome('./chromedrivers/chromedriver')
    driver.get(config.config[url])

    try:
        #dismiss the cookie message since it make the close button untouchable
        driver.find_element_by_xpath('/html/body/div[1]/div/a').click()
        print('dismissed cookie')
    except NoSuchElementException:
        print('can not find cookie message')
        pass
    
    return driver

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('''Please follow the correct format to enter argument\n
                eg. python bot.py random 5
                    random scenario 5 times\n
                    or\n
                    python bot.py custom 1 2 3 
                    each argument is the index of the scenario\n''')
        exit()
    mode = sys.argv[1]

    print('Number of arguments: ', len(sys.argv), 'arguments.')
    print('Argument List: ', str(sys.argv))
    print('Bot mode: ' + mode)
    starting_time = str(datetime.now())
    
    


    if mode == 'random' or mode == 'r':
        driver = create_driver(url="url")
        for i in range(int(sys.argv[2])):
            try:
                random.choice(scenario_list)(driver)
            except NoSuchElementException:
                continue
    if mode == 'custom' or mode == 'c':
        driver = create_driver(url="url")
        for i in range(len(sys.argv)):
            if i == 0 or i == 1:
                continue
            else:
                index = int(sys.argv[i])
                if (index >= len(scenario_list) or index < 0):
                    print('scenario value out of bound, skipped')
                    continue
                else:
                    try:
                        scenario_list[index](driver)
                    except NoSuchElementException:
                        continue

    if mode == 'custom-attack' or mode == 'ca':
        for i in range(len(sys.argv)):
            if i == 0 or i == 1:
                continue
            else:
                index = int(sys.argv[i])
                if (index >= len(attack_scenario_list) or index < 0):
                    print('scenario value out of bound, skipped')
                    continue
                else:
                    if index == 0 or index == 1:
                        attack_url = "xss_url"
                    elif index == 2:
                        attack_url = "sql_url"

                    driver = create_driver(url=attack_url)
                    try:
                        attack_scenario_list[index](driver)
                    except NoSuchElementException:
                        continue
    
    print('Starting time: ' + starting_time)
    print('Ending time: ' + str(datetime.now()))