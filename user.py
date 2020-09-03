from seed import *
from log import logger
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class User:

    def __init__(self, driver, title=None,
                 fname=None, lname=None, email=None,
                 password=None, dob=None, company=None, address=None,
                 city=None, postalcode=None, phone=None):
        logger.info('Starting user profile')
        self.automation = driver
        self.title = title
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password
        self.dob = dob
        self.company = company
        self.address = address
        self.city = city
        self.postalcode = postalcode
        self.phone = phone
        logger.info('Ending user profile')

    def set_user_info(self, usrs):
        """
           set user profile info using random user of users list
        :return:
        """
        logger.info('Starting set user profile info')
        user = choice(usrs)
        self.title = user['title']
        self.fname = user['fname']
        self.lname = user['lname']
        self.email = user['email']
        self.password = user['password']
        self.dob = user['dob']
        self.company = user['company']
        self.address = user['address']
        self.city = user['city']
        self.postalcode = user['postalcode']
        self.phone = user['phone']
        logger.info('Ending set user profile info')

    def __repr__(self):
        return f'fname: {self.fname} \nlastname: {self.lname}\n' \
               f'email: {self.email}\npassword: {self.password}\n' \
               f'dob: {self.dob}\ncompany: {self.company}\naddress: {self.address}\ncity: {self.city}' \
               f'postalcode: {self.postalcode}\nphone: {self.phone}'

    def create_account(self):
        """
        create new user account using user profile info
        :return: True if login else False
        """
        logger.info('*' * 20 + ' Starting creating  user account ' + '*' * 20)
        logger.info(f'\nfor user {self}')
        self.automation.wait.until(EC.presence_of_element_located((By.ID, 'email_create')))
        self.automation.driver.find_element_by_css_selector("#email_create").send_keys(self.email)  # send email
        self.automation.driver.find_element_by_css_selector("#SubmitCreate").click()  # 'create an account' btn

        # ##############################################
        # 1- mr. or mrs. ?
        logger.info(f'Choose title {self.title}')
        self.automation.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#account-creation_form div.account_creation div.clearfix')))
        if self.title == 'mr.':
            gender_selector = "input#id_gender1"

        else:
            gender_selector = "input#id_gender2"

        self.automation.driver.find_element_by_css_selector(gender_selector).click()
        self.automation.driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 2000)")  # scroll down

        # ##############################################
        logger.info(f'adding fname {self.fname}')
        # 2- first name
        self.automation.driver.find_element_by_css_selector("#customer_firstname").send_keys(self.fname)

        # ##############################################
        logger.info(f'adding lname {self.lname}')
        # 3- last name
        self.automation.driver.find_element_by_css_selector("#customer_lastname").send_keys(self.lname)

        # ##############################################
        logger.info(f'adding email {self.email}')
        # 4- email
        email_elem = self.automation.driver.find_element_by_css_selector("#email")
        email = email_elem.get_attribute('value')
        if not email:  # check email is passed or not ?
            logger.info('email was not added , add it again ')
            email.send_keys(self.email)

        # ##############################################
        logger.info(f'adding password')
        # 5- password
        password = f'document.getElementById("passwd").value="{self.password}";'  # js code to change password elm value
        self.automation.driver.execute_script(password)

        self.automation.driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1000)")  # scroll down

        # ##############################################
        # 6- date of birth   year-month-day
        logger.info(f'adding dob {self.dob}')
        self.select_dob()

        # ##############################################
        logger.info(f'adding fname#2 {self.fname}')
        # 7- fname
        get_fname = 'return document.querySelectorAll("div.account_creation #firstname")[0].value;'
        fname = self.automation.driver.execute_script(get_fname)
        if not fname:  # check fname is passed or not ?
            fname = f'document.querySelectorAll("div.account_creation #firstname")[0].value="{self.fname}";'
            self.automation.driver.execute_script(fname)

        # ##############################################
        logger.info(f'adding lname#2 {self.lname}')
        # 8- last name
        get_lname = 'return document.querySelectorAll("div.account_creation #lastname")[0].value;'
        lname = self.automation.driver.execute_script(get_lname)
        if not lname:  # check lname is passed or not ?
            lname = f'document.querySelectorAll("div.account_creation #lastname")[0].value="{self.lname}";'
            self.automation.driver.execute_script(lname)

        # ##############################################
        # 9- complete profile ( company, city, address, mobile, postalcode, alias address)
        logger.info('complete profile with ( company, city, address, mobile, postalcode, alias address)')
        logger.info(f'company({self.company}) , city({self.city}) , address({self.address}), mobile({self.phone}) , postalcode({self.postalcode}) , alias address({self.address[0] + self.address[-1]})')
        self.complete_profile()

        # ##############################################
        # 10- state (randomly choice)
        logger.info('choose state randomly')
        states = [state.text for state in self.automation.driver.find_elements_by_css_selector('#id_state option')]
        Select(self.automation.driver.find_element_by_css_selector('#id_state')).select_by_visible_text(choice(states))
        # ###############################################
        self.automation.driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 700)")  # scroll down
        self.automation.driver.find_element_by_css_selector('#submitAccount').click()  # register btn
        # ################ wait to login ###############################
        account_lst = self.automation.driver.find_elements_by_css_selector('.myaccount-link-list')
        timer = 1
        is_login = True
        while not account_lst:
            if timer == 60:
                is_login = False
                break
            time.sleep(.3)
            account_lst = self.automation.driver.find_elements_by_css_selector('.myaccount-link-list')
            timer += 1
        return is_login

    def complete_profile(self):
        elements = [
            {'element': 'company', 'elem_id': 'company', 'elem_value': self.company},
            {'element': 'address', 'elem_id': 'address1', 'elem_value': self.address},
            {'element': 'city', 'elem_id': 'city', 'elem_value': self.city},
            {'element': 'postalcode', 'elem_id': 'postcode', 'elem_value': self.postalcode},
            {'element': 'mobile', 'elem_id': 'phone_mobile', 'elem_value': self.phone},
            {'element': 'alias address', 'elem_id': 'alias', 'elem_value': self.address[0] + self.address[-1]},
        ]
        for element in elements:
            elem_id = element['elem_id']
            value = element['elem_value']
            elm_value = f'document.getElementById("{elem_id}").value="{value}";'
            self.automation.driver.execute_script(elm_value)

    def select_dob(self):
        dob = self.dob.split('-')
        year = dob[0]
        month = dob[1]
        day = dob[-1]
        if day[0] == '0':  # example : remove 0 ==> 03 to 3
            day = day[1:]
        if month[0] == '0':  # example : remove 0 ==> 05 to 5
            month = month[1:]
        dob_elems = {
            'days': day,
            'months': month,
            'years': year,

        }
        for elm_id, value in dob_elems.items():
            select = Select(self.automation.driver.find_element_by_id(elm_id))

            # select by visible value
            select.select_by_value(value)

    def choose_blouses_item(self):
        """
        choose blouses item and idd to cart
        Select “Blouses” Subcategory in “Women” Category & checkout procedure
        :return:
        """
        self.automation.driver.get('http://automationpractice.com/index.php?id_category=7&controller=category')
        logger.info(f'You Moved to "{self.automation.driver.title}"')
        self.automation.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product-image-container a.product_img_link')))
        logger.info('Click on Product')
        # click on product
        self.automation.driver.execute_script("document.querySelectorAll('div.product-image-container "
                                              "a.product_img_link')[0].click()")
        # time.sleep(2)
        logger.info('Adding Product to cart')
        # add to cart
        self.automation.driver.execute_script("document.querySelectorAll('#add_to_cart button')[0].click()")
        time.sleep(2)
        # proceed to checkout
        logger.info('proceed to checkout')
        self.automation.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.button-container .btn.btn-default.button.button-medium')))
        self.automation.driver.execute_script("document.querySelectorAll('.button-container "
                                              ".btn.btn-default.button.button-medium')[0].click()")

    def proceed_to_checkout_and_payment(self):
        """
        proceed to checkout and confirm order
        wizard : 1-summary ==> 2-sign in ==> 3-address ==> 4-shipping ==> 5-Payment
        :return:
        """
        # 1- summary
        logger.info('starting wizard with summary')
        self.automation.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.cart_navigation a.standard-checkout')))
        self.automation.driver.execute_script("document.querySelectorAll('.cart_navigation a.standard-checkout')[0]"
                                              ".click()")

        # 2-sign in & 3-address
        logger.info('2-sign in & 3-address')
        self.automation.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[name="processAddress"]')))

        self.automation.driver.find_element_by_css_selector('button[name="processAddress"]').click()

        # 4- shipping
        logger.info('4- shipping')
        self.automation.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#uniform-cgv span')))

        is_checked = self.automation.driver.find_element_by_css_selector('#uniform-cgv span').get_attribute('class')
        if not is_checked:  # agree
            self.automation.driver.execute_script("document.querySelectorAll('#cgv')[0].click()")

        self.automation.driver.find_element_by_css_selector('button[name=processCarrier]').click()
        logger.info('agree and confirmed')

        # pay by bank wire
        logger.info('pay by bank wire')
        self.automation.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.payment_module a')))

        self.automation.driver.find_element_by_css_selector('.payment_module a').click()

        # 5- payment and confirm
        logger.info('5- payment and confirm')
        self.automation.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#cart_navigation button')))
        self.automation.driver.find_element_by_css_selector('#cart_navigation button').click()

        # back to orders
        logger.info('back to orders')
        self.automation.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p.cart_navigation  .button-exclusive.btn')))
        self.automation.driver.find_element_by_css_selector('p.cart_navigation  .button-exclusive.btn').click()

        # how many items do you have
        time.sleep(1.5)
        self.automation.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#order-list tbody tr')))
        items = self.automation.driver.find_elements_by_css_selector('#order-list tbody tr')
        logger.info(f'You have "{len(items)}" at your order')






