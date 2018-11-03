import config
# from selenium import webdriver
import random
from time import sleep
import json
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

is_logged_in = False
accounts = None
current_logged_in = None

with open('accounts.json') as f:
    accounts = json.load(f)
    for ac in accounts:
        #print(type(ac)) #dict
        print(ac)

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
        except NoSuchElementException:
            pass

def scenario_click_product(driver, page='home', verbose=config.config['verbose']):   
    #driver.get(config.config['url'])
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
    if is_logged_in:
        return
    else:
        driver.find_element_by_xpath('/html/body/nav/div/ul/li[1]').click()
        random_sleep(1, 2)

        # Choose a user credential randomly
        uid = random.randint(0, len(accounts) - 1)
        email = accounts[uid]['id']
        passwd = accounts[uid]['pw']

        current_logged_in = uid

        driver.find_element_by_xpath('//*[@id="userEmail"]').send_keys(email)
        driver.find_element_by_xpath('//*[@id="userPassword"]').send_keys(passwd)
        driver.find_element_by_xpath('//*[@id="loginButton"]').click()
        is_logged_in = True
        if verbose:
            print(email + 'is logged in')
        random_sleep(2, 3)
   
def scenario_logout(driver, verbose=config.config['verbose']):
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
        except:
            pass
        random_sleep(2, 3)
    else:
         return

def scenario_search(driver, verbose=config.config['verbose']):
    random_sleep()

    r = random.randint(0, len(config.search_keyword) - 1)
    driver.find_element_by_xpath('/html/body/nav/div/ul/li[4]/form/div/input').clear()
    driver.find_element_by_xpath('/html/body/nav/div/ul/li[4]/form/div/input').send_keys(config.search_keyword[r])
    random_sleep()
    driver.find_element_by_xpath('//*[@id="searchButton"]').click()
    scenario_click_product(driver,page='search')
    
def scenario_checkout(driver, verbose=config.config['verbose']):
    global is_logged_in
    global current_logged_in
    global accounts
    if is_logged_in:
        random_sleep(2,3)
        driver.find_element_by_xpath('/html/body/nav/div/ul/li[5]/a').click()
        driver.find_element_by_xpath('//*[@id="checkoutButton"]').click()

        # wait 7 sec to ensure the browser jumped to order pdf
        sleep(7) 
        order = driver.current_url[39:-4]
        print(order)
        accounts[current_logged_in]['orders'].append(order)
        with open('accounts.json', 'w') as f:
            json.dump(accounts, f, indent=4)
    else:
        pass

def scenario_track_order(driver, verbose=config.config['verbose']):
    global is_logged_in
    global current_logged_in
    global accounts
    if is_logged_in:
        random_sleep()
        driver.find_element_by_xpath('/html/body/nav/div/ul/li[9]/a').click()
        try:
            order = accounts[current_logged_in]['orders'].pop()
            driver.find_element_by_xpath('//*[@id="orderId"]').send_keys(order)
            driver.find_element_by_xpath('//*[@id="trackButton"]').click()
        except IndexError:
            pass
    else:
        pass

def scenario_complain(driver, verbose=config.config['verbose']):
    random_sleep()
    driver.find_element_by_xpath('//*[@id="complaintMessage"]').send_keys(random_comment(2))
    driver.find_element_by_xpath('//*[@id="submitButton"]').click()
    # skip the upload invoice, whatever

def scenario_recycle(driver, verbose=config.config['verbose']):
    # do this if you are free and bored
    pass

def scenario_change_password(driver, verbose=config.config['verbose']):
    # do this if you are free and bored
    pass

def scenario_about_us(driver, verbose=config.config['verbose']):
    # do this if you are free and bored
    pass

def scenario_register(driver, verbose=config.config['verbose']):
    global is_logged_in
    global current_logged_in
    global accounts
    # please finish this at least
    # probably u need to register manually using raw_input() and append new user data to accounts and output to json
    # also see if it will automatically login after successfully registered. So u need to change the global variable.
    # (No, it won't)
    if verbose:
        print ("ENTER REGISTER")
    # 1. if it is login, logout first
    if is_logged_in:
        scenario_logout(driver=driver, verbose=verbose)

    # 2. if it is not login, register directly
    driver.find_element_by_xpath('/html/body/nav/div/ul/li[1]').click()
    random_sleep(1, 2)

    driver.find_element_by_xpath('/html/body/main/div/section/form/div[3]/aside/a[2]').click()
    random_sleep(1, 2)

    domain_name = ["ricci", "tao", "david", "petra", "albert", "ust", "hkust", "gmail", "yahoo", "hotmail", "hku", "cuhk"]
    domain_type = [".com", ".org", ".gov", ".edu", ".mil", ".net", ".int", ".name", ".wtf"]
    domain_location = [".hk", ".cn", ".id", ".tw", ".au", ".jp", ".uk", ".nz", ".kp", ".kr"]
    # generate fake email account using time
    import time
    current_time = str(time.time())
    email = current_time + "@" + \
        domain_name[random.randint(0,len(domain_name)-1)] + \
        domain_type[random.randint(0,len(domain_type)-1)] + \
        domain_location[random.randint(0,len(domain_location)-1)]
    passwd = current_time
    
    driver.find_element_by_xpath('//*[@id="userEmail"]').send_keys(email)
    driver.find_element_by_xpath('//*[@id="userPassword"]').send_keys(passwd)
    driver.find_element_by_xpath('//*[@id="userPasswordRepeat"]').send_keys(passwd)
    Select(driver.find_element_by_xpath('//*[@id="securityQuestion"]')).select_by_value('9')
    driver.find_element_by_xpath('//*[@id="securityAnswer"]').send_keys("0000")
    driver.find_element_by_xpath('//*[@id="registerButton"]').click()


    # update the json file
    new_user = {
        "id": email,
        "pw": passwd,
        "orders": []
    }

    accounts.append(new_user)
    with open('accounts.json', 'w') as f:
        json.dump(accounts, f, indent=4)
    
    return

#***********************************
#add all your scenario function here
#***********************************

scenario_list = [scenario_login, scenario_logout, scenario_search, scenario_track_order, scenario_complain, scenario_checkout, scenario_click_product, scenario_contact, scenario_register]
