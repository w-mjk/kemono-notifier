import time
import Profile
import json
import requests
import send_message
import os
from datetime import datetime

api_url = "https://kemono.cr/api"
favorites = "/v1/account/favorites"
authentication = "eyJfcGVybWFuZW50Ijp0cnVlLCJhY2NvdW50X2lkIjoxNjUxNTI4fQ.aIWIKg.yWF4o8P_ZpfXzi6QbZTM9NIdLTk"
seconds_to_sleep = 600
profile_list = []
email = None

with open("profile_list.json", "r") as current_json_file:
        if (os.path.getsize("profile_list.json") != 0):  
            current_json = json.load(current_json_file)
            for profile in current_json:
                profile_list.append(Profile.Profile(profile["name"], profile["last_imported"]))

while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current time = ", current_time)

    #Extract API information
    response = requests.get(api_url+favorites, params={"type":"artist"}, headers={"Cookie":"session="+authentication, "accept":"application/response_json"})
    try:
        response_json = response.json()
    except:
        response_json = None
    extracted_profile_list = []
            
    if (response_json != None):
        #First time execution only
        if len(profile_list) == 0:
            print("Is not appending again and again!\n")
            #Append each profile in the response_json file to the list
            for profile in response_json:
                profile_list.append(Profile.Profile(profile["name"], profile["last_imported"]))
        
        for profile in response_json:
            extracted_profile_list.append(Profile.Profile(profile["name"], profile["last_imported"]))

        #Upon change in the favorite list
        if len(profile_list) < len(extracted_profile_list):
            for i in range(len(extracted_profile_list)):
                profile_exists = False
                for j in range(len(profile_list)):
                    if extracted_profile_list[i].get_name() == profile_list[j].get_name():
                        profile_exists = True
                if (profile_exists == False):
                    profile_list.append(extracted_profile_list[i])

        if len(profile_list) > len(extracted_profile_list):
            for i in range(len(profile_list)):
                profile_exists = False
                for j in range(len(extracted_profile_list)):
                    if profile_list[i].get_name() == extracted_profile_list[j].get_name():
                        profile_exists = True
                if (profile_exists == False):
                    profile_list.remove(profile_list[i])

        #Update data for each profile in the list
        for i in range(len(profile_list)):
            for j in range(len(extracted_profile_list)):
                if profile_list[i].get_name() == extracted_profile_list[j].get_name():
                    if (profile_list[i].get_last_imported() != extracted_profile_list[j].get_last_imported()):
                        #Send email
                        name = extracted_profile_list[j].get_name()
                        send_message.send_message(name)
                        
                        #Set new date imported
                        profile_list[i].set_last_imported(extracted_profile_list[j].get_last_imported())

        #send_message.send_message("AWS")

        #Store in response_json
        profile_dicts = []
        for profile in profile_list:
            #print(profile.to_json())
            profile_dicts.append(profile.to_json())
            
        with open("profile_list.json", "w") as f:
            json.dump(profile_dicts, f, indent=4)

    #Suspend activity for X seconds
    time.sleep(seconds_to_sleep)
