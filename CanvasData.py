import json
import requests
import html2text

def grab_canvas_data():

    url = "https://asu.instructure.com/api/v1/courses/18732/assignments?per_page=200"

    headers = {"Authorization": "Bearer " + "7236~vh5XQQveDqwkvzPvhzsK9IivIdSmUDKY3FarvXAiY0xUpeCGhFmXkjKzMu67yYcc"}
    response = requests.get(url, headers = headers)

    data = json.loads(response.text)

    #for grades only
    url2 = "https://asu.instructure.com/api/v1/courses/18732/gradebook_history/feed?per_page=200"
    response2 = requests.get(url2, headers = headers)
    data2 = json.loads(response2.text)

    assignments = []
    users = []

    for dictionary in data:
        for dictionary2 in data2:
            ## assignment, score, total, module
            newEntry = {}
            newEntry["user_id"] = None
            newEntry["score"] = None
            newEntry["total"] = 0

            if dictionary["name"]:
                newEntry["assignment"] = dictionary["name"]

            if dictionary["id"]:
                newEntry["assignment_id"] = dictionary["id"]
                if dictionary2["assignment_id"] == dictionary["id"]:
                    newEntry["score"] = dictionary2["current_grade"]

                    if dictionary2["user_id"]:
                        if dictionary2["user_id"] not in users:
                            users.append(dictionary2["user_id"])
                        newEntry["user_id"] = dictionary2["user_id"]

            if dictionary["points_possible"]:
                newEntry['total'] = dictionary["points_possible"]

            if dictionary["position"]:
                newEntry["module"] = dictionary["position"]

            if newEntry["total"] != 0 and newEntry["score"] != None and newEntry["user_id"] != None:
                assignments.append(newEntry)

    return (assignments, users)
