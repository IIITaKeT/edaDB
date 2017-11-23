import requests
import json
import datetime

api_address = "https://api.platron.pro/v1.0"
request_token = {"request" : {}}
commands_pull = {
    "/user/info" : ["Login", "UserInfoIdentity", "UserId", "Signature"],
    "/account/list" : ["Login", "Signature"],
    "/report/financial" : ["Login", "AccountId", "StartDate", "EndDate", "Signature"],
    "/report/transaction_list" : ["AccountId", "StartDate", "EndDate", "Login", "Signature"]
}

class Query:
    Login = ""
    api_key = ""

    def __init__(self, data):
        for key in data.keys():
            self.__dict__.update({key : data.get(key)})

    def CalcSign(self, list_of_params):
        import hashlib, base64
        query_token = {}
        for x in list_of_params:
            if x != "Signature":
                query_token.update({x : getattr(self, x)})
        sign_source = str(getattr(self, "url_to_add") + str({"request" : query_token}).replace("'", "\"") + getattr(self, "api_key")).replace(": ",":").replace(", ",",")
        m = hashlib.sha256(sign_source.encode())
        self.__dict__.update({"Signature": base64.b64encode(m.digest()).decode("utf-8")})

    def ParamsInput(self, list_of_params):
        self.CalcSign(list_of_params)
        query_token = {}
        for x in list_of_params:
            query_token.update({x: getattr(self, x)})
        return query_token

current_command = "/report/transaction_list"
id_list = ['42', '43', '44']
StartDate = datetime.datetime(2017,9,1).strftime("%Y.%m.%d %H:%M:%S")
EndDate = datetime.datetime(2017,11,20,23,59,59).strftime("%Y.%m.%d %H:%M:%S")

with open("transactions.txt", 'w') as file:
    for count, acc_id in enumerate(id_list):
        new_qeury = Query({"url_to_add" : current_command, "AccountId" : acc_id, "StartDate": StartDate, "EndDate": EndDate})
        request_token.update({"request" : new_qeury.ParamsInput(commands_pull[current_command])})

        post = requests.post(url=(api_address + getattr(new_qeury, "url_to_add")), data=json.dumps(request_token), headers={'Content-type': 'application/json'})
        head = json.loads(post.content)["response"].get("TransactionList")
        if count == 0:
            file.write("\t".join([str(k) for k in head[0].keys()]) + "\tAccountId\n")
        for i in json.loads(post.content)["response"].get("TransactionList"):
            if i['TypeTransactionStatus'] == 40:
                # user_info = "/user/info"
                # user_finder = Query({"url_to_add" : user_info, "UserId" : str(i['UserId']), "UserInfoIdentity": i['TypePaymentMethod']})
                # request_token.update({"request": user_finder.ParamsInput(commands_pull[user_info])})
                # post_user = requests.post(url=(api_address + getattr(user_finder, "url_to_add")), data=json.dumps(request_token),
                #                      headers={'Content-type': 'application/json'})
                i.update({"Amount" : round(i["Amount"] - i["Commission"],2), "AccountId": acc_id})
                file.write("\t".join([str(k) for k in i.values()]) + "\n")