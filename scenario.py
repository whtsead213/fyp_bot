import config
from selenium import webdriver
import random
from time import sleep


def random_sleep(min=config.config['sleep_min'],max=config.config['sleep_max'],verbose=config.config['verbose']):
    assert(min<=max)
    sleep_time = random.randint(min,max)
    if verbose:
        print('sleep for %d seconds' %(sleep_time))
    sleep(sleep_time)

def random_comment(index='random'):
    if index == 'random':
        i = random.choice(range(len(config.comments)))
        return config.comments[i]
    else:
        assert index < len(config.comments)
        return config.comments[index]

def scenario_contact(verbose=config.config['verbose']):
    '''
    This is a function that you can access the juiceshop and go to the comment page automatically
    You can follow this function as template to create more scenario
    Basically, you inspect the html element with chrome dev tool and copy the XPATH to the driver.find_element_by_xpath() function
    Then, follow by click() and send_keys() depends on what action you wanna do to that html element
    Also, use the random_sleep() function to create some random delay to make this natural
    '''
    #initiate chrome
    driver = webdriver.Chrome('./chromedrivers/chromedriver')

    #go to main page
    driver.get(config.config['url']) # You can change this to other url if you don't want to access from main page
    random_sleep()

    #click contact us 
    driver.find_element_by_xpath('/html/body/nav/div/ul/li[7]/a/span').click() 
    random_sleep()

    #leave comment, sample comments are in config.py
    driver.find_element_by_xpath('//*[@id="feedbackComment"]').send_keys(random_comment())
    random_sleep()

    #handle star
    star = random.randint(1,5)
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