from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time, re, utils, requests

utils.log('Starting Facebook scrapping via browser')

#=== Initial 'constants'
# Sleep in seconds
sleep_interval = 2
res_file = utils.ensure_path('~/data_analysis/fcb_analysis.txt')


missing_arg = utils.check_required_arg(utils.login_opt, utils.password_opt, utils.ch_driver_opt)
if missing_arg is not None:
    utils.exit_program('Missing required argument ' + missing_arg)

login = utils.get_arg(utils.login_opt)
password = utils.get_arg(utils.password_opt)
driver_path = utils.get_arg(utils.ch_driver_opt)


utils.log('Starting browser')
browser = webdriver.Chrome(executable_path=driver_path)

# Log in
utils.log('Logging in as ' + login + ' : **' + password[2:])
url = 'https://www.facebook.com/'
browser.get(url)
browser.find_element_by_id('email').send_keys(login)
browser.find_element_by_id('pass').send_keys(password)
browser.find_element_by_id('u_0_n').click()

url = 'https://www.facebook.com/groups/153748404666241/members'
# url = 'https://www.facebook.com/groups/597682743580084/members'
# url = 'https://www.facebook.com/groups/javagroupsk/members'

utils.log('Getting the group page')
browser.get(url)

more_btn = None

counter = 0
while more_btn == None:
    try:
        try:
            browser.find_element_by_class_name('uiMorePager')
        except NoSuchElementException:
            # We are missing the holding element
            utils.log('Loaded all group members')
            break

        more_btn = browser.find_element_by_class_name('uiMorePagerPrimary')
        counter += 1
        utils.log('Loading more group members({})'.format(counter))
        more_btn.click()
        more_btn = None



        time.sleep(sleep_interval)
    except NoSuchElementException:
        pass

 
utils.log("Finding relevant elements")
elements = browser.find_elements_by_css_selector('div.fsl.fwb.fcb')
utils.log("Elements found")


c = 0
users = []
for el in elements:
    c += 1
    a = el.find_element_by_tag_name('a')
    name = a.text
    link = a.get_attribute('data-hovercard')
    match = re.search('(?<=id=).*(?=&)', link)
    if match == None:
        raise RuntimeError('Unexpected data format. Could not parse user id from ' + link)
    user_id = match.group(0)
    t = (name, user_id)
    utils.log("Adding user " + str(t) + " ({}/{})".format(c, len(elements)))
    users.append(t)


# utils.log(users)

def process_users(users):
    c = 0
    html_page = '<html><body>'
    prefix = 'https://facebook.com/'
    for user in users:
        c += 1
        utils.log(user)
        user_id = user[1]
        utils.log('Processing ' + user_id + " ({}/{})".format(c, len(users)))
        url = prefix + user_id
        browser.get(url)

        a_el = browser.find_element_by_class_name('profilePicThumb')
        a_el.click()

        while True:
            try:
                img_el =  browser.find_element_by_class_name('spotlight')
                break
            except NoSuchElementException:
                    try:
                        img_el = browser.find_element_by_css_selector('img._4-od')
                        break
                    except NoSuchElementException:
                        pass
            #The ajax call has not finished yet so let's wait 1 second
            #and repeat it again
            time.sleep(1)
        
        pic_url = img_el.get_attribute('src')
        response = requests.get(pic_url)
        f = open('/home/arkonix/tmp/pics/{}.jpg'.format(user_id), 'wb')
        f.write(response.content)
        page_row = '<a href="{}"><img src="{}" title="{}"></a>'.format(url, user_id + '.jpg', user[0])
        html_page = html_page + page_row + '\n'

    html_page = html_page + '</body></html>'
    page_file = open('/home/arkonix/tmp/pics/all.html','w',encoding='utf-8')
    page_file.write(html_page)

        
        

process_users(users)
# 
utils.log('Closing the browser')
# browser.close()
utils.log('The end')


