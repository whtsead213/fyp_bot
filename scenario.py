import config
# from selenium import webdriver
import random
from time import sleep

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
        random_sleep(min=10, max=20) #make it longer
       
        #send the comment
        driver.find_element_by_xpath('//*[@id="submitButton"]/span').click() 
        random_sleep()
    
    #close the product window
    driver.find_element_by_xpath('/html/body/div[1]/div/div/section/footer/button/span').click() 

def scenario_click_home_product(driver, verbose=config.config['verbose']):   
    driver.get(config.config['url'])
    max_clicks = config.config["home_product_clicks_max"]
    min_clicks = config.config["home_product_clicks_min"]
    clicks = random.randint(min_clicks,max_clicks)
    print(clicks)
    for i in range(clicks):
        random_sleep()
        product_id = random.randint(2,29) 
        product = "/html/body/main/div/section/table/tbody/tr["+str(product_id)+"]/td[5]/div/a[1]"
        driver.find_element_by_xpath(product).click()
        comment_product(driver)
    

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
    driver.get(config.config['url']) # You can change this to other url if you don't want to access from main page
    random_sleep()

    #click contact us 
    driver.find_element_by_xpath('/html/body/nav/div/ul/li[7]/a/span').click() 
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
    driver.get(config.config['url'])
    random_sleep()

    driver.find_element_by_xpath('/html/body/nav/div/ul/li[1]').click()
    random_sleep(1, 2)

    # Choose a user credential randomly
    r = random.randint(0, len(config.users) - 1)
    email = config.users[r][0]
    passwd = config.users[r][1]

    driver.find_element_by_xpath('//*[@id="userEmail"]').send_keys(email)
    driver.find_element_by_xpath('//*[@id="userPassword"]').send_keys(passwd)
    driver.find_element_by_xpath('//*[@id="loginButton"]').click()
    random_sleep(2, 3)
   

def scenario_logout(driver, verbose=config.config['verbose']):
    driver.get(config.config['url'])
    random_sleep(2, 3)

    try:
        driver.find_element_by_xpath('/html/body/nav/div/ul/li[2]').click()
    except:
        pass
    random_sleep(2, 3)

#***********************************
#add all your scenario function here
#***********************************
scenario_list = [scenario_click_home_product,scenario_contact, scenario_login, scenario_logout]
