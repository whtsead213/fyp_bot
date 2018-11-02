import scenario
import sys
import random
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from scenario import scenario_list
from selenium import webdriver
import config

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
    
    driver = webdriver.Chrome('./chromedrivers/chromedriver')
    driver.get(config.config['url'])

    if mode == 'random' or mode == 'r':
        for i in range(int(sys.argv[2])):
            try:
                random.choice(scenario_list)(driver)
            except NoSuchElementException:
                continue
    if mode == 'custom' or mode == 'c':
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
    print('Starting time: ' + starting_time)
    print('Ending time: ' + str(datetime.now()))