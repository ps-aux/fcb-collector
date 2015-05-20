"""An attempt to log to and use Facebook Graph API with application authorization"""

import requests

# App node_id & secret. Not too much secure I know:) Will be changed later.
app_id= 'the_app_id'
app_secret = 'the_app_secret'

#Faceboook node node_id
node_id = '1647561646'


# First retrieve the access_token using app node_id & secret.
# This will be sufficient for the kind of operations we need.
token_url = 'https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id={}&client_secret={}'
token_url = token_url.format(app_id, app_secret)
response = requests.get(token_url)
token = response.text.split('=')[1]

url_args = "?&access_token=" + token
api_prefix = "https://graph.facebook.com/"

url = api_prefix + node_id + url_args
response = requests.get(url)
print(response.text)
print("Finished")
