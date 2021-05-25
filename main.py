from activity_lib import *
from optparse import OptionParser

### Handle options ###

parser = OptionParser()
parser.add_option("-C","--activity_completion",action="store_true",dest="activity_completion",default=False,help="(Need ACTIVITY_ID) Return the code of a doughnut chart. This chart is displaying percentages of activity completion by learners.")
parser.add_option("-c","--personnal_completion",action="store_true",dest="personnal_completion",default=False,help="(Need ACTIVITY_ID and LEARNER_ID) Return tab that contain various information about activity completion, including personnal completion of learner.",)
parser.add_option("-A","--activity_id",dest="activity_id",help="Used to pass activity ID", metavar="ACTIVITY_ID")
parser.add_option("-L","--learner_id",dest="learner_id",help="Used to pass learner ID", metavar="LEARNER_ID")
parser.add_option("-N","--required_completion",dest="required_completion",help="Used to pass the minimum completion that is required for the activity to be considered completed", metavar="REQUIRED_COMPLETION")

(options,args)=parser.parse_args()

if options.activity_completion:
    if options.personnal_completion or options.activity_id is None or options.required_completion is None:
        parser.print_help()
        exit(1)
    obj = ActivityCompletion(options.activity_id, int(options.required_completion))
    obj.mkchart()
    print(obj.chartjs_code)
if options.personnal_completion:
    if options.activity_completion or options.activity_id is None or options.learner_id is None or options.required_completion is None:
        parser.print_help()
        exit(1)

#######################


#test = ActivityCompletion("https://uppa-la-preprod.solunea.net/xapi/activities/course/4da94a34-650f-4001-ab3b-7bbb19d987b7",7)
#test.mkchart()
#print("Code HTML + JS: \n",test.chartjs_code)
#print("La completion maximum est de: ",test.max)
#print("La completion minimum est de: ",test.min)
#print("La completion médiane est de: ",test.median)
#print("L'utilisateur 10058019-b4cc-492a-b651-66ccf6c33af3 à complété ",test.personnal_data("10058019-b4cc-492a-b651-66ccf6c33af3")," activités")
