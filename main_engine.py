import json, re, requests
from auth_lrs import *
from types import SimpleNamespace
from base64 import b64encode

def query_lrs(request):
    # Init var
    user = user_lrs()
    password = password_lrs()
    endpoint = endpoint_lrs()
    xapi_req = endpoint + "statements?" + request
    # Header variable contain informations for basic auth
    # "X-Experience-API-Version": "1.0.0" is a header asked by the server to accept request, may not be needed on every LRS
    headers = {
        "Authorization": "Basic {}".format(
            b64encode(bytes(f"{user}:{password}", "utf-8")).decode("ascii")
        ),
        "X-Experience-API-Version": "1.0.0"
    }
    # Storing the return of request
    data_str = requests.get(xapi_req, headers=headers).text
    # Turning JSON string received into python object
    data_object = json.loads(data_str, object_hook=lambda d: SimpleNamespace(**d))
    # Rename the JSON object statements0 to avoid conflict with the objects that will be get after
    data_str = re.sub("statements", "statements0", data_str)

    # Checking if data_object has "more" attribute, this attribute is part of XAPI protocol and means that the rest of the data may be requested with the given link
    if hasattr(data_object, "more"):
        # Storing the "more" url
        more_url = data_object.more + "&" + request
        # Remove the "more" part from the string
        data_str = re.sub(",\"more.*}", "}", data_str)
        # Variable that store the number of JSON objects received
        count = 0
        # Loop as long as the received object has a "more" attribute
        while more_url:
            count += 1
            # Request to the "more" url
            temp_str = requests.get(more_url, headers=headers).text
            # Go out of loop if empty answer from LRS
            # Due to strange behaviour some LRS might give more_url even if all data has been sent
            if temp_str == '{"statements":[]}':
                break
            # JSON object to python object
            temp_object = json.loads(temp_str, object_hook=lambda d: SimpleNamespace(**d))
            # Remove the "more" part from the string
            temp_str = re.sub(",\"more.*}","}",temp_str)
            # Rename the received object by adding the object number
            temp_str = re.sub("statements", "statements{}".format(count), temp_str)
            # Remove the first character wich is "{"
            temp_str = temp_str[1:]
            # Remove the final "}" that mean the end of the JSON string. Replace it by "," to add the remaining data
            data_str = data_str[:-1] + ","
            # Add the received data to the return string
            data_str += temp_str
            # Checking if received object has "more" attribute
            if hasattr(temp_object, "more"):
                # New url
                more_url = temp_object.more + "&" + request
            else:
                # Make more_url variable empty to go out of loop
                more_url = ""
    return data_str
def activity_completion(data_obj, activity_id):
    # Init var
    learners = 100
    completed = 0
    in_progress = 0
    # Get all attribute of data_obj and filter to remove default attr (Circle by __)
    statements_list = [item for item in dir(data_obj) if '__' not in item]
    for i in statements_list: # Loop on statements packages
        for j in range(len(vars(data_obj)[i])): # Loop on statements
            # Check if the data is what we want to count
            # vars(data_obj)[i] refers to the attribute i of data_obj which is a list of statements
            if vars(data_obj)[i][j].verb.id == activity_id:
                completed += 1
    return completed
data_str = query_lrs("verb=http://adlnet.gov/expapi/verbs/completed")
data_obj = json.loads(data_str, object_hook=lambda d: SimpleNamespace(**d))
#print(activity_completion(data_obj, "http://adlnet.gov/expapi/verbs/completed"))