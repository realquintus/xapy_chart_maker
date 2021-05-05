from activity_lib import *

test = ActivityCompletion("https://uppa-la-preprod.solunea.net/xapi/activities/course/4da94a34-650f-4001-ab3b-7bbb19d987b7",7)
test.mkchart()
print("Code HTML + JS: \n",test.chartjs_code)
print("La completion maximum est de: ",test.max)
print("La completion minimum est de: ",test.min)
print("La completion médiane est de: ",test.median)
print("L'utilisateur 10058019-b4cc-492a-b651-66ccf6c33af3 à complété ",test.personnal_data("10058019-b4cc-492a-b651-66ccf6c33af3")," activités")
