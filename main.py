from activity_lib import *
from optparse import OptionParser

### Def options ###
parser = OptionParser()
parser.add_option("-c","--chart_completion",action="store_true",dest="chart_completion",default=False,help="(Need ACTIVITY_ID and REQUIRED_COMPLETION) Return the code of a doughnut chart. This chart is displaying percentages of activity completion by learners.")
parser.add_option("-t","--tab_completion",action="store_true",dest="tab_completion",default=False,help="(Need ACTIVITY_ID and REQUIRED_COMPLETION, LEARNER_ID is optional) Return tab that contain various information about activity completion. If LEARNER_ID is given, the tab will also return personnal completion of the learner.",)
parser.add_option("-a","--activity_id",dest="activity_id",help="Used to pass activity ID", metavar="ACTIVITY_ID")
parser.add_option("-l","--learner_id",dest="learner_id",help="Used to pass learner ID", metavar="LEARNER_ID")
parser.add_option("-n","--required_completion",dest="required_completion",help="Used to pass the minimum completion that is required for the activity to be considered completed", metavar="REQUIRED_COMPLETION")
(options,args)=parser.parse_args()
####################

### Handling options ###

# Chart block
if options.chart_completion:
    # Check if tab_completion is entered or required data are not entered
    if options.tab_completion or options.activity_id is None or options.required_completion is None:
        parser.print_help()
        exit(1)

    # Create object from ActivityCompletion class
    obj = ActivityCompletion(options.activity_id, int(options.required_completion))
    # Process the object and generate the JS code
    obj.mkchart()
    # Print JS code
    print(obj.chartjs_code)

# Table block
elif options.tab_completion:
    # Check if required data are not entered
    if options.activity_id is None or options.required_completion is None:
        parser.print_help()
        exit(1)
    # Create object from ActivityCompletion class
    obj = ActivityCompletion(options.activity_id, int(options.required_completion))
    # Check is learner_id is entered
    if options.learner_id is None:
        # Process without learner_id
        obj.mktab()
    else:
        # Process with learner_id
        obj.mktab(options.learner_id)
    # Print HTML
    print(obj.html_tab)

# Neither tab_completion nor chart_completion has been filled in
else:
    parser.print_help()
    exit(1)

########################
#test = ActivityCompletion("https://uppa-la-preprod.solunea.net/xapi/activities/course/4da94a34-650f-4001-ab3b-7bbb19d987b7",7)
#print("L'utilisateur 10058019-b4cc-492a-b651-66ccf6c33af3 à complété ",test.personnal_data("10058019-b4cc-492a-b651-66ccf6c33af3")," activités")
