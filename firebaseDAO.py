import time
import requests
from firebase import firebase

#firebase = firebase.FirebaseApplication('https://ml-sec-fyp.firebaseio.com', None)
firebase = firebase.FirebaseApplication('https://hkust-fyp-ricwta01.firebaseio.com/', None)
def attack_record(attack_type=None, attack_scenario=None, attack_time=None, attacker=None):
    if attack_type == None or attack_scenario == None:
        return
    
    # 1. Update the total attack count
    attack_count = firebase.get('/attacks/' + attack_type, 'count')
    if attack_count:
        attack_count += 1
        firebase.put('/attacks/' + attack_type, 'count', attack_count)
    else:
        attack_count = 1
        firebase.put('/attacks/' + attack_type, 'count', attack_count)

    # 2. Record account detail
    attack = {
        "number": attack_count,
        "type": attack_type,
        "scenario": attack_scenario,
        "attacker": attacker,
        "attack_time": attack_time,
        "record_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }

    firebase.put('/attacks/' + attack_type + "/attacks", str(attack_count), attack)
