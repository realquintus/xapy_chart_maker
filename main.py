from teacher_lib import *

test = ActivityCompletion("https://uppa-la-preprod.solunea.net/xapi/activities/course/4da94a34-650f-4001-ab3b-7bbb19d987b7",7)
test.mkchart()
print(test.chartjs_code)
