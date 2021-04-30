import json, re, requests
from auth_lrs import *
from types import SimpleNamespace
from base64 import b64encode

def query_lrs():
    user = user_lrs()
    password = password_lrs()
    endpoint = endpoint_lrs()
    xapi_req = endpoint + "statements?verb=https://w3id.org/xapi/adl/verbs/logged-in"
    headers = {
        "Authorization": "Basic {}".format(
            b64encode(bytes(f"{user}:{password}", "utf-8")).decode("ascii")
        ),
        "X-Experience-API-Version": "1.0.0"
    }
    data_str = requests.get(xapi_req, headers=headers).text
    data_object = json.loads(data_str, object_hook=lambda d: SimpleNamespace(**d))
    more_url = data_object.more
    data_str = re.sub(",\"more.*}", "}", data_str)
    count = 0
    while more_url:
        count += 1
        data_str = data_str[:-1] + ","
        temp_str = requests.get(more_url, headers=headers).text
        temp_object = json.loads(temp_str, object_hook=lambda d: SimpleNamespace(**d))
        temp_str = re.sub(",\"more.*}","}",temp_str)
        temp_str = re.sub("statements", "statements-{}".format(count), temp_str)
        temp_str = temp_str[1:]
        data_str += temp_str
        if hasattr(temp_object, "more"):
            more_url = temp_object.more
        else:
            more_url = ""
    return data_str
data = json.loads(query_lrs(), object_hook=lambda d: SimpleNamespace(**d))
print(len(data.statements))
#print(query_lrs())
#json.loads(query_lrs(), object_hook=lambda d: SimpleNamespace(**d))
#data_str=''
# JSON file to python object
#with open('test__multiple_data.txt', 'r') as file:
#    for i in file:
#        if re.search("^}",i):
#            data_str += i.replace(' ','')
#        else:
#            data_str += i.replace('\n', '').replace(' ','')
#    print(data_str)
   # data = json.load(file, object_hook=lambda d: SimpleNamespace(**d))
        

#print(data.id)
