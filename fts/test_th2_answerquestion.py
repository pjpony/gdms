
from functional_tests import FunctionalTest, ROOT, USERS, questref
import functional_tests
import time
from ddt import ddt, data, unpack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# Testuser1 - stays as unspecified
# Testuser2 - specifies Africa and unspecified country and subdivision
# Testuser3 - specifies Africa and South Africa and unspecified subdivision
# Testuser4 - specifies Europe and unspecified country
# Testuser5 - specifies Europe and Switzerland and unspecified Subdivision
# Testuser6 - specifies North America and Unspeccified country
# Testuser7 - specifies North America, Canada and unspecified subdivision
# Testuser8 - specifies North America, Canada and Alberta
# Testuser9 - specifies North America, Canada and Saskatchewan
# This currently not working properly with chromedriver use firefox for this phase
# this will need to be done along with add questions be

# changed user 6 to get local questions for all areas of north america
# seems reasonable then more tests of getting all questsions


@ddt
class AnswerQuestion (FunctionalTest):

    def setUp(self):
        self.url = ROOT + '/default/user/login'
        get_browser = self.browser.get(self.url)

    @data((USERS['USER2'], USERS['PASSWORD2'], '2', 'in progress', 'Africa Continental'),
          (USERS['USER3'], USERS['PASSWORD3'], '2', 'in progress', 'Africa Continental'),
          (USERS['USER4'], USERS['PASSWORD4'], '2', 'in progress', 'Switzerland National'),
          (USERS['USER5'], USERS['PASSWORD5'], '2', 'in progress', 'Switzerland National'),
          (USERS['USER6'], USERS['PASSWORD6'], '2', 'in progress', 'Saskatchewan Local'),
          (USERS['USER7'], USERS['PASSWORD7'], '2', 'in progress', 'Saskatchewan Local'),
          (USERS['USER8'], USERS['PASSWORD8'], '9', 'All questions', 'All questions'),
          (USERS['USER9'], USERS['PASSWORD9'], '2', 'ell done', 'Saskatchewan Local'))
    @unpack
    def test_answer(self, user, passwd, answer, result1, result2):
        mailstring = user + '@user.com'
        email = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_name("email"))
        email.send_keys(mailstring)

        password = self.browser.find_element_by_name("password")
        password.send_keys(passwd)

        submit_button = self.browser.find_element_by_css_selector("#submit_record__row input")
        submit_button.click()
        time.sleep(1)

        self.url = ROOT + '/answer/get_question/quest'
        get_browser = self.browser.get(self.url)
        time.sleep(1)

        if answer != '9':
            ansstring = "(//input[@name='ans'])[" + answer + "]"

            wait = WebDriverWait(self.browser, 12)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, ansstring)))
            element.click()
            # toclick = WebDriverWait(self, 10).until(lambda self : self.browser.find_element_by_xpath(ansstring))
            # toclick.click()
            urgency = self.browser.find_element_by_id("userquestion_urgency")
            urgency.send_keys("7")
            importance = self.browser.find_element_by_id("userquestion_importance")
            importance.send_keys("8")
            self.browser.find_element_by_id("userquestion_changecat").click()

            category = self.browser.find_element_by_id("userquestion_category")
            category.send_keys("Strategy")
            self.browser.find_element_by_id("userquestion_changescope").click()

            self.browser.find_element_by_id("userquestion_answerreason").send_keys("the right answer selenium testing")

            submit_button = self.browser.find_element_by_css_selector("#submit_record__row input")
            submit_button.click()

        time.sleep(1)
        body = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_tag_name('body'))
        self.assertIn(result1, body.text)
        self.assertIn(result2, body.text)

        self.url = ROOT + '/default/user/logout'
        get_browser = self.browser.get(self.url)
        time.sleep(1)
