import requests
import json

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
        sign_source = str(getattr(self, "url_to_add") + str({"request" : query_token}).replace("'", "\"") + getattr(self, "api_key")).replace(" ", "")
        m = hashlib.sha256(sign_source.encode())
        self.__dict__.update({"Signature": base64.b64encode(m.digest()).decode("utf-8")})

    def ParamsInput(self, list_of_params):
        self.CalcSign(list_of_params)
        query_token = {}
        for x in list_of_params:
            query_token.update({x: getattr(self, x)})
        return query_token

current_command = "/account/list"

new_qeury = Query({"url_to_add" : current_command})

request_token.update({"request" : new_qeury.ParamsInput(commands_pull[current_command])})

post = requests.post(url=(api_address + getattr(new_qeury, "url_to_add")), data=json.dumps(request_token), headers={'Content-type': 'application/json'})
print("Platron счета:")
for i in json.loads(post.content)["response"].get("AccountList"):
    print(i)