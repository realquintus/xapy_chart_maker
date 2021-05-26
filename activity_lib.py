from misc_lib import *
from statistics import median
import os,sys

class ActivityCompletion:

    def __init__(self, activity_id, completion_needed):
        # Initialize default variables
        self.activity_id = activity_id
        self.completion_needed = completion_needed
        self.registered = 0
        self.completed = 0
        self.in_progress = 0
        self.not_started = 0
        self.max = 0
        self.min = 0
        self.median = 0
        self.chartjs_code = ""
        self.processed = False
        self.html_tab = ""
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

                # Check if the user has between 1 and completion_needed completed activity. Check also if it is the last JSON package
                if i == statements_list[-1] and learners_completed[learners_list.index(learner)] != 0 and learners_completed[learners_list.index(learner)] < self.completion_needed:
                    self.in_progress += 1

            # Check if the user has as enought activity completed
            if learners_completed[learners_list.index(learner)] >= self.completion_needed:
                self.completed += 1

        self.not_started = self.registered - self.in_progress - self.completed
        self.processed = True # Variable that tell that the object has been processed by this method
        self.max = max(learners_completed)
        self.min = min(learners_completed)
        self.median = median(learners_completed)
        self.learners_list = learners_list
        self.learner_completed = learners_completed

        return 0
    def mkchart(self):

        # Check that the object has been processed by process() method
        if not self.processed:
            self.process()

        # Open activity_completion.example which is the HTML and JS of the chartjs for activity_completion
        dirname = os.path.dirname(sys.argv[0])
        if dirname == "":
            dirname = "."
        file = open("{}/code_examples/activity_completion.example".format(dirname))
        # String to insert into the file (Containing the data)
        string = str(self.completed) + "," + str(self.in_progress) + "," + str(self.not_started)
        # Replace "&" (Which is a marker for data in the file) by the previous string
        self.chartjs_code = re.sub("&",string,file.read())

        return 0
    def personal_data(self, learner_id):
        return self.learner_completed[self.learners_list.index(learner_id)]
    def mktab(self, learner_id=""):
        # Check that the object has been processed by process() method
        if not self.processed:
            self.process()

        # Open activity_completion_table.example
        dirname=os.path.dirname(sys.argv[0])
        if dirname == "":
            dirname = "."
        file = open("{}/code_examples/activity_completion_table.example".format(dirname))
        # Insert data in the code then store it in html_tab
        self.html_tab = re.sub("&min_compl&",str(self.min),re.sub("&max_compl&",str(self.max),re.sub("&med_compl&",str(self.median),file.read())))
        # Check learner_id is filled in
        if learner_id == "":
            # Remove the "Personnel" line
            self.html_tab = re.sub("&perso_compl&\n","",re.sub(".*Personnel.*\n","",self.html_tab))
        else:
            # Create string that will be add to code, containing personal data
            string = "\t<td>" + str(self.personal_data(learner_id)) + "</td>"
            # Insert string to code
            self.html_tab = re.sub("&perso_compl&", string, self.html_tab)
        return 0