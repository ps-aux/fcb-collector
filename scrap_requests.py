"""
An attempt to scrap Facebook using just request lib.
Implemented is only logging to Faceebook according to
its login process at the time
"""

import requests, utils
from http.cookies import SimpleCookie
from http import cookies

# Loging of requests
# logging.basicConfig(level=logging.DEBUG)

url = 'http://www.facebook.com/login.php?login_attempt=1'

missing_arg = utils.check_required_arg(utils.login_opt, utils.password_opt)
if missing_arg is not None:
    utils.exit_program("Missing required argument " + missing_arg)



email = utils.get_arg(utils.login_opt)
password = utils.get_arg(utils.password_opt)
payload = {'email': email, 'pass' : password}

resp_counter = 0

def log_response(response):
    print('Response:', response)
    indent = '\t'
    print(indent, 'Status:', response.status_code)
    if response.status_code != 200:
        print(indent, 'Redirect to:', response.headers['location'])
#     print('    Content: ', response.text)
    print(indent, 'Headers: ', response.headers)
    if 'set-cookie' in response.headers:
        print(indent, 'Cookies:')
        cookies = SimpleCookie(response.headers['set-cookie'])
        for c in cookies:
            print(indent * 2, c, ':', cookies[c].value)
    else:
        print(indent, 'Cookies: ---')
    
    global resp_counter
    resp_counter += 1
    utils.save_response(response, 'response{}.html'.format(resp_counter))

req = requests

#==== 1st request (response 301)

print("POST for " + url)
response = req.post(url, payload, allow_redirects=False)
log_response(response)


#Process 1st response
headers = response.headers
cookies = headers['set-cookie']
fcbk_cookie = cookies.split(';')[0].split('=')
print('Facebook cookie:', fcbk_cookie)
cookies = {fcbk_cookie[0]: fcbk_cookie[1]}
url = headers['location']

#===== 2nd request (response 302)
print("POST for " + url)
response = req.post(url, data=payload, cookies=cookies, allow_redirects=False)
log_response(response)

#Process 2nd response
url = response.headers['location']
cookies = SimpleCookie(response.headers['set-cookie'])

cookie_data = {}

for c_name in cookies:
    cookie_data[c_name] = cookies[c_name].value


#===== 3rd request
url = 'https://www.facebook.com/groups/153748404666241/members'
print("GET for " + url)
response = requests.get(url, cookies=cookie_data, allow_redirects=False)
log_response(response)

print('Finished')
