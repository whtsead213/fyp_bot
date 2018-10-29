# Fyp_bot
A bot to access owasp juice shop 

**Extract the chromedrive.exe according to your os in the chromedrivers directory**

Please define function for any scenario in **scerario.py** following same pattern as the **scenario_contact()**. Also, add the scenario function name into the **scenario_list** in **scenario.py**.

How to use: 

**random mode**

```python bot.py random 5```

randomly pick a scenario 5 times        
    
or

**custom mode**
    
```python bot.py custom 1 2 3 2 1 0```

each argument is the index of the scenario
       
       
You can also change the sleep duration and verbose in **config.py**
