# from selenium import webdriver
import time
import json
import string
import random
import base64
import datetime
import requests
import paramiko
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from config import config, good_comments, bad_comments, search_keyword, domain_name, domain_type, domain_location, HONK_KOND_DIST, HONG_KONG_ADDR


def random_sleep(min=config['sleep_min'],max=config['sleep_max'],verbose=config['verbose']):
    assert(min<=max)
    sleep_time = random.randint(min,max)
    if verbose:
        print('sleep for %d seconds' %(sleep_time))
    sleep(sleep_time)


def random_comment(index, verbose=config['verbose']):
    '''
    Choose a random comment from good / bad comment list depends on the input index
    '''
    if index >= 3:
        i = random.choice(range(len(good_comments)))
        return good_comments[i]
    else:
        i = random.choice(range(len(bad_comments)))
        return bad_comments[i]


def random_return_home(driver, prob=config['return_home_probability'], verbose=config['verbose']):
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


def comment_product(driver, prob=config["comment_product_probability"], verbose=config['verbose']):
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





class Action():
    def __init__(self, driver, actionType, firebaseDAO):
        if config['verbose']:
            print ("An action is created")
        
        self.driver = driver
        self.actionType = actionType
        self.firebaseDAO = firebaseDAO
        
        self.is_logged_in = False
        self.current_email = None
        self.cart_is_filled = False
        self.current_logged_in = None
        self.verbose = config['verbose']
        self.accounts = firebaseDAO.append_accounts()

        self.scenario_list = [
            self.scenario_login,
            self.scenario_logout,
            self.scenario_search,
            self.scenario_track_order,
            self.scenario_complain,
            self.scenario_checkout,
            self.scenario_click_product,
            self.scenario_contact,
            self.scenario_recycle,
            self.scenario_change_password,
            self.scenario_about_us,
            self.scenario_register
        ]


    def scenario_click_product(self, page="home"):
        def add_product_to_cart(product_id=None):

            min_add = config["add_product_to_cart_min"]
            max_add = config["add_product_to_cart_max"]
            r = random.randint(min_add,max_add)

            for i in range(r):
            #i dont know how to find all product in a page so i simply select the top one, please improve it if u know
                try:
                    random_sleep(1,2)
                    if product_id == None:
                        self.driver.find_element_by_xpath('/html/body/main/div/section/table/tbody/tr[3]/td[5]/div/a[2]').click()
                    else :
                        #print('this should appear')
                        product = '/html/body/main/div/section/table/tbody/tr[' + str(product_id) +']/td[5]/div/a[2]'
                        #print(product)
                        #print(product == '/html/body/main/div/section/table/tbody/tr[2]/td[5]/div/a[2]')
                        self.driver.find_element_by_xpath(product).click()
                    self.cart_is_filled = True
                
                except NoSuchElementException:
                    pass
            
            if(random.random() < 0.3):
                self.scenario_checkout(self.driver)

            return

        #driver.get(config.config['url'])
        if(random.random() < 0.3):
            self.scenario_login(self.driver)
        
        max_clicks = config['home_product_clicks_max']
        min_clicks = config['home_product_clicks_min']
        clicks = random.randint(min_clicks,max_clicks)
        if self.verbose:
            print(clicks)
        
        for i in range(clicks):
            try:
                random_sleep(2,3)
                if page == "home":
                    product_id = random.randint(2,29)

                elif page == "search":
                     product_id = random.randint(2,2)
                
                product = "/html/body/main/div/section/table/tbody/tr[" + str(product_id) + "]/td[5]/div/a[1]"
                self.driver.find_element_by_xpath(product).click()
                self.comment_product(self.driver)
                
                if self.is_logged_in:
                    random_prob = random.random()
                    if random_prob <= config['add_product_to_cart_prob']:
                        add_product_to_cart(self.driver, product_id=product_id)
            
            except NoSuchElementException:
                pass

        return


    def scenario_contact(self, contant=None):
        '''
        This is a function that you can access the juiceshop and go to the comment page automatically
        You can follow this function as template to create more scenario
        Basically, you inspect the html element with chrome dev tool and copy the XPATH to the driver.find_element_by_xpath() function
        Then, follow by click() and send_keys() depends on what action you wanna do to that html element
        Also, use the random_sleep() function to create some random delay to make this natural
        '''
        if(random.random() < 0.2):
            return

        random_sleep()

        # 1. click contact us 
        self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[7]/a').click() 
        random_sleep()
        random_return_home(self.driver)

        # 2. leave comment, sample comments are in config.py
        #give good / bad comment according to star
        star = random.randint(1,5)
        if contant:
            self.driver.find_element_by_xpath('//*[@id="feedbackComment"]').send_keys(contant)
        else:
            self.driver.find_element_by_xpath('//*[@id="feedbackComment"]').send_keys(random_comment(star))
        random_sleep()

        # 3. handle star
        if self.verbose:
            print(star)
        self.driver.find_element_by_xpath("/html/body/main/div/section/div/form/div[4]/div[3]/div/span/span/i[" + str(star) + "]").click()
        random_sleep()
        random_return_home(self.driver)

        # 4. handle captcha
        captcha = self.driver.find_element_by_xpath('//*[@id="captcha"]').text
        ans = eval(captcha)
        if self.verbose:
            print(captcha)
            print(ans)
        self.driver.find_element_by_xpath('/html/body/main/div/section/div/form/div[4]/div[4]/div/input').send_keys(ans)
        random_sleep()

        # 5. send
        self.driver.find_element_by_xpath('//*[@id="submitButton"]').click()

        return


    def scenario_login(self):
        random_sleep()
        
        if self.is_logged_in:
            return

        else:
            self.accounts = self.firebaseDAO.append_accounts()
            
            if(len(self.accounts) == 0):
                self.scenario_register()
                random_sleep()
            self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[1]').click()
            random_sleep(1, 2)

            # Choose a user credential randomly
            uid = random.randint(0, len(self.accounts) - 1)
            self.current_email = self.accounts[uid]
            acc = self.firebaseDAO.get_account(self.current_email)
            passwd = acc['pw']
            email = self.current_email + '@' + acc['host']

            self.current_logged_in = uid

            self.driver.find_element_by_xpath('//*[@id="userEmail"]').send_keys(email)
            self.driver.find_element_by_xpath('//*[@id="userPassword"]').send_keys(passwd)
            self.driver.find_element_by_xpath('//*[@id="loginButton"]').click()
            
            self.is_logged_in = True
            
            if self.verbose:
                print(email + 'is logged in')
            
            random_sleep(2, 3)
            
            return


    def scenario_logout(self, p=0.8):
        if(random.random() < (1-p)):
            return
        random_sleep(2, 3)

        if self.is_logged_in:
            try:
                self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[2]/a/span').click()
                self.is_logged_in = False
                self.current_logged_in = None
                self.cart_is_filled = False
                
                if self.verbose:
                    print('logged out')

            except:
                pass
            
            random_sleep(2, 3)
        
        return


    def scenario_search(self):
        random_sleep()

        if(random.random() < 0.3):
            self.scenario_login()

        r = random.randint(0, len(config.search_keyword) - 1)
        self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[4]/form/div/input').clear()
        self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[4]/form/div/input').send_keys(search_keyword[r])
        random_sleep()
        self.driver.find_element_by_xpath('//*[@id="searchButton"]').click()
        self.scenario_click_product(page='search')

        return


    def scenario_checkout(self):
        if self.is_logged_in:
            random_sleep(2,3)
            self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[5]/a').click()
            
            if(not self.cart_is_filled):
                self.driver.find_element_by_xpath('/html/body/nav/div/div/a[2]/span').click() 
                random_sleep()
                return
            
            self.driver.find_element_by_xpath('//*[@id="checkoutButton"]').click()

            # wait 7 sec to ensure the browser jumped to order pdf
            sleep(7) 
            order = self.driver.current_url[39:-4]
            print(order)
            prev_order = self.firebaseDAO.get_order(self.current_email)
            if(prev_order is None):
                orders = {order: True}
                self.firebaseDAO.set_order(self.current_email, orders)
            
            else:
                prev_order[order] = True
                self.firebaseDAO.set_order(self.current_email, prev_order)
        
            
            self.driver.get(config['url'])
        
        return


    def scenario_track_order(self):
        if self.is_logged_in:
            random_sleep()
            self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[9]/a').click()
            
            try:
                orders = self.firebaseDAO.get_order(self.current_email)
                if(orders is None):
                    self.driver.find_element_by_xpath('/html/body/nav/div/div/a[2]/span').click() 
                    random_sleep()
                    return

                else:
                    order = random.choice(list(orders.keys()))
                
                self.driver.find_element_by_xpath('//*[@id="orderId"]').send_keys(order)
                self.driver.find_element_by_xpath('//*[@id="trackButton"]').click()
            
            except IndexError:
                pass
        
        return


    def scenario_complain(self):
        if(random.random() < 0.2):
            return

        random_sleep()
        self.driver.find_element_by_xpath('//*[@id="complaintMessage"]').send_keys(random_comment(2))
        self.driver.find_element_by_xpath('//*[@id="submitButton"]').click()
        # skip the upload invoice, whatever


    def scenario_recycle(self):
        # 1. Check if is log in
        if not self.is_logged_in:
            self.scenario_login()

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

        if self.verbose:
            print ("Address: " + str(random_address))

        self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[8]').click()
        random_sleep(1, 2)
        self.driver.find_element_by_xpath('//*[@id="recycleQuantity"]').send_keys(random_quan)
        random_sleep(1, 2)
        self.driver.find_element_by_xpath('//*[@id="recycleAddress"]').send_keys(random_address)

        if (random_quan > 100) and (random.randint(0, 1) == 1):
            self.driver.find_element_by_xpath('//*[@id="isPickup"]').click()

            pick_up_date = datetime.datetime.now() + datetime.timedelta(days=random.randint(0, 30))

            if self.verbose:
                print ("00" + str(pick_up_date.year) + str(pick_up_date.month) + str(pick_up_date.day))

            random_sleep(1, 2)
            self.driver.find_element_by_xpath('//*[@id="recyclePickupDate"]').send_keys("00" + str(pick_up_date.year) + str(pick_up_date.month) + str(pick_up_date.day))

        self.driver.find_element_by_xpath('//*[@id="submitButton"]').click()

        return


    def scenario_change_password(self):
        if(random.random() < 0.8):
            return
        
        # 1. Check if is log in
        if not self.is_logged_in:
            self.scenario_login()

        # 2. change the password with the current time and update the json file
        passwdCharLength = random.randint(8, 15)
        old_password = self.firebaseDAO.get_passwd(self.current_email)
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=passwdCharLength))

        self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[6]').click()
        random_sleep(1, 2)

        # input the new password and update
        self.driver.find_element_by_xpath('//*[@id="currentPassword"]').send_keys(old_password)
        random_sleep(1, 2)
        self.driver.find_element_by_xpath('//*[@id="newPassword"]').send_keys(new_password)
        self.driver.find_element_by_xpath('//*[@id="newPasswordRepeat"]').send_keys(new_password)
        random_sleep(1, 2)
        self.driver.find_element_by_xpath('//*[@id="changeButton"]').click()

        # Update data
        self.firebaseDAO.set_passwd(self.current_email, new_password)

        self.scenario_logout(p=1)
        
        return


    def scenario_about_us(self):
        if(random.random() < 0.4):
            return

        self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[12]').click()
        random_sleep(1, 2)

        row_time = random.randint(0, 10)

        if self.verbose:
            print ("row time = " + str(row_time))

        for i in range(0, row_time):
            random_left_right = random.randint(0, 1)
            if random_left_right == 0:
                self.driver.find_element_by_xpath('/html/body/main/div/div/section[1]/div/div/a[1]').click()
            else:
                self.driver.find_element_by_xpath('/html/body/main/div/div/section[1]/div/div/a[2]').click()
            random_sleep(1, 2)

        return


    def scenario_register(self, login_after_register=False):
        if self.verbose:
            print ("ENTER REGISTER")

        if(random.random() < 0.5):
            return

        # 1. if it is login, logout first
        if self.is_logged_in:
            self.scenario_logout(p=1)

        # 2. if it is not login, register directly
        self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[1]').click()
        random_sleep(1, 2)

        self.driver.find_element_by_xpath('/html/body/main/div/section/form/div[3]/aside/a[2]').click()
        random_sleep(1, 2)

        emailCharLength = random.randint(9, 12)
        passwdCharLength = random.randint(8, 15)
        email = ''.join(random.choices(string.ascii_letters + string.digits, k=emailCharLength)) + '@' + \
            domain_name[random.randint(0, len(domain_name) - 1)] + \
            domain_type[random.randint(0, len(domain_type) - 1)] + \
            domain_location[random.randint(0, len(domain_location) - 1)]
        # Usually passwords contain punctuation but not set right now because it may make the dataset noisy
        passwd = ''.join(random.choices(string.ascii_letters + string.digits, k=passwdCharLength))

        self.driver.find_element_by_xpath('//*[@id="userEmail"]').send_keys(email)
        self.driver.find_element_by_xpath('//*[@id="userPassword"]').send_keys(passwd)
        self.driver.find_element_by_xpath('//*[@id="userPasswordRepeat"]').send_keys(passwd)
        Select(self.driver.find_element_by_xpath('//*[@id="securityQuestion"]')).select_by_value('9')
        self.driver.find_element_by_xpath('//*[@id="securityAnswer"]').send_keys("0000")
        self.driver.find_element_by_xpath('//*[@id="registerButton"]').click()


        # update the json file
        new_user = {
            "pw": passwd,
            "orders": [],
            "host": email.split('@')[1]
        }

        self.accounts.append(email)
        self.firebaseDAO.set_account(email.split('@')[0], new_user)

        if login_after_register:
            random_sleep(2, 3)
            self.driver.find_element_by_xpath('//*[@id="userEmail"]').send_keys(email)
            self.driver.find_element_by_xpath('//*[@id="userPassword"]').send_keys(passwd)
            self.driver.find_element_by_xpath('//*[@id="loginButton"]').click()

            self.is_logged_in = True
            if self.verbose:
                print(email + 'is logged in')

        return
