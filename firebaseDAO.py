import requests
from datetime import datetime
from firebase import firebase

#firebase = firebase.FirebaseApplication('https://ml-sec-fyp.firebaseio.com', None)
firebase = firebase.FirebaseApplication('https://hkust-fyp-ricwta01.firebaseio.com/', None)


def append_accounts():
    if firebase.get('/accounts', None):
        return [key for key in firebase.get('/accounts', None).keys()]
    return []


def firebase_get(item=None, key=None):
    if item == None:
        return None
    
    return firebase.get(item, key)


def firebase_put(item=None, key=None, value=None):
    if item == None or key == None:
        return
    
    firebase.put(item, key, value)
    return


def get_account(email):
    return firebase.get('/accounts', email)


def set_account(email, account):
    firebase.put('/accounts', email, account)
    return


def delete_account(account_name=None):
    firebase.delete('/accounts', account_name)
    return


def get_order(email):
    return firebase.get('/accounts/' + email, 'orders')


def set_order(email, order):
    firebase.put('/accounts/' + email, 'orders', order)
    return


def get_passwd(email):
    return firebase.get('/accounts/' + email, 'pw')


def set_passwd(email, password):
    firebase.put('/accounts/' + email, 'pw', password)
    return


def normal_record(normal_scenario, access_time, creater):
    # 1. Update the total normal count
    normal_count = firebase.get('/attacks/normal', 'count')
    if normal_count:
        normal_count += 1
        firebase.put('/attacks/normal', 'count', normal_count)
    else:
        normal_count = 1
        firebase.put('/attacks/normal', 'count', normal_count)

    # 2. Record account detail
    normal = {
        "number": normal_count,
        "scenario": normal_scenario,
        "creater": creater,
        "access_time": access_time,
        "record_time": str(datetime.now())
    }

    firebase.put('/attacks/normal/actions', str(normal_count), normal)


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
        "record_time": str(datetime.now())
    }

    firebase.put('/attacks/' + attack_type + "/attacks", str(attack_count), attack)
