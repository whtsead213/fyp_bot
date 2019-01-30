import config

# from selenium import webdriver
import time
import json
import random
import datetime
import string
import paramiko
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from firebase import firebase

firebase = firebase.FirebaseApplication('https://ml-sec-fyp.firebaseio.com', None)


is_logged_in = False
accounts = []
current_logged_in = None
current_email = None
cart_is_filled = False

HONK_KOND_DIST = ["Hong Kong Island", "Kowloon", "New Territories"]
HONG_KONG_ADDR = {
    "Hong Kong Island":["Central and Western", "Eastern", "Southern", "Wan Chai"],
    "Kowloon":["Sham Shui Po", "Kowloon City", "Kwun Tong", "Wong Tai Sin", "Yau Tsim Mong"],
    "New Territories":["Islands", "Kwai Tsing", "North", "Sai Kung", "Sha Tin", "Tai Po", "Tsuen Wan", "Tuen Mun", "Yuen Long"]
}

ENGLISH_CHAR = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

"""
with open('accounts.json') as f:
    accounts = json.load(f)
    for ac in accounts:
        #print(type(ac)) #dict
        print(ac)
"""

for key in firebase.get('/accounts', None).keys():
    accounts.append(key)


def random_sleep(min=config.config['sleep_min'],max=config.config['sleep_max'],verbose=config.config['verbose']):
    assert(min<=max)
    sleep_time = random.randint(min,max)
    if verbose:
        print('sleep for %d seconds' %(sleep_time))
    sleep(sleep_time)


def random_comment(index, verbose=config.config['verbose']):
    '''
    Choose a random comment from good / bad comment list depends on the input index
    '''
    if index >= 3:
        i = random.choice(range(len(config.good_comments)))
        return config.good_comments[i]
    else:
        i = random.choice(range(len(config.bad_comments)))
        return config.bad_comments[i]


def random_return_home(driver, prob=config.config['return_home_probability'], verbose=config.config['verbose']):
    '''
    Randomly return home by clicking the home button

    params:
        driver: the original webdriver
        prob: probability to return home, defined in config
    '''
    random_prob = random.random()
    if random_prob <= prob:
        driver.find_element_by_xpath('/html/body/nav/div/div/a[2]/span').click() 
        random_sleep()


def comment_product(driver, prob=config.config["comment_product_probability"], verbose=config.config['verbose']):
    # if too fast, the product_review element cannot be found
    random_sleep(2, 3)
    #generate comment, usually good
    random_prob = random.random() 
    if random_prob <= prob:
        bias = random.randint(2,5) #tend to give good comment
        driver.find_element_by_xpath('//*[@id="product_review"]').send_keys(random_comment(bias))
        random_sleep(min=5, max=8) #make it longer
       
        #send the comment
        driver.find_element_by_xpath('//*[@id="submitButton"]').click() 
        random_sleep()
    
    #close the product window
    if verbose:
        print('click close')
    driver.find_element_by_xpath('/html/body/div[1]/div/div/section/footer/button').click()


def add_product_to_cart(driver, product_id=None, verbose=config.config['verbose']):
    global cart_is_filled

    min_add = config.config["add_product_to_cart_min"]
    max_add = config.config["add_product_to_cart_max"]
    r = random.randint(min_add,max_add)

    for i in range(r):
    #i dont know how to find all product in a page so i simply select the top one, please improve it if u know
        try:
            random_sleep(1,2)
            if product_id == None:
                driver.find_element_by_xpath('/html/body/main/div/section/table/tbody/tr[3]/td[5]/div/a[2]').click()
            else :
                #print('this should appear')
                product = '/html/body/main/div/section/table/tbody/tr[' + str(product_id) +']/td[5]/div/a[2]'
                #print(product)
                #print(product == '/html/body/main/div/section/table/tbody/tr[2]/td[5]/div/a[2]')
                driver.find_element_by_xpath(product).click()
            cart_is_filled = True
        except NoSuchElementException:
            pass
    if(random.random() < 0.3):
        scenario_checkout(driver)


def scenario_click_product(driver, page='home', verbose=config.config['verbose']):   
    #driver.get(config.config['url'])
    if(random.random() < 0.3):
        scenario_login(driver)
    max_clicks = config.config["home_product_clicks_max"]
    min_clicks = config.config["home_product_clicks_min"]
    clicks = random.randint(min_clicks,max_clicks)
    if verbose:
        print(clicks)
    for i in range(clicks):
        try:
            random_sleep(2,3)
            if page == 'home':
                product_id = random.randint(2,29)
            elif page == 'search':
                 product_id = random.randint(2,2)
            product = "/html/body/main/div/section/table/tbody/tr["+str(product_id)+"]/td[5]/div/a[1]"
            driver.find_element_by_xpath(product).click()
            comment_product(driver)
            if is_logged_in:
                #print('debug')
                random_prob = random.random()
                if random_prob <= config.config["add_product_to_cart_prob"]:
                    add_product_to_cart(driver, product_id=product_id)
        except NoSuchElementException:
            pass


def scenario_contact(driver, verbose=config.config['verbose']):
    '''
    This is a function that you can access the juiceshop and go to the comment page automatically
    You can follow this function as template to create more scenario
    Basically, you inspect the html element with chrome dev tool and copy the XPATH to the driver.find_element_by_xpath() function
    Then, follow by click() and send_keys() depends on what action you wanna do to that html element
    Also, use the random_sleep() function to create some random delay to make this natural
    '''
    if(random.random() < 0.2):
        return
    #initiate chrome
    #driver = webdriver.Chrome('./chromedrivers/chromedriver')

    #go to main page
    #driver.get(config.config['url']) # You can change this to other url if you don't want to access from main page
    random_sleep()

    #click contact us 
    driver.find_element_by_xpath('/html/body/nav/div/ul/li[7]/a').click() 
    random_sleep()
    random_return_home(driver)

    #leave comment, sample comments are in config.py
    #give good / bad comment according to star
    star = random.randint(1,5)
    driver.find_element_by_xpath('//*[@id="feedbackComment"]').send_keys(random_comment(star))
    random_sleep()

    #handle star
    
    if verbose:
        print(star)
    if star == 1:
        driver.find_element_by_xpath('/html/body/main/div/section/div/form/div[4]/div[3]/div/span/span/i[1]').click()
    elif star == 2:
        driver.find_element_by_xpath('/html/body/main/div/section/div/form/div[4]/div[3]/div/span/span/i[2]').click()
    elif star == 3:
        driver.find_element_by_xpath('/html/body/main/div/section/div/form/div[4]/div[3]/div/span/span/i[3]').click()
    elif star == 4:
        driver.find_element_by_xpath('/html/body/main/div/section/div/form/div[4]/div[3]/div/span/span/i[4]').click()
    elif star == 5:
        driver.find_element_by_xpath('/html/body/main/div/section/div/form/div[4]/div[3]/div/span/span/i[5]').click()
    random_sleep()
    random_return_home(driver)

    #handle captcha
    captcha = driver.find_element_by_xpath('//*[@id="captcha"]').text
    ans = eval(captcha)
    if verbose:
        print(captcha)
        print(ans)
    driver.find_element_by_xpath('/html/body/main/div/section/div/form/div[4]/div[4]/div/input').send_keys(ans)
    random_sleep()

    #send
    driver.find_element_by_xpath('//*[@id="submitButton"]').click()


def scenario_login(driver, verbose=config.config['verbose']):
    random_sleep()
    global is_logged_in
    global current_logged_in 
    global current_email
    if is_logged_in:
        return
    else:
        accounts = []
        for key in firebase.get('/accounts', None).keys():
            accounts.append(key)
        if(len(accounts) == 0):
            scenario_register()
            random_sleep()
        driver.find_element_by_xpath('/html/body/nav/div/ul/li[1]').click()
        random_sleep(1, 2)

        # Choose a user credential randomly
        uid = random.randint(0, len(accounts) - 1)
        current_email = accounts[uid]
        acc = firebase.get('/accounts', current_email)
        passwd = acc['pw']
        email = current_email + '@' + acc['host']

        current_logged_in = uid

        #driver.find_element_by_xpath('//*[@id="userEmail"]').send_keys(email)
        driver.find_element_by_xpath('//*[@id="userEmail"]').send_keys("a@gmail.com")
        #driver.find_element_by_xpath('//*[@id="userPassword"]').send_keys(passwd)
        driver.find_element_by_xpath('//*[@id="userPassword"]').send_keys("abc123")
        driver.find_element_by_xpath('//*[@id="loginButton"]').click()
        is_logged_in = True
        if verbose:
            print(email + 'is logged in')
        random_sleep(2, 3)


def scenario_logout(driver, verbose=config.config['verbose'], p=0.8):
    if(random.random() < (1-p)):
        return
    random_sleep(2, 3)

    global is_logged_in
    global current_logged_in
    if is_logged_in:
        try:
            driver.find_element_by_xpath('/html/body/nav/div/ul/li[2]/a/span').click()
            is_logged_in = False
            current_logged_in = None

            if verbose:
                print('logged out')

            cart_is_filled = False
        except:
            pass
        random_sleep(2, 3)
    else:
         return


def scenario_search(driver, verbose=config.config['verbose']):
    random_sleep()

    if(random.random() < 0.3):
        scenario_login(driver)
    r = random.randint(0, len(config.search_keyword) - 1)
    driver.find_element_by_xpath('/html/body/nav/div/ul/li[4]/form/div/input').clear()
    driver.find_element_by_xpath('/html/body/nav/div/ul/li[4]/form/div/input').send_keys(config.search_keyword[r])
    random_sleep()
    driver.find_element_by_xpath('//*[@id="searchButton"]').click()
    scenario_click_product(driver,page='search')


def scenario_checkout(driver, verbose=config.config['verbose']):
    global is_logged_in
    global current_logged_in
    global current_email
    global accounts
    global cart_is_filled
    if is_logged_in:
        random_sleep(2,3)
        driver.find_element_by_xpath('/html/body/nav/div/ul/li[5]/a').click()
        if(not cart_is_filled):
            driver.find_element_by_xpath('/html/body/nav/div/div/a[2]/span').click() 
            random_sleep()
            return
        driver.find_element_by_xpath('//*[@id="checkoutButton"]').click()

        # wait 7 sec to ensure the browser jumped to order pdf
        sleep(7) 
        order = driver.current_url[39:-4]
        print(order)
        prev_order = firebase.get('/accounts/' + current_email, 'orders')
        if(prev_order is None):
            orders = {order: True}
            firebase.put('/accounts/' + current_email, 'orders', orders)
        else:
            prev_order[order] = True
            firebase.put('/accounts/' + current_email, 'orders', prev_order)
        """
        accounts[current_logged_in]['orders'].append(order)
        with open('accounts.json', 'w') as f:
            json.dump(accounts, f, indent=4)
        """
        driver.get(config.config['url'])
    else:
        pass


def scenario_track_order(driver, verbose=config.config['verbose']):
    global is_logged_in
    global current_logged_in
    global accounts
    global current_email
    if is_logged_in:
        random_sleep()
        driver.find_element_by_xpath('/html/body/nav/div/ul/li[9]/a').click()
        try:
            # order = accounts[current_logged_in]['orders'].pop()
            orders = firebase.get('/accounts/' + current_email, 'orders')
            if(orders is None):
                driver.find_element_by_xpath('/html/body/nav/div/div/a[2]/span').click() 
                random_sleep()
                return
            else:
                order = random.choice(list(orders.keys()))
            driver.find_element_by_xpath('//*[@id="orderId"]').send_keys(order)
            driver.find_element_by_xpath('//*[@id="trackButton"]').click()
        except IndexError:
            pass
    else:
        pass


def scenario_complain(driver, verbose=config.config['verbose']):
    if(random.random() < 0.2):
        return
    random_sleep()
    driver.find_element_by_xpath('//*[@id="complaintMessage"]').send_keys(random_comment(2))
    driver.find_element_by_xpath('//*[@id="submitButton"]').click()
    # skip the upload invoice, whatever


def scenario_recycle(driver, verbose=config.config['verbose']):
    global is_logged_in
    global current_logged_in
    global accounts
    global HONK_KOND_DIST
    global HONG_KONG_ADDR

    # 1. Check if is log in
    if not is_logged_in:
        scenario_login(driver=driver, verbose=verbose)

    if(random.random() < 0.4):
        return

    # 2. input recycle request
    
    # Quantity
    random_quan = random.randint(10, 1000)
    
    # Address
    random_dist = random.randint(0, 2)
    random_address = str(HONG_KONG_ADDR[HONK_KOND_DIST[random_dist]][random.randint(0, len(HONG_KONG_ADDR[HONK_KOND_DIST[random_dist]])-1)]) +\
     str(HONK_KOND_DIST[random_dist]) +\
     "Hong Kong SAR"

    if verbose:
        print ("Address: " + str(random_address))

    driver.find_element_by_xpath('/html/body/nav/div/ul/li[8]').click()
    random_sleep(1, 2)
    driver.find_element_by_xpath('//*[@id="recycleQuantity"]').send_keys(random_quan)
    random_sleep(1, 2)
    driver.find_element_by_xpath('//*[@id="recycleAddress"]').send_keys(random_address)

    if (random_quan > 100) and (random.randint(0, 1) == 1):
        driver.find_element_by_xpath('//*[@id="isPickup"]').click()

        pick_up_date = datetime.datetime.now() + datetime.timedelta(days=random.randint(0, 30))
        
        if verbose:
            print ("00" + str(pick_up_date.year) + str(pick_up_date.month) + str(pick_up_date.day))
        
        random_sleep(1, 2)
        driver.find_element_by_xpath('//*[@id="recyclePickupDate"]').send_keys("00" + str(pick_up_date.year) + str(pick_up_date.month) + str(pick_up_date.day))
        

    driver.find_element_by_xpath('//*[@id="submitButton"]').click()

    return
    


def scenario_change_password(driver, verbose=config.config['verbose']):
    global is_logged_in
    global current_logged_in
    global accounts
    global current_email
    
    if(random.random() < 0.8):
        return
    # 1. Check if is log in
    if not is_logged_in:
        scenario_login(driver=driver, verbose=verbose)
    
    # 2. change the password with the current time and update the json file
    passwdCharLength = random.randint(8, 15)
    # old_password = accounts[current_logged_in]['pw']
    old_password = firebase.get('/accounts/' + current_email, 'pw')
    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=passwdCharLength))

    driver.find_element_by_xpath('/html/body/nav/div/ul/li[6]').click()
    random_sleep(1, 2)

    # input the new password and update
    driver.find_element_by_xpath('//*[@id="currentPassword"]').send_keys(old_password)
    random_sleep(1, 2)
    driver.find_element_by_xpath('//*[@id="newPassword"]').send_keys(new_password)
    driver.find_element_by_xpath('//*[@id="newPasswordRepeat"]').send_keys(new_password)
    random_sleep(1, 2)
    driver.find_element_by_xpath('//*[@id="changeButton"]').click()
    
    # Update data
    firebase.put('/accounts/' + current_email, 'pw', new_password)

    """
    # update the JSON and account
    accounts[current_logged_in]['pw'] = new_password
    with open('accounts.json', 'w') as f:
        json.dump(accounts, f, indent=4)

    """
    scenario_logout(driver, p=1)
    return


def scenario_about_us(driver, verbose=config.config['verbose']):
    
    if(random.random() < 0.4):
        return

    driver.find_element_by_xpath('/html/body/nav/div/ul/li[12]').click()
    random_sleep(1, 2)

    row_time = random.randint(0, 10)

    if verbose:
        print ("row time = " + str(row_time))

    for i in range(0, row_time):
        random_left_right = random.randint(0, 1)
        if random_left_right == 0:
            driver.find_element_by_xpath('/html/body/main/div/div/section[1]/div/div/a[1]').click()
        else:
            driver.find_element_by_xpath('/html/body/main/div/div/section[1]/div/div/a[2]').click()
        random_sleep(1, 2)
    
    return


def scenario_register(driver, verbose=config.config['verbose']):
    global is_logged_in
    global current_logged_in
    global accounts

    if verbose:
        print ("ENTER REGISTER")

    if(random.random() < 0.5):
        return

    # 1. if it is login, logout first
    if is_logged_in:
        scenario_logout(driver=driver, verbose=verbose, p=1)

    # 2. if it is not login, register directly
    driver.find_element_by_xpath('/html/body/nav/div/ul/li[1]').click()
    random_sleep(1, 2)

    driver.find_element_by_xpath('/html/body/main/div/section/form/div[3]/aside/a[2]').click()
    random_sleep(1, 2)

    domain_name = ["ricci", "tao", "david", "petra", "albert", "ust", "hkust", "gmail", "yahoo", "hotmail", "hku", "cuhk"]
    domain_type = [".com", ".org", ".gov", ".edu", ".mil", ".net", ".int", ".name", ".wtf"]
    domain_location = [".hk", ".cn", ".id", ".tw", ".au", ".jp", ".uk", ".nz", ".kp", ".kr"]

    emailCharLength = random.randint(9, 12)
    passwdCharLength = random.randint(8, 15)
    email = ''.join(random.choices(string.ascii_letters + string.digits, k=emailCharLength)) + '@' + \
        domain_name[random.randint(0, len(domain_name) - 1)] + \
        domain_type[random.randint(0, len(domain_type) - 1)] + \
        domain_location[random.randint(0, len(domain_location) - 1)]
    # Usually passwords contain punctuation but not set right now because it may make the dataset noisy
    passwd = ''.join(random.choices(string.ascii_letters + string.digits, k=passwdCharLength))

    driver.find_element_by_xpath('//*[@id="userEmail"]').send_keys(email)
    driver.find_element_by_xpath('//*[@id="userPassword"]').send_keys(passwd)
    driver.find_element_by_xpath('//*[@id="userPasswordRepeat"]').send_keys(passwd)
    Select(driver.find_element_by_xpath('//*[@id="securityQuestion"]')).select_by_value('9')
    driver.find_element_by_xpath('//*[@id="securityAnswer"]').send_keys("0000")
    driver.find_element_by_xpath('//*[@id="registerButton"]').click()


    # update the json file
    new_user = {
        "pw": passwd,
        "orders": [],
        "host": email.split('@')[1]
    }

    """
    with open('accounts.json', 'w') as f:
        json.dump(accounts, f, indent=4)
    
    """
    accounts.append(email)
    firebase.put('/accounts', email.split('@')[0], new_user)
    return

def scenario_xss_searchbar_attack(driver, verbose=config.config['verbose']):
    global is_logged_in
    global current_logged_in
    global accounts

    if verbose:
        print ("ENTER XSS ATTACK1")
    
    # 1. Set logstash
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='vml1wk054.cse.ust.hk', username='root', key_filename='albert_rsa')

    random_sleep(120)

    # 2. Check if is log in
    if not is_logged_in:
        scenario_login(driver=driver, verbose=verbose)


    # 3. Attack under specific pattern
    # 3-1. generate XSS pattern
    attack = ""
    
    attackType = random.randint(0, 8)
    attackKeyWordLength = random.randint(1, 15)
    if attackType == 0:
        attackKeyWord = ""
        attack = "<IMG \"\"\"><SCRIPT>alert(\"" + attackKeyWord + "\")</SCRIPT>\">"
    elif attackType == 1:
        pass
    elif attackType == 2:
        pass
    elif attackType == 3:
        pass
    elif attackType == 4:
        pass
    elif attackType == 5:
        pass
    elif attackType == 6:
        pass
    elif attackType == 7:
        pass
    elif attackType == 8:
        pass

    
    # 3-2. attack in search bar
    return

def scenario_xss_trackorders_attack(driver, verbose=config.config['verbose']):
    global is_logged_in
    global current_logged_in
    global accounts

    if verbose:
        print ("ENTER XSS ATTACK1")
    
    # 1. Set logstash
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='vml1wk054.cse.ust.hk', username='root', key_filename='<your private key>', passphrase='<key passphrase>')
    stdin, stdout, stderr = ssh.exec_command('make xss-log')
    if verbose:
        print (stdout.readlines())
    
    sleep(120)
    ssh.close()

    # 2. Check if is log in
    if not is_logged_in:
        scenario_login(driver=driver, verbose=verbose)


    # 3. Attack under specific pattern
    # 3-1. generate XSS pattern
    attack = ""
    attackType = random.randint(0, 8)
    attackKeyWordLength = random.randint(1, 15)
    # for testing
    #if attackType == 0:
    if True:
        attackKeyWord = ""
        for i in range(attackKeyWordLength):
            attackKeyWord = attackKeyWord + ENGLISH_CHAR[random.randint(0, len(ENGLISH_CHAR)-1)]
        attack = "<IMG \"\"\"><SCRIPT>alert(\"" + attackKeyWord + "\")</SCRIPT>\">"
    elif attackType == 1:
        pass
    elif attackType == 2:
        pass
    elif attackType == 3:
        pass
    elif attackType == 4:
        pass
    elif attackType == 5:
        pass
    elif attackType == 6:
        pass
    elif attackType == 7:
        pass
    elif attackType == 8:
        pass
    
    # 3-2. attack in tracking orders
    random_sleep()
    driver.find_element_by_xpath('/html/body/nav/div/ul/li[9]/a').click()
    driver.find_element_by_xpath('//*[@id="orderId"]').send_keys(attack)
    driver.find_element_by_xpath('//*[@id="trackButton"]').click()
    random_sleep()
    driver.switch_to_alert().accept()

    #4 turn of the xxs filter
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='vml1wk054.cse.ust.hk', username='root', key_filename='<your private key>', passphrase='<key passphrase>')
    stdin, stdout, stderr = ssh.exec_command('make terminate-xss')
    
    if verbose:
        print (stdout.readlines())
    stdin, stdout, stderr = ssh.exec_command('make normal-log')

    if verbose:
        print (stdout.readlines())
    
    ssh.close()
    return

#***********************************
#add all your scenario function here
#***********************************

scenario_list = [
        scenario_login,
        scenario_logout,
        scenario_search,
        scenario_track_order,
        scenario_complain,
        scenario_checkout,
        scenario_click_product,
        scenario_contact,
        scenario_recycle,
        scenario_change_password,
        scenario_about_us,
        scenario_register
]

attack_scenario_list = [
    scenario_xss_searchbar_attack,
    scenario_xss_trackorders_attack
]
