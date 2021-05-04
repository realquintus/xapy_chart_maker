from misc_lib import *
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