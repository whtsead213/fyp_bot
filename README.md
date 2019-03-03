# Fyp_bot
A bot to access owasp juice shop 

## TODOs Before starting

**Extract the chromedrive.exe according to your os in the chromedrivers directory**

~~Please define function for any scenario in **scerario.py** following same pattern as the **scenario_contact()**. Also, add the scenario function name into the **scenario_list** in **scenario.py**.~~

  - Please remember to change the **user name** in the `firebaseDAO` of `bot.py`
  - Please provide some `.pdf` file **(100~200KB)** and some `.xml` file **(<100KBN)** if possible for the upload part

## Usage: 

### Normal Action

#### Random Mode

```sh
$ python bot.py -r1 5
```

  - `-r1`, `-r2`, `-r3`, `-r4`, `-r5`, and `-r6` are using different port to create normal logs
  - The second number means how many random normal scenario you want to execute

#### Custom Mode
    
```sh
$ python bot.py -c1 1 2 3 2 1 0
```
  - `-c1`, `-c2`, `-c3`, `-c4`, `-c5`, and `-c6` are using different port to create normal logs
  - The numbers following the flag means the specific normal action you want to execute

### Attack Action

#### Attack Mode
    
```sh
$ python bot.py -a xss 0
```

  - `-a` flag means attack
  - `dos`, `error`, `tampering`, `xxe`, `file_upload`, `site_visiting`, `sql`, and `xss` are the different attck types available
  - The number follows behind the attack is the scenario of the specific attack. Details of each scenario is listed in the `Attack Types` part


## Attack Types

### Attack In Use
  - Tampering Attack
  - XXE Attack
  - SQL Attack
  - XSS Attack

There are eight attack types in total

| Attack | Scenario |
| ------ | ------ |
| DOS Attack | `scenario_server_random_sleep_attack() `|
| Error Attack | `scenario_error_message_login_with_single_quote_attack` |
| Tampering Attack | `scenario_link_tampering` |
| XXE Attack | `scenario_xxe_retrieve_passwd_attack` |
| File Upload Attack | `scenario_upload_bigger_file`, `scenario_upload_non_pdf_file`|
| Site Visiting Attack | `scenario_redirect1_attack`, `scenario_redirect2_attack`, `scenario_find_easter_egg_attack`, `scenario_access_signature_file_attack`, `scenario_undefine_language_attack` |
| SQL Attack | `scenario_user_login_without_passwd_attack`, `scenario_retrieve_user_credentials_attack`, `scenario_sql_login_attack` |
| XSS Attack | `scenario_xss_trackorders_attack`, `scenario_xss_searchbar_attack`, `scenario_xss_user_register_attack`, `scenario_xss_contact_attack` |


You can also change the sleep duration and verbose in **config.py**
