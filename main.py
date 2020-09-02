from seed import users
from user import User
from automation import BrowserAutomation
from log import logger
from datetime import datetime


if __name__ == '__main__':

    # ################ initialize driver and user info ########
    start_time = datetime.now()

    driver = BrowserAutomation()
    user = User(driver)
    user.set_user_info(users)

    # ############## automation  ###############################
    is_login = user.create_account()  # create an account an login
    if is_login:
        user.choose_blouses_item()  # Select “Blouses” Subcategory in “Women” Category & checkout procedure
        user.proceed_to_checkout_and_payment()  # checkout & confirm

    else:
        logger.info('registration or login failed, please check network connection and try again ')

    user.automation.driver.quit()
    end_time = datetime.now()
    logger.info("Duration of running tool was {} : ".format(end_time - start_time))
