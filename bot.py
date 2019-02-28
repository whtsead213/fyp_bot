# Library import
import sys
import random
from time import sleep
from datetime import datetime
from selenium import webdriver
from sshtunnel import SSHTunnelForwarder
from selenium.common.exceptions import NoSuchElementException

# File import
import config
from firebaseDAO import FirebaseDAO
#import Scenarios.normalScenario
from Scenarios.normalScenario import Action
from Scenarios.attackScenario import DosAttack, ErrorAttack, TamperingAttack, XXEAttack, FileUploadAttack, SiteVisitingAttack, SQLAttack, XSSAttack
#from Scenarios.attackScenario import attack_scenario_dict, DosAttack, ErrorAttack, TamperingAttack, XXEAttack, FileUploadAttack, SiteVisitingAttack, SQLAttack, XSSAttack

server = None

def create_driver(url, port):
    global server
    server = SSHTunnelForwarder(
        ('vml1wk054.cse.ust.hk', 22),
        ssh_username="bot",
        ssh_password="tobtobtobtob",
        remote_bind_address=('127.0.0.1', port),
        local_bind_address=('127.0.0.1', port)
    )
    server.start()
    print("Local bind port: " + str(server.local_bind_port))  # show assigned local port
    # work with `SECRET SERVICE` through `server.local_bind_port`.
    
    driver = webdriver.Chrome('./chromedrivers/chromedriver')
    driver.get('localhost:' + str(port))

    try:
        if port == 43333:
            sleep(5)
            driver.switch_to_alert().accept()   # this is temparary implemented since an xss item is added
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
        firebaseDAO = FirebaseDAO(port=config.config['normal_port'], actionType="normal")
        action = Action(driver=driver, actionType="normal", firebaseDAO=firebaseDAO)
        for i in range(int(sys.argv[2])):
            try:
                scenario = random.choice(action.scenario_list)
                scenario()
                firebaseDAO.normal_record(str(scenario), str(datetime.now()), config.config['user_Albert']) 
            except NoSuchElementException:
                continue
    if mode == 'custom' or mode == 'c':
        driver = create_driver(url="url", port=config.config['normal_port'])
        firebaseDAO = FirebaseDAO(port=config.config['normal_port'], actionType="normal")
        action = Action(driver=driver, actionType="normal", firebaseDAO=firebaseDAO)
        
        for i in range(2, len(sys.argv)):
            index = int(sys.argv[i])
            if (index >= len(action.scenario_list) or index < 0):
                print('scenario value out of bound, skipped')
                continue  
            else:
                try:
                    action.scenario_list[index]()
                    firebaseDAO.normal_record(normal_scenario=str(action.scenario_list[index]), access_time=str(datetime.now()), creater=config.config['user_Albert'])
                except NoSuchElementException:
                    continue

    if mode == '-a' or mode == '--attack':
        attack_type = sys.argv[2]
        driver = create_driver(url="url", port=config.config[attack_type + "_port"])
        
        """attack_scenario_dict = {
            "dos" : DosAttack(driver=driver),
            "error" : ErrorAttack(driver=driver),
            "tampering" : TamperingAttack(driver=driver),
            "xxe" : XXEAttack(driver=driver),
            "file_upload" : FileUploadAttack(driver=driver),
            "site_visiting" : SiteVisitingAttack(driver=driver),
            "sql" : SQLAttack(driver=driver),
            "xss" : XSSAttack(driver=driver)
        }"""

        attack = None

        if attack_type == "dos":
            firebaseDAO = FirebaseDAO(port=config.config['dos_port'], actionType="dos")
            attack = DosAttack(driver=driver, attackType="dos", firebaseDAO=firebaseDAO)
        elif attack_type == "error":
            firebaseDAO = FirebaseDAO(port=config.config['error_port'], actionType="error")
            attack = ErrorAttack(driver=driver, attackType="error", firebaseDAO=firebaseDAO)
        elif attack_type == "tampering":
            firebaseDAO = FirebaseDAO(port=config.config['tampering_port'], actionType="tampering")
            attack = TamperingAttack(driver=driver, attackType="tampering", firebaseDAO=firebaseDAO)
        elif attack_type == "xxe":
            firebaseDAO = FirebaseDAO(port=config.config['xxe_port'], actionType="xxe")
            attack = XXEAttack(driver=driver, attackType="xxe", firebaseDAO=firebaseDAO)
        elif attack_type == "file_upload":
            firebaseDAO = FirebaseDAO(port=config.config['file_upload_port'], actionType="file_upload")
            attack = FileUploadAttack(driver=driver, attackType="file_upload", firebaseDAO=firebaseDAO)
        elif attack_type == "site_visiting":
            firebaseDAO = FirebaseDAO(port=config.config['site_visiting_port'], actionType="site_visiting")
            attack = SiteVisitingAttack(driver=driver, attackType="site_visiting", firebaseDAO=firebaseDAO)
        elif attack_type == "sql":
            firebaseDAO = FirebaseDAO(port=config.config['sql_port'], actionType="sql")
            attack = SQLAttack(driver=driver, attackType="sql", firebaseDAO=firebaseDAO)
        elif attack_type == "xss":
            firebaseDAO = FirebaseDAO(port=config.config['xss_port'], actionType="xss")
            attack = XSSAttack(driver=driver, attackType="xss", firebaseDAO=firebaseDAO)

        #attack = attack_scenario_dict[attack_type] if attack_type in attack_scenario_dict else None
        
        
        if attack:
            for i in range(3, len(sys.argv)):
                index = int(sys.argv[i])
                if False:#(index >= len(attack_scenario_dict[attack_type]) or index < 0):
                    #print('scenario value out of bound, skipped')
                    continue
                else:

                    try:
                        attack_starting_time = str(datetime.now())
                        attack.attack_scenario_list[index]()
                        #attack_scenario_dict[attack_type][index](driver)
                        firebaseDAO.attack_record(
                            attack_type=attack_type,
                            attack_scenario=str(attack.attack_scenario_list[index]),
                            attack_time=attack_starting_time,
                            attacker=config.config['user_Albert']
                        )
                    except NoSuchElementException:
                        continue

        else:
            print ("the given attack type is not valid")

        
    sleep(5)
    driver.close()
    server.stop()
    print('Starting time: ' + starting_time)
    print('Ending time: ' + str(datetime.now()))