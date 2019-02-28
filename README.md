# Fyp_bot
A bot to access owasp juice shop 

**Extract the chromedrive.exe according to your os in the chromedrivers directory**

Please define function for any scenario in **scerario.py** following same pattern as the **scenario_contact()**. Also, add the scenario function name into the **scenario_list** in **scenario.py**.

How to use: 

**random mode**

```python bot.py -r1 5```

-r1 to -r6 are using different port to create normal logs
randomly pick a scenario 5 times        
    
or

**custom mode**
    
```python bot.py -c1 1 2 3 2 1 0```
same here, -c1 to -c6 are using different port to create normal logs



**attack mode**
    
```python bot.py -a xss 0```
-a flag mean attack
xss specifys the attack type, and 1 means the first attack in the attack list of the specific attack


**attack type**
***DOS***
```scenario_server_random_sleep_attack```
***Error Attack***
```scenario_error_message_login_with_single_quote_attack```
***Tampering Attack***
```scenario_link_tampering```
***XXE Attack***
```scenario_xxe_retrieve_passwd_attack```
***File Upload Attack***
```scenario_upload_bigger_file```
```scenario_upload_non_pdf_file```
***SiteVisitingAttack***
```scenario_redirect1_attack```
```scenario_redirect2_attack```
```scenario_find_easter_egg_attack```
```scenario_access_signature_file_attack```
```scenario_undefine_language_attack```
***SQL Injection Attack***
```scenario_admin_login_without_passwd_attack```
```scenario_user_login_without_passwd_attack```
```scenario_retrieve_user_credentials_attack```
```scenario_sql_login_attack```
***XSS Attack***
```scenario_xss_trackorders_attack```
```scenario_xss_searchbar_attack```
```scenario_xss_user_register_attack```
```scenario_xss_contact_attack```


You can also change the sleep duration and verbose in **config.py**
