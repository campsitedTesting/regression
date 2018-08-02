import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

## For Image comparison
from PIL import Image, ImageDraw
import os
import math

## For exception
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

## For randomization
import random
import string


from selenium.webdriver.chrome.options import Options



##  For testing file name
import datetime
import time

## For data analysis
import pandas as pd
import matplotlib

## For GUI control and config
from tkinter import Tk, Label, Button, Radiobutton, IntVar
from tkinter.ttk import *
import sys

##################################################################################
##
##  This is the common class which will be inherited  by other specific child classes
##
##################################################################################

class testing_config_utility():
    
    global text_info
    global driver
    global campsite_name
    global check_in_date
    global check_out_date
    global country_name
    global sort_criteria
    global filter_criteria
    
    def __init__(self, url, browser):
        self.url = url
        self.browser = browser

    ## Config the browser
    def web_driver_config(self):      
        global driver
        if (self.browser == 'Chrome'):
            driver = webdriver.Chrome(r'C:\Users\yanhui\AppData\Local\Programs\Python\Python36\Scripts\chromedriver.exe')
        driver.get(self.url)
        driver.maximize_window()
        time.sleep(2)

    ## Utility for partial-link-text-based-button
    def pltb_button_click(text_info):
        pltb_button_element = driver.find_element_by_partial_link_text(text_info)
        pltb_button_element.click()
        time.sleep(2)
        print('TESTING SUCCESS :  "{info}" is done successfully.....' .format(info = text_info))
    
    ## Utility for social-icon-based-button
    def social_icon_click(self):
        social_icon_list = driver.find_elements_by_xpath("//*[contains(@class, 'social-icon')]")
        for social_icon in social_icon_list:
            try:
                #print(social_icon.get_attribute('title'))
                text_info = social_icon.get_attribute('title')
                print('TESTING SUCCESS : "{info}" is done successfully.....' .format(info = text_info))
                social_icon.click()
                time.sleep(2)
                driver.back()
            except StaleElementReferenceException:
                #print ('Currently mail function in social icon checking will be ignored......')
                driver.switch_to.window(driver.window_handles[0])
                continue
                
    ## Common Search based on specific campsite and date
    def common_search_specific_campsite(campsite_name, check_in_date, check_out_date):
        ##  Maximize the window of the page
        driver.maximize_window()
        ## Fill in check-in date
        date_check_in_field = driver.find_element_by_name("csf[date_from]")
        driver.execute_script("arguments[0].type='text'",date_check_in_field)
        driver.find_element_by_name("csf[date_from]").send_keys(check_in_date)

        ## Fill in check-out date
        date_check_out_field = driver.find_element_by_name("csf[date_to]")
        driver.execute_script("arguments[0].type='text'",date_check_out_field)
        driver.find_element_by_name("csf[date_to]").send_keys(check_out_date)

        ## Fill in specific campsite name
        elem = driver.find_element_by_name("csf[query]")
        elem.clear()
        elem.send_keys(campsite_name)
        elem.send_keys(Keys.RETURN)
    
    ## Common Search based on specifc country card, the entrance should be from home page
    def common_search_country_card(country_name):
        ##  Maximize the window of the page
        driver.maximize_window()
        country_list = driver.find_elements_by_xpath("//*[contains(@class, 'country-card country-card-link')]")
        for country in country_list:
            country_name_tmp = country.get_attribute('title')
            if (country_name_tmp == country_name):
                #print ('Finding the country user defined......')
                country.click() ## to specific results page
                #driver.switch_to.window(driver.window_handles[0]) ## switch main tab (home page) to click next one
    
    ## Automation for 3 Steps based booking flow, and the payment step is not included
    def booking_flow(self):
        ## The precondition is use has done the checking of availability for accommodations in details page
        
        ## Click "Book now" with available accommodation to enter step 1
        button_book_now = driver.find_element_by_xpath("//*[contains(@class, 'campsite-availability__cta')]")  
        driver.execute_script("arguments[0].click();", button_book_now)
        time.sleep(15)
        
        ##  Click "Next" to enter step 2
        next_button_in_step1 = driver.find_element_by_xpath("//*[contains(@class, 'request-to-book')]")  
        next_button_in_step1.click()
        print('             1) Done to booking flow step 1.')
        time.sleep(10)
        
        ## Extract the filed info in source code of step 2l
        booking_input_items = driver.find_elements_by_xpath("//*[contains(@class, 'bookings__input')]")

        ## Following fixed info will be used to fill in the fileds, other fileds will be filled with random info
        country = "France"
        mail_address = "super@163.com"
        brith_date = "11111980"
        phone_number = "12345"
        
        input_item_list = [] ## This list is for debugging purpose
        for input_item in booking_input_items:
            item_name = input_item.get_attribute('name')
            temp_name = item_name.split('personal_information_form')[1][:-1][1:]
            input_item_list.append(item_name)

            # random value will be generated and used for some fileds
            random_value = ''.join([random.choice(string.ascii_lowercase) for n in range(8)])
    
            elem = driver.find_element_by_name(item_name)
            if (temp_name == "first_name" or temp_name == "last_name" or temp_name == "address" or temp_name == "city" or \
                 temp_name == "zip" or temp_name == "special_requests"):
                elem.send_keys(random_value)
            else:
                if (temp_name == "country"):
                    elem.send_keys(country)
                elif (temp_name == "email"):
                    elem.send_keys(mail_address)
                elif (temp_name == "email_confirmation"):
                    elem.send_keys(mail_address)
                elif (temp_name == "birthdate" or temp_name == "additional_persons_birthdays]["):
                    elem.send_keys(brith_date)
                elif (temp_name == "phone"):
                    elem.send_keys(phone_number)
                else:
                    elem.send_keys(random_value)
        
        ## Clicking "go to final step" to enter Step 3
        next_button_in_step2 = driver.find_element_by_xpath("//*[contains(@class, 'campsites-wishlist__item-btn')]")  
        next_button_in_step2.click()
        print('             2) Done to booking flow step 2.')
        time.sleep(15)     
        print('             3) Done to booking flow step 3. (fake step.....)')
        print("     TESTING SUCCESS: Campsite run through whole booking flow..... \n " )

    ## Sorting function (in Results page)    
    def specific_sort(self, sort_criteria):
        ## Do the sorting based on results pages
        ## Step 1 :  Click the button of sort 
        sort_buttion = driver.find_element_by_id('sort-select')
        sort_buttion.click()

        ## Step 2: Click user defined criteria to do the sorting
        sort_option = driver.find_element_by_link_text(sort_criteria)
        sort_option.click()
        
    ## Filter function (in Results Page)
    def specific_filter(self, filter_criteria):
        ##  Open the Filter checkbox
        filter_button = driver.find_element_by_xpath("//*[contains(@class, 'icon-filter')]")
        filter_button.click()
        time.sleep(2)
        
        filter_checkbox_list = driver.find_elements_by_xpath("//*[contains(@class, 'main-checkbox__icon')]")

        #  default filter criteria:  select the accomodation type "Pitch"  and other conditions for filtering
        if (filter_criteria == 'default_filter'):
            filter_checkbox_list[1].click() ## Pitch locates at the second one in the list, so "[1]"  is assigned to it ("[0"] means the first one)
            filter_checkbox_list[3].click() ## "[3]" means "2 stars"
            filter_checkbox_list[4].click() ## "[4]" means "3 stars"
            filter_checkbox_list[5].click() ## "[5]" means "4 stars"
        else:
            filter_checkbox_list[8].click() ## "[8]" means "restaurant"
            
        time.sleep(2)

        ## Apply the filtering to get the results expected
        apply_filter_buttion = driver.find_element_by_id("apply-filter")
        apply_filter_buttion.click()


##################################################################################
##
##  Following are for specific website functional classes
##
##################################################################################
        
## This is for common Navbar testing 
class campsited_common_navbar(testing_config_utility):
    def __init__(self, url, browser):
        super(campsited_common_navbar, self).__init__(url, browser)
        self.url = url
        self.browser = browser
        
    def button_click(self):
        button_list = ['About us', 'FAQs', 'My booking', 'Site Sign in', 'My wish list']
        
        for button in button_list:            
            if (button != 'My wish list'):
                campsited_common_navbar.pltb_button_click(button)
                driver.back()
            else: 
                try:
                    campsited_common_navbar.pltb_button_click('My wish list')
                    print('TESTING SUCCESS :  "My wish list" is done successfully.....')
                    driver.back()
                except WebDriverException:
                    print ('TESTING PENDED ： "My wish list" is not clickable, No campsite added by user....')

## This is for common Footer testing 
class campsited_common_footer(testing_config_utility):
    def __init__(self, url, browser):
        super(campsited_common_footer, self).__init__(url, browser)
        self.url = url
        self.browser = browser
        
    def button_click(self):
        button_list = ['About us', 'Blog', 'Privacy Policy', 'Customer Terms', 'Park Terms', 'Cookie Policy']
        
        for button in button_list:
            campsited_common_navbar.pltb_button_click(button)
            driver.back()
                    
## This is for General searching 
class campsited_common_search(testing_config_utility):
    def __init__(self, url, browser, campsite_name, check_in_date, check_out_date):
        super(campsited_common_search, self).__init__(url, browser)
        self.url = url
        self.browser = browser 
        self.campsite_name = campsite_name
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
    
    def specific_campsite(self):
        campsited_common_search.common_search_specific_campsite(self.campsite_name, self.check_in_date, self.check_out_date)
        time.sleep(15)
        
        ## Click "Availability" at details page to check the accommodation
        availability_button = driver.find_element_by_partial_link_text('Availability')
        availability_button.click()
        time.sleep(5)

## Country card clicking (from home page)
class country_card_clicking(testing_config_utility):
    def __init__(self, url, browser, country_name):
        super(country_card_clicking, self).__init__(url, browser)
        self.url = url
        self.browser = browser
        self.country_name = country_name
    
    def specific_country_card(self):
        country_card_clicking.common_search_country_card(self.country_name)
        time.sleep(5)

##  Theme cark clicking (from home page)
class theme_card_clicking(testing_config_utility):
    def __init__(self, url, browser, theme_candidate):
        super(theme_card_clicking, self).__init__(url, browser)
        self.url = url
        self.browser = browser
        self.theme_candidate = theme_candidate
    
    def specific_theme_card(self):
        driver.maximize_window()
        ## all of the countries and campsites in the themes will be caught and mixed into this list
        mixed_web_elem_list = driver.find_elements_by_xpath("//*[contains(@class, 'country-card-link')]")

        sites_num = 0
        for campsite in mixed_web_elem_list:
            campsite_name = campsite.get_attribute('title')
            ## "sites_num > 15" is to filter out the countries
            ## "sites_num % 2 == 0" is to make sure no repeating for one specific campsite
            ##  little tricky here.......
            if (sites_num > 15 and sites_num % 2 == 0):
                ## theme_candidate is a number assigned by user, which should be larger than 15
                if (sites_num == self.theme_candidate):
                    campsite.click()
            sites_num = sites_num + 1

## Campsite cark clicking (from Results page)
## Campsite cark clicking (from Results page)
#class country_card_booking(testing_config_utility):

## Campsite cark based booking (Tree tabs: Home page -----> Results page -----> Details page)
class country_card_booking():
    def __init__(self, current_country, current_browser, availab_only):
        self.country = current_country
        self.browser = current_browser
        self.availab_only = availab_only
    
    ############
    ## This will be tricky for this loop, since driver will be out of control after each booking is done, so 
    ##   1) A new initialization is needed for a new campsite booking
    ##  2) In each new initialization, driver and URL should be changed to original 
    ##  3) Each loop mapped with a new campsite (i = 0 means the first campsite, i=1 means the second campsite)
    ############
    def campsites_cards_run(self):
        ## Config the initial enviornment 
        if (self.browser == 'Chrome'):
            driver = webdriver.Chrome(r'C:\Users\yanhui\AppData\Local\Programs\Python\Python36\Scripts\chromedriver.exe')
        #driver.get('https://www.campsited.com/') ## Always from home page
        driver.get('https://campsited-staging.herokuapp.com/') ## For production purpuse
        driver.maximize_window()

        time.sleep(5)
 
        country_elem = driver.find_element_by_partial_link_text(self.country)
        country_elem.click()
        
        driver.switch_to.window(driver.window_handles[1])
        
        time.sleep(15)

        ## Get the totoal number of campsites in the first page
        elem = driver.find_element_by_class_name('search-results__cards-title')
        site_number_html = elem.get_attribute('innerHTML')

        site_number = int(site_number_html.split('>')[1].split('<')[0])

        print('Totally {number} campsites will be tested in {country}....\n ' .format (number = site_number, country = self.country))

        #print ('debug 3 ..........')
        for i in range(site_number):
            if (i > 0):
                if (self.browser == 'Chrome'):
                    driver = webdriver.Chrome(r'C:\Users\yanhui\AppData\Local\Programs\Python\Python36\Scripts\chromedriver.exe')
                driver.get('https://www.campsited.com/') ## Always from home page
                driver.get('https://campsited-staging.herokuapp.com/') ## For production purpose
                driver.maximize_window()
                time.sleep(5)

                country_elem = driver.find_element_by_partial_link_text(self.country)
                country_elem.click()
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(15)
                
            ## Get the campsites list
            campsite_web_elem_list = driver.find_elements_by_xpath("//*[contains(@class, 'js-card-data')]")
            #print(campsite_web_elem_list.get_attribute('innerHTML'))
            active_campsite = campsite_web_elem_list[i]
            #print(active_campsite.get_attribute('innerHTML'))
            active_campsite_name = active_campsite.get_attribute('data-name')
            print("No.{number} : Campsite Name: {name}" .format(number = i, name = active_campsite_name))
    
            ## Trick: ActionChains tech is used here because of the blocking of small-popup window related cookies(GDPR)
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_to_element_with_offset(active_campsite, 350, 0) # move click point to more right (positive x value 350), and keep the same height(no change for y value 0)
            action.click()
            action.perform()

            #driver.switch_to.window(driver.window_handles[1])
            ## Currently there are three tabs here, home page, country results page, and campsite details page (this is the destination) 
            driver.switch_to.window(driver.window_handles[-1])
            #driver.switch_to.window(driver.window_handles[1])
            time.sleep(5)
    
            check_in_date = '22/08/18'
            check_out_date = '23/08/18'
            
            date_check_in_field = driver.find_element_by_name("csf[date_from]")
            driver.execute_script("arguments[0].type='text'",date_check_in_field)
            driver.find_element_by_name("csf[date_from]").send_keys(check_in_date)

            ## Fill in check-out date
            date_check_out_field = driver.find_element_by_name("csf[date_to]")
            driver.execute_script("arguments[0].type='text'",date_check_out_field)
            driver.find_element_by_name("csf[date_to]").send_keys(check_out_date)
            print('				1) Done to fill date.')
            
            time.sleep(5)
            availability_button = driver.find_element_by_class_name('campsite-overview__panel-btn')
            #print(availability_button.get_attribute('innerHTML'))
            availability_button.click()
            print('				2) Done to check availability.')
            time.sleep(15)

            #country_card_booking.booking_flow(self)
            

            if (self.availab_only == True):
                print("				Campsite {name} availability checking is done....\n " .format(name = active_campsite_name))
                driver.quit()
            else:
                ### Following code is the details for booking which is the same as the function in test utility
                ## Click "Book now" with available accommodation to enter step 1
                try:  
                    button_book_now = driver.find_element_by_xpath("//*[contains(@class, 'campsite-availability__cta')]")
                    #print(button_book_now.get_attribute('innerHTML'))
                    driver.execute_script("arguments[0].click();", button_book_now)
                    #print('debug 5..........')
                    print('				3) Go to booking flow.')
                    time.sleep(10)
        
                    booking_summary_flag = driver.find_element_by_xpath("//*[contains(@class, 'campsite-booking__title')]") 
                    
                    ##  Click "Next" to enter step 2
                    next_button_in_step1 = driver.find_element_by_xpath("//*[contains(@class, 'request-to-book')]")  
                    next_button_in_step1.click()
                    time.sleep(10)
        
                    ## Extract the filed info in source code of step 2l
                    booking_input_items = driver.find_elements_by_xpath("//*[contains(@class, 'bookings__input')]")

                    ## Following fixed info will be used to fill in the fileds, other fileds will be filled with random info
                    country = "France"
                    mail_address = "super@163.com"
                    brith_date = "11111980"
                    phone_number = "12345"
        
                    input_item_list = [] ## This list is for debugging purpose
                    for input_item in booking_input_items:
                        item_name = input_item.get_attribute('name')
                        temp_name = item_name.split('personal_information_form')[1][:-1][1:]
                        input_item_list.append(item_name)

                        #random value will be generated and used for some fileds
                        random_value = ''.join([random.choice(string.ascii_lowercase) for n in range(8)])
                        elem = driver.find_element_by_name(item_name)
                        if (temp_name == "first_name" or temp_name == "last_name" or temp_name == "address" or temp_name == "city" or \
                            temp_name == "zip" or temp_name == "special_requests"):
                            elem.send_keys(random_value)
                        else:
                            if (temp_name == "country"):
                                elem.send_keys(country)
                            elif (temp_name == "email"):
                                elem.send_keys(mail_address)
                            elif (temp_name == "email_confirmation"):
                                elem.send_keys(mail_address)
                            elif (temp_name == "birthdate" or temp_name == "additional_persons_birthdays]["):
                                elem.send_keys(brith_date)
                            elif (temp_name == "phone"):
                                elem.send_keys(phone_number)
                            else:
                                elem.send_keys(random_value)
        
                    ## Clicking "go to final step" to enter Step 3

                    next_button_in_step2 = driver.find_element_by_xpath("//*[contains(@class, 'campsites-wishlist__item-btn')]")  
                    next_button_in_step2.click()
                    print('				5) Done to booking flow step 2.')
            
                    time.sleep(15)     
                    print('				6) Done to booking flow step 3. (fake step.....)')
                    print("		TESTING SUCCESS: Campsite < {name} > run through whole booking flow..... \n " .format(name = active_campsite_name))
                except NoSuchElementException:
                    print("		TESTING PENDED: Campsite < {name} >  is not available between {start_time} and {end_time}..... \n " .format(name = active_campsite_name, start_time = check_in_date, end_time = check_out_date))

                
                driver.quit()

##################################################################################
##
##  Following are for website snapshot comparison based checking methods
##
##################################################################################

class screen_analysis():

    global target_page_snapshot
    
    def __init__(self, browser, url, reference_page_snapshot, output_path):
        self.browser = browser
        self.url = url
        self.reference_page_snapshot = reference_page_snapshot
        self.output_path = output_path
    
    ## Get the time for each testing which will be used inside file name as flag
    def current_time_formated(self):
        ts = time.time()
        timestamp_formated = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
        return(timestamp_formated)
    
        ## Config the browser
    def web_driver_config(self):      
        global driver
        if (self.browser == 'Chrome'):
            driver = webdriver.Chrome(r'C:\Users\yanhui\AppData\Local\Programs\Python\Python36\Scripts\chromedriver.exe')
        driver.get(self.url)
        driver.maximize_window()
        time.sleep(15)
        
    def whole_page_snapshot(self):
        #driver.get(url)
        #driver.maximize_window()
         #time.sleep(15)

        ## get dimensions
        window_height = driver.execute_script('return window.innerHeight')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        num = int( math.ceil( float(scroll_height) / float(window_height) ) )

        ## Generate PNG files and scroll window to save the info into those files
        for i in range(num):
            f_name = self.output_path + 'tmp_' + str(i) + '_tmp.png'
            driver.save_screenshot(f_name)
    
            image = Image.open(f_name)
            (image_width, image_height) = image.size

            driver.execute_script( 'window.scrollBy(%d,%d)' % (0, window_height) )

        ## Merge the pieces of PNG files into one
        new_image = Image.new('RGB', (image_width, scroll_height))   
        for i in range(num):
            f_name = self.output_path + 'tmp_' + str(i) + '_tmp.png'
            image = Image.open(f_name)
    
            (image_width, image_height) = image.size
            y = i * window_height

            new_image.paste(image, box=(0, y, image_width, y + image_height))

        ## Save the whole target page PNG file
        global target_page_snapshot ## this variable will be used by function "analyze" in class 
        #target_page_snapshot = self.output_path + 'target_page_' + self.current_time_formated() + '.png'
        target_page_snapshot = self.output_path + self.current_time_formated() +'_target_page' +  '.png'
        new_image.save(target_page_snapshot)
        print('Target page is dumped into file {file_name}' .format(file_name = target_page_snapshot))
        print('\n')

    def analyze(self):
        screenshot_staging = Image.open(target_page_snapshot)
        screenshot_production = Image.open(self.reference_page_snapshot)

        print('Prepare for the comparison.....')
        print('Reference : {file_name}' .format(file_name = self.reference_page_snapshot))
        print('Target    : {file_name}' .format(file_name = target_page_snapshot))
        print('\n')
        columns = 60
        rows = 80
        screen_width, screen_height = screenshot_staging.size

        block_width = ((screen_width - 1) // columns) + 1 # this is just a division ceiling
        block_height = ((screen_height - 1) // rows) + 1

        pass_fail_marker = 'pass'
        for y in range(0, screen_height, block_height+1):
            for x in range(0, screen_width, block_width+1):
                region_staging = self.process_region(screenshot_staging, x, y, block_width, block_height)
                region_production = self.process_region(screenshot_production, x, y, block_width, block_height)

                if (region_staging is not None and region_production is not None and region_production != region_staging):
                    draw = ImageDraw.Draw(screenshot_staging)
                    draw.rectangle((x, y, x+block_width, y+block_height), outline = "red")
                    pass_fail_marker = 'fail'

        #diff_page_snapshot = self.output_path + 'diff_page_' + self.current_time_formated() + '.png'
        diff_page_snapshot = self.output_path + self.current_time_formated() +'_diff_page' +  '.png'
        screenshot_staging.save(diff_page_snapshot)
        
        print('Comparison is done.....')
        print('Difference : {file_name}' .format(file_name = diff_page_snapshot))
        if (pass_fail_marker == 'pass'):
            print('TESTING SUCCESS: No difference between Reference and Target.\n')
        else: ## fail
            print('TESTING FAILED: difference is found between Reference and Target. More details please check {f_name}\n' .format(f_name = diff_page_snapshot))

    def process_region(self, image, x, y, width, height):
        region_total = 0

        # This can be used as the sensitivity factor, the larger it is the less sensitive the comparison
        factor = 100

        for coordinateY in range(y, y+height):
            for coordinateX in range(x, x+width):
                try:
                    pixel = image.getpixel((coordinateX, coordinateY))
                    region_total += sum(pixel)/4
                except:
                    return

        return region_total/factor


##################################################################################
##
##  Following are for simple GUI config module to contrl scripts running
##
#################################################################################

class main_window(object):
    def __init__(self,master):
        self.master=master

        frame1 = Frame(self.master)
        frame1.pack()
        mLabel = Label(frame1, text = "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$").grid(row=0, column=0)
        mLabel = Label(frame1, text = "       Welcome to the regression system for Campsited page frontend functions       ").grid(row=1, column=0)
        mLabel = Label(frame1, text = "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$").grid(row=2, column=0)
    
    def user_testing_config(self, prompt, options):
        frame2 = Frame(self.master)
        frame2.pack()
        if prompt:
            Label(self.master, text=prompt).pack()
        global v
        v = IntVar()
        for i, option in enumerate(options):
            Radiobutton(self.master, text=option, variable=v, value=i).pack(anchor="w")
        Button(text="Submit", command=self.master.destroy).pack()
        self.master.mainloop()
        if v.get() == 0: return None
        return options[v.get()]


##################################################################################
##
##  Following are main body for scripts running
##
#################################################################################

if __name__ == '__main__':

    root=Tk()
    root.title("Main Window")
    #root.geometry("500x500")
    m_window=main_window(root)
    testing_item=m_window.user_testing_config("Please select following testing items....",
        [
            "initialization",
            "Common_header_footer",
            "Booking from country card",
            "Booking from specific area",
            "Booking from campsite name",
            "Booking from theme card",
            "Sort_and_filter_function",
            "Page info comparison"
        ])
    root.mainloop()

    print("#################################################################")
    print("##### Testing item : {}".format(repr(testing_item)))
    print("#################################################################")
    print("\n")


    ## Initialize all the variables to "False" to give a clean env 
    config_whole_env = False ## this should be set to True as usual except under some specific testing conditions (pure checking, campsite card based booking<3 tabs>, etc)
    config_click_header_button = False
    config_click_footer_button = False
    config_specific_campsite_search = False
    config_perform_booking_flow = False
    config_click_country_card = False
    config_click_theme_card = False
    config_sort_function = False
    config_filter_function = False
    config_country_card_booking = False
    config_enable_pure_checking = False 
    ##

    if (testing_item == "Common_header_footer"):
        config_whole_env = True ## ON
        config_click_header_button = True ## ON
        config_click_footer_button = True ## ON
        config_specific_campsite_search = False
        config_perform_booking_flow = False
        config_click_country_card = False
        config_click_theme_card = False
        config_sort_function = False
        config_filter_function = False
        config_country_card_booking = False
        config_enable_pure_checking = False
    elif (testing_item == "Booking from country card"):
        config_whole_env = False 
        config_click_header_button = False
        config_click_footer_button = False
        config_specific_campsite_search = False
        config_perform_booking_flow = False
        config_click_country_card = False
        config_click_theme_card = False
        config_sort_function = False
        config_filter_function = False
        config_country_card_booking = True ## ON
        config_enable_pure_checking = False
    elif (testing_item == "Booking from specific area"):
        None      
    elif (testing_item == "Booking from campsite name"):
        config_whole_env = True ## ON
        config_click_header_button = False
        config_click_footer_button = False
        config_specific_campsite_search = True ## ON
        config_perform_booking_flow = True ## ON
        config_click_country_card = False
        config_click_theme_card = False
        config_sort_function = False
        config_filter_function = False
        config_country_card_booking = False
        config_enable_pure_checking = False
    elif (testing_item == "Booking from theme card"):
        config_whole_env = True ## ON
        config_click_header_button = False
        config_click_footer_button = False
        config_specific_campsite_search = False
        config_perform_booking_flow = False
        config_click_country_card = False
        config_click_theme_card = True ## ON
        config_sort_function = False
        config_filter_function = False
        config_country_card_booking = False
        config_enable_pure_checking = False
    elif (testing_item == "Sort_and_filter_function"):
        config_whole_env = True ## ON
        config_click_header_button = False
        config_click_footer_button = False
        config_specific_campsite_search = False
        config_perform_booking_flow = False
        config_click_country_card = True ## ON
        config_click_theme_card = False
        config_sort_function = True ## ON
        config_filter_function = True ## ON
        config_country_card_booking = False
        config_enable_pure_checking = False
    elif (testing_item == "Page info comparison"):
        config_whole_env = False 
        config_click_header_button = False
        config_click_footer_button = False
        config_specific_campsite_search = False
        config_perform_booking_flow = False
        config_click_country_card = False
        config_click_theme_card = False
        config_sort_function = False
        config_filter_function = False
        config_country_card_booking = False
        config_enable_pure_checking = True ## ON        
    else:
        None
    
    
    ## Config the env
    if (config_whole_env == True):
        home_page_url = 'http://www.campsited.com'
        browser_name = 'Chrome'
    
        ## Initialize page with customerized URL and browser
        initial_page_enable = testing_config_utility(home_page_url, browser_name)
        initial_page_enable_config = initial_page_enable.web_driver_config()
    
    ## Check the button in header
    if (config_click_header_button == True):
        initial_page_navbar = campsited_common_navbar(home_page_url, browser_name)
        page_navbar_click = initial_page_navbar.button_click()
    
    ## Check the button in footer
    if (config_click_footer_button == True):
        initial_page_footer = campsited_common_footer(home_page_url, browser_name)
        page_footer_click = initial_page_footer.button_click()
        page_social_icon_click = initial_page_footer.social_icon_click()

    ## Perform common search based on specific campsite
    if (config_specific_campsite_search == True):
        campsite_name = 'Camping La Balma'
        user_check_in_date = '21/08/18'
        user_check_out_date = '23/08/18'
        print('Campsite < {name} > is seleted for booking flow testing in period between {s_date} and {e_date}.....' .format(name = campsite_name, s_date = user_check_in_date, e_date = user_check_out_date))
        page_common_search = campsited_common_search(home_page_url, browser_name, campsite_name, user_check_in_date, user_check_out_date )
        page_specific_campsite_search = page_common_search.specific_campsite()
    
    ## Perform 3 steps booking flow 
    if (config_perform_booking_flow == True):
        page_book_flow = page_common_search.booking_flow() ## after common search from a specific campsite
    
    ## Check country card
    if (config_click_country_card == True):
        country_name_given = 'Spain'
        initial_country_card_clicking = country_card_clicking(home_page_url, browser_name, country_name_given)
        specific_country_card_click = initial_country_card_clicking.specific_country_card()
        
       ##  Switch the active window to the country related results page
        driver.switch_to.window(driver.window_handles[-1])

    ## Check theme card
    if (config_click_theme_card == True):
        theme_candidate_given = 16
        initial_theme_card_clicking = theme_card_clicking(home_page_url, browser_name, theme_candidate_given)
        specific_theme_card_click = initial_theme_card_clicking.specific_theme_card()
        
        ##  Switch the active window to the campsite related details page
        driver.switch_to.window(driver.window_handles[1])
    
    ## Do sorting
    if (config_sort_function == True):
        root=Tk()
        root.title("Main Window")
        #root.geometry("500x500")
        m_window=main_window(root)
        sort_gui_given = m_window.user_testing_config(
            "Please select following sort criterias....",
            [
                "Relevance",
                "Best reviews",
                "Price (Low to high)",
                "Price (High to low)",
            ]
        )

        print("#################################################################")
        print("##### Sort criteria : {}".format(repr(sort_gui_given)))
        print("#################################################################")
        print("\n")

        #sort_criteria_given = 'Best reviews'
        sort_criteria_given = sort_gui_given

        time.sleep(5)
        specific_sort_function = initial_country_card_clicking.specific_sort(sort_criteria_given) ## after country card clicking
    
        ##  Switch the active window to results page with current sorting criteria
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])
    
    ## Do filter
    if (config_filter_function == True):
        filter_criteria_given = 'default_filter'
        print("#################################################################")
        print("##### Filter criteria : Pitch + 2 stars + 3 stars + 4 stars")
        print("#################################################################")
        print("\n")

        time.sleep(5)
        specific_filter_function = initial_country_card_clicking.specific_filter(filter_criteria_given) ## after country card clicking
        
        ##  Switch the active window to results page with current filter criteria
        driver.switch_to.window(driver.window_handles[-1])


    
        ## dump file for comparison
        time.sleep(10)
        #page_url_campare = driver.current_url
        #print(given_page_url)
        #browser_name = 'Chrome'
        #reference_page_given = r'C:\Users\yanhui\Python\python3\Campsited\reference file\try\whole_page.png' 
        #reference_page_given = r'D:\Project\campsited\regression\camprison\reference\\2018_08_01_19_21_39_target_page.png' 
        reference_page_given = r'D:\Project\campsited\regression\camprison\target\\2018_08_01_20_35_10_target_page.png'
        #output_path_given = r'C:\Users\yanhui\Python\python3\Campsited\reference file\try\\'
        output_path_given = r'D:\Project\campsited\regression\camprison\target\\'
    
        initial_screen_analysis = screen_analysis(browser_name, driver.current_url, reference_page_given, output_path_given)
        config_screen_analysis = initial_screen_analysis.web_driver_config()
        dump_page_snapshot = initial_screen_analysis.whole_page_snapshot()
        analysis_page_snapshot = initial_screen_analysis.analyze()

    
    ## Do campsite card based booking
    if (config_country_card_booking == True):
        root=Tk()
        root.title("Main Window")
        #root.geometry("500x500")
        m_window=main_window(root)
        country_gui_given = m_window.user_testing_config(
            "Please select following country to be tested....",
            [
                "Austria",
                "Spain",
                "France",
                "Belgium",
                "Germany",
                "Italy",
                "The Netherlands",
                "Luxembourg"
            ]
        )

        print("#################################################################")
        print("##### Country : {}".format(repr(country_gui_given)))
        print("#################################################################")
        print("\n")

        initial_country_card_booking = country_card_booking(country_gui_given, 'Chrome', False)
        run_country_card_booking = initial_country_card_booking.campsites_cards_run()
    
    ## Fore pure screen analysis based checking (no other actions)
    if (config_enable_pure_checking == True):
        
        home_page_url = 'https://www.campsited.com/campsites_search/results?csf%5Bquery%5D=Spain'
        browser_name = 'Chrome'
        reference_page_given = r'C:\Users\yanhui\Python\python3\Campsited\reference file\try\whole_page.png' 
        output_path_given = r'C:\Users\yanhui\Python\python3\Campsited\reference file\try\\'
    
        initial_screen_analysis = screen_analysis(browser_name, home_page_url, reference_page_given, output_path_given)
        config_screen_analysis = initial_screen_analysis.web_driver_config()
        dump_page_snapshot = initial_screen_analysis.whole_page_snapshot()
        analysis_page_snapshot = initial_screen_analysis.analyze()
