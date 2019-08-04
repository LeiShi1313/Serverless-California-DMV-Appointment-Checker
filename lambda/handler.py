import os
import boto3
from datetime import datetime
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


class DMV:
    def __init__(self, options, path='/opt/chromedriver', screen_shot_path='/tmp'):
        self._driver = webdriver.Chrome(path, chrome_options=options)
        self.screen_shot_count = 0
        self.screen_shot_path = screen_shot_path

    @property
    def title(self):
        return self._driver.title

    def go_to_appointment_page(self):
        self._driver.get('https://www.dmv.ca.gov/wasapp/foa/driveTest.do')
        return self

    def get_screen_shot(self, element_id=None):
        if element_id is not None:
            ActionChains(self._driver).move_to_element(self._driver.find_element_by_id(element_id)).perform()
            self._driver.save_screenshot('{}/{}.png'.format(self.screen_shot_path, self.screen_shot_count))
        else:
            self._driver.save_screenshot('{}/{}.png'.format(self.screen_shot_path, self.screen_shot_count))
        print('screenshot {}/{}.png saved!'.format(self.screen_shot_path, self.screen_shot_count))
        print(os.path.exists('{}/{}.png'.format(self.screen_shot_path, self.screen_shot_count)))
        self.screen_shot_count += 1

    def find_element_by_id(self, id_):
        return self._driver.find_element_by_id(id_)

    def set_office(self, office_name):
        for office in self._driver.find_element_by_id('officeId').find_elements_by_tag_name('option'):
            if office.text == office_name:
                office.click()
                break
        print('office set')
        return self

    def set_type(self):
        self._driver.find_element_by_id('DT').click()
        print('type set')
        return self

    def set_first_name(self, first_name):
        self._driver.find_element_by_id('firstName').send_keys(first_name)
        print('first name set')
        return self

    def set_last_name(self, last_name):
        self._driver.find_element_by_id('lastName').send_keys(last_name)
        print('last name set')
        return self

    def set_dl_number(self, dl_number):
        self._driver.find_element_by_id('dl_number').send_keys(dl_number)
        print('dl number set')
        return self

    def set_birth(self, date):  # separate by '-'
        month, day, year = date.split('-')
        self._driver.find_element_by_id('birthMonth').send_keys(month)
        self._driver.find_element_by_id('birthDay').send_keys(day)
        self._driver.find_element_by_id('birthYear').send_keys(year)
        print('birth date set')
        return self

    def set_phone(self, number):  # separate by '-'
        area, prefix, suffix = number.split('-')
        self._driver.find_element_by_id('areaCode').send_keys(area)
        self._driver.find_element_by_id('telPrefix').send_keys(prefix)
        self._driver.find_element_by_id('telSuffix').send_keys(suffix)
        print('phone set')
        return self

    def submit(self):
        self._driver.find_element_by_xpath("//input[@value='1']").submit()
        print('form submitted')

    def print_page(self):
        print(self._driver.page_source)


def hello(event, context):
    options = Options()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('--start-fullscreen')

    dmv = DMV(options)
    dmv.get_screen_shot('findOffice')
    dmv.go_to_appointment_page()\
        .set_office("SAN JOSE")\
        .set_type()\
        .set_dl_number('Y7741394')\
        .set_first_name('Lei')\
        .set_last_name('Shi')\
        .set_birth('12-14-1992')\
        .set_phone('425-393-8484')\
        .submit()
    dmv.get_screen_shot()

    bucket_name = "selenium-screenshot"
    s3 = boto3.resource("s3")
    for i in range(dmv.screen_shot_count):
        s3.Bucket(bucket_name).put_object(
            Key='{}-{}.png'.format(datetime.now().strftime('%Y-%m-%d-%H:%M:%S'), i),
            Body=open('{}/{}.png'.format(dmv.screen_shot_path, i), 'rb'))

    response = {
        "statusCode": 200,
        "body": f"Page title: {dmv.title}"
    }
    return response


if __name__ == '__main__':
    hello('foo', 'bar')
