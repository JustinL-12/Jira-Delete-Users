import requests
import Config
import json
import time

instance_url = 'team.uic.edu' # url of the Jira Server instance
user_search = 'ПОЛУЧИТЬ'      # the string to search users for
del_count = 1000              # number of users to delete, max 1000
wait_time = 5                 # time to wait between delete requests

# This is the url for the GET request search of users
users_url = "https://" + instance_url + "/rest/api/latest/user/search?username=" + user_search + "&maxResults=1000"

# GET request to JIRA REST Api
resp = requests.get(users_url, auth=Config.client_key)

# Check status of GET request
if resp.status_code != 200:
    raise Exception("GET users request failed with status code " + resp.status_code)

# Create json from response
resp_json = resp.json()

# Create an array of the emails and filter for real accounts
emails = []
for user in resp_json:
    if not user['emailAddress'].endswith('.edu'):
        emails.append(user['emailAddress'])

for email in emails:
    # DELETE request to Jira REST api
    del_url = "https://" + instance_url + "/rest/api/latest/user?key=" + email
    resp = requests.delete(del_url, auth=Config.client_key)

    # Parse response from Jira
    if resp.status_code == 204:
        print("User " + email + " successfully deleted")
    else:
        raise Exception("Failed to delete user " + email + " with status code " + resp.status_code)

    # Artificial wait so Jira doesn't slow down
    time.sleep(wait_time)

print("Process succesfully finished")
