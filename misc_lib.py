import json, re, requests
from auth_lrs import *
from types import SimpleNamespace
from base64 import b64encode

def json2py(string):
    data_obj = json.loads(string, object_hook=lambda d: SimpleNamespace(**d))
    return data_obj
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
    data_object = json2py(data_str)
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
            temp_object = json2py(temp_str)
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
                break

    return data_str
def median(l):
    half = len(l) // 2
    l.sort()
    if not len(l) % 2:
        return (l[half - 1] + l[half]) / 2.0
    return l[half]