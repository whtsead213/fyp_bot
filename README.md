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

       
You can also change the sleep duration and verbose in **config.py**
