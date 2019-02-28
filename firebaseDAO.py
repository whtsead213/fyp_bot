#import requests
from datetime import datetime
from firebase import firebase

class FirebaseDAO():
    def __init__(self, port, actionType):
        self.port = port
        self.actionType = actionType
        self.firebase = firebase.FirebaseApplication("https://hkust-fyp-ricwta01.firebaseio.com/", None)


    def append_accounts(self):
        if self.firebase.get("/accounts/" + str(self.port), None):
            return [key for key in self.firebase.get("/accounts/" + str(self.port), None).keys()]
        return []


    def firebase_get(self, item, key=None):
        return self.firebase.get(item, key)


    def firebase_put(self, item, key, value=None):
        self.firebase.put(item, key, value)
        return


    def get_account(self, email):
        return self.firebase.get("/accounts/" + str(self.port), email)


    def set_account(self, email, account):
        self.firebase.put("/accounts/" + str(self.port), email, account)
        return


    def delete_account(self, account_name=None):
        self.firebase.delete("/accounts/" + str(self.port), account_name)
        return


    def get_order(self, email):
        return self.firebase.get("/accounts/" + str(self.port) + "/" + email, 'orders')


    def set_order(self, email, order):
        self.firebase.put("/accounts/" + str(self.port) + "/" + email, 'orders', order)
        return


    def get_passwd(self, email):
        return self.firebase.get("/accounts/" + str(self.port) + "/" + email, 'pw')


    def set_passwd(self, email, password):
        self.firebase.put("/accounts/" + str(self.port) + "/" + email, 'pw', password)
        return


    def normal_record(self, normal_scenario, access_time, creater):
        # 1. Update the total normal count
        normal_count = self.firebase.get('/actions/normal', 'count')
        if normal_count:
            normal_count += 1
            self.firebase.put('/actions/normal', 'count', normal_count)
        else:
            normal_count = 1
            self.firebase.put('/actions/normal', 'count', normal_count)

        # 2. Record account detail
        normal = {
            "number": normal_count,
            "scenario": normal_scenario,
            "creater": creater,
            "access_time": access_time,
            "record_time": str(datetime.now())
        }

        self.firebase.put('/actions/normal/actions', str(normal_count), normal)


    def attack_record(self, attack_type=None, attack_scenario=None, attack_time=None, attacker=None):
        if attack_type == None or attack_scenario == None:
            return

        # 1. Update the total attack count
        attack_count = self.firebase.get('/actions/attacks/' + attack_type, 'count')
        if attack_count:
            attack_count += 1
            self.firebase.put('/actions/attacks/' + attack_type, 'count', attack_count)
        else:
            attack_count = 1
            self.firebase.put('/actions/attacks/' + attack_type, 'count', attack_count)

        # 2. Record account detail
        attack = {
            "number": attack_count,
            "type": attack_type,
            "scenario": attack_scenario,
            "attacker": attacker,
            "attack_time": attack_time,
            "record_time": str(datetime.now())
        }

        self.firebase.put('/actions/attacks/' + attack_type + "/attacks", str(attack_count), attack)
