from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,\
    StaleElementReferenceException
import time, re, utils, requests
from utils import log

class FcbBrowserScrapper:
    
    root_url = 'https://www.facebook.com/'

    def __init__(self, browser, login, password):
        self.browser = browser
        self.login = login
        self.password = password

    def log_in(self):
        """Logs in to the facebook. User must not be logged in"""

        if (hasattr(self, 'logged_in')):
            raise ValueError("The user is already logged in")

        self.logged_in = True
        
        log('Logging in as ' + self.login + ' : **' + self.password[2:])
        self.browser.get(FcbBrowserScrapper.root_url)
        self.browser.find_element_by_id('email').send_keys(self.login)
        self.browser.find_element_by_id('pass').send_keys(self.password)
        self.browser.find_element_by_id('u_0_n').click()


    def scrap_group_members(self, group_id):
        #Wait interval for more members to be loaded - in seconds.
        sleep_interval = 2
        url = 'https://www.facebook.com/groups/{}/members'.format(group_id)

        log('Getting the group page')
        self.browser.get(url)

        more_btn = None

        counter = 0
        while more_btn == None:
            try:
                try:
                    self.browser.find_element_by_class_name('uiMorePager')
                except NoSuchElementException:
                    # We are missing the holding element
                    log('Loaded all group members')
                    break

                more_btn = self.browser.find_element_by_class_name('uiMorePagerPrimary')
                counter += 1
                log('Loading more group members({})'.format(counter))
                more_btn.click()
                more_btn = None

                time.sleep(sleep_interval)
            except NoSuchElementException:
                pass

         
        log("Finding relevant elements")
        elements = self.browser.find_elements_by_css_selector('div.fsl.fwb.fcb')
        log("Elements found")


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
            log("Adding user " + str(t) + " ({}/{})".format(c, len(elements)))
            users.append(t)
            
        return users


    def process_users(self, users, directory):
        
        utils.ensure_path(directory + '/pics/')

        c = 0
        stale_count = 0
        no_such_el_count = 0
        unprocessed_ids = []
        bad_page_ids = []
        html_file = open(directory + '/index.html','w',encoding='utf-8')
        html_file.write('<html><body>\n')

        for user in users:
            try:
                c += 1
                log(user)
                user_id = user[1].strip()
                log('Processing ' + user_id + " ({}/{})".format(c, len(users)))

                url = FcbBrowserScrapper.root_url + user_id
                self.browser.get(url)

                a_el = self.browser.find_element_by_class_name('profilePicThumb')
                a_el.click()

                while True:
                    try:
                        img_el =  self.browser.find_element_by_class_name('spotlight')
                        break
                    except NoSuchElementException:
                            try:
                                img_el = self.browser.find_element_by_css_selector('img._4-od')
                                break
                            except NoSuchElementException:
                                pass
                    #The ajax call has not finished yet so lets wait 1 second
                    #and repeat it again
                    time.sleep(1)
                
                try:
                    pic_url = img_el.get_attribute('src')
                except StaleElementReferenceException:
                    stale_count +=1
                    utils.log('Stale element encountered ({})'.format(stale_count))
                    unprocessed_ids.append(user_id)
                    continue

                #Retrieve and... 
                response = requests.get(pic_url)
                #...save the photo
                photo_file = open(directory + '/pics/{}.jpg'.format(user_id), 'wb')
                photo_file.write(response.content)

            except NoSuchElementException:
                utils.log("Failed scrapping page for user {} - no such element".format(user_id))
                unprocessed_ids.append(user_id)
                bad_page_ids.append(user_id)
                no_such_el_count += 1

            
            
            #
            page_row = '<a href="{}"><img src="pics/{}" title="{}"></a>'.format(url, user_id + '.jpg', user[0])
            html_file.write(page_row + '\n')

        utils.log('Total staled: ' + stale_count)
        utils.log('Total not found: ' + no_such_el_count)
        utils.log('Unprocessed ids:' + unprocessed_ids)
        html_file.write('</body></html>')

        
def main():
    #Basic configuration
    data_dir = utils.ensure_path('~/data_analysis/fcb/')
#     group_id = 153748404666241
    group_id = 597682743580084
    
    #Load basic arguments
    log("Parsing basic arguments")
    missing_arg = utils.check_required_arg(utils.login_opt, utils.password_opt, utils.ch_driver_opt)
    if missing_arg is not None:
        utils.exit_program('Missing required argument ' + missing_arg)
    login = utils.get_arg(utils.login_opt)
    password = utils.get_arg(utils.password_opt)
    driver_path = utils.get_arg(utils.ch_driver_opt)


    log('Starting browser')
    browser = webdriver.Chrome(executable_path=driver_path)

    scrapper = FcbBrowserScrapper(browser, login, password)
    users = scrapper.scrap_group_members(group_id)

    
    #Temporary code for loading user from file rather from the web
    #to speed up the development
#     users_file = utils.ensure_path('~/data_analysis/mlyny_group.txt')
#     users = []
#     with open(users_file,  encoding='utf-8') as f:
#         for line in f:
#             if line == '':
#                 break
#             s = line.split(',')
#             users.append((s[0], s[1]))

    
    scrapper.log_in()
    scrapper.process_users(users, data_dir)
 
    log('Closing the browser')
    browser.close()
    log('The end')


main()

