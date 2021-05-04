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
class ActivityCompletion:
    def __init__(self, activity_id, completion_needed):
        # Initialize default variables
        self.activity_id = activity_id
        self.completion_needed = completion_needed
        self.registered = 0
        self.completed = 0
        self.in_progress = 0
        self.not_started = 0
        self.chartjs_code = ""
        self.processed = False
    def process(self):
        # Init var
        learners_list = []
        learners_completed = []
        # Request the users registered to the course
        learners_obj = json2py(query_lrs("activity={}&related_activities=true&verb=http://adlnet.gov/expapi/verbs/registered".format(self.activity_id)))
        # Make a list of JSON packages received
        statements_list = [item for item in dir(learners_obj) if '__' not in item]
        for i in statements_list: # Loop on JSON packages
            for j in range(len(vars(learners_obj)[i])): # Loop on statements
                # Add each user id to learners_list
                learners_list.append(vars(learners_obj)[i][j].actor.account.name)
                learners_completed.append(0)
        # Count and store registered users
        self.registered = len(learners_list)
        # Get the list of completed activities
        completed_activity = json2py(query_lrs("activity={}&related_activities=true&verb=http://adlnet.gov/expapi/verbs/completed".format(self.activity_id)))
        # List of JSON packages
        statements_list = [item for item in dir(completed_activity) if '__' not in item]
        for learner in learners_list: # Loop on users
            for i in statements_list: # Loop on JSON packages
                for j in range(len(vars(completed_activity)[i])): # Loop statements
                    if vars(completed_activity)[i][j].actor.account.name == learner: # Check if the activity has been completed by the user
                        learners_completed[learners_list.index(learner)] += 1 # Increment the completed variable in list learners_completed
                        # Check if the completed variable in list learners_completed is greater than or equal to completion_needed
                        if learners_completed[learners_list.index(learner)] >= self.completion_needed:
                            self.completed += 1 # Increment value of completed variable
                            break # Go out of statement loop
                # Check if the completed variable in list learners_completed is greater than or equal to completion_needed
                if learners_completed[learners_list.index(learner)] >= self.completion_needed:
                    break # Go out of JSON packages loop
                # Check if the user has more than 1 completed activity and if it is the last JSON package, in this case it mean that the user has a number of completed activities beetween 0 and completion_needed
                if i == statements_list[-1] and learners_completed[learners_list.index(learner)] != 0:
                    self.in_progress += 1
        self.not_started = self.registered - self.in_progress - self.completed
        self.processed = True # Variable that tell that the object has been processed by this method
        return 0
    def mkchart(self, activity_id="", completion_needed=0):
        # Check that the object has been processed by process() method
        if not self.processed:
            self.process()
        # Open activity_completion.example which is the HTML and JS of the chartjs for activity_completion
        file = open("./chartjs_examples/activity_completion.example")
        # String to insert into the file (Containing the data)
        string = str(self.completed) + "," + str(self.in_progress) + "," + str(self.not_started)
        # Replace "&" (Which is a marker for data in the file) by the previous string
        self.chartjs_code = re.sub("&",string,file.read())
        return 0
test = ActivityCompletion("https://uppa-la-preprod.solunea.net/xapi/activities/course/4da94a34-650f-4001-ab3b-7bbb19d987b7",7)
test.mkchart()
print(test.chartjs_code)