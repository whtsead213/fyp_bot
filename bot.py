import scenario
import sys
import random
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from scenario import scenario_list, attack_scenario_list
from sshtunnel import SSHTunnelForwarder
from selenium import webdriver
import config
import firebaseDAO

server = None

def create_driver(url,port):
    global server
    server = SSHTunnelForwarder(
        ('vml1wk054.cse.ust.hk', 22),
        ssh_username="bot",
        ssh_password="tobtobtobtob",
        remote_bind_address=('127.0.0.1', port),
        local_bind_address=('127.0.0.1', port)
    )
    server.start()
    print(server.local_bind_port)  # show assigned local port
    # work with `SECRET SERVICE` through `server.local_bind_port`.
    
    driver = webdriver.Chrome('./chromedrivers/chromedriver')
    driver.get('localhost:' + str(port))

    try:
        #dismiss the cookie message since it make the close button untouchable
        driver.find_element_by_xpath('/html/body/div[1]/div/a').click()
        print('dismissed cookie')
    except NoSuchElementException:
        print('can not find cookie message')
        pass
    
    #server.stop()
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
        driver = create_driver(url="url", port=config.config['normal_port'])
        for i in range(int(sys.argv[2])):
            try:
                scenario = random.choice(scenario_list)
                firebaseDAO.normal_record(str(scenario), str(datetime.now()), "PLEASE TYPE YOUR NAME HERE") 
                scenario(driver)
                
            except NoSuchElementException:
                continue
    if mode == 'custom' or mode == 'c':
        driver = create_driver(url="url", port=config.config['normal_port'])
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
                        firebaseDAO.normal_record(str(scenario_list[index]), str(datetime.now()), "PLEASE TYPE YOUR NAME HERE")
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
                        attack_port = "xss_port"
                        attack_type = "xss"
                    elif index == 2 or index == 3:
                        attack_port = "sql_potr"
                        attack_type = "sql_inj"
                    else:
                        attack_port = "normal_potr"
                        attack_type = "other"
                    driver = create_driver(url="url", port=config.config[attack_port])
                    try:
                        firebaseDAO.attack_record(attack_type=attack_type, attack_scenario=str(attack_scenario_list[index]), attack_time=str(datetime.now()), attacker="PLEASE TYPE YOUR NAME HERE")
                        attack_scenario_list[index](driver)
                    except NoSuchElementException:
                        continue
    
    print('Starting time: ' + starting_time)
    print('Ending time: ' + str(datetime.now()))