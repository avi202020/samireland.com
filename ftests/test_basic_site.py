from .base import FunctionalTest

class SiteLayoutTests(FunctionalTest):

    def test_page_layout(self):
        # All the right elements are there
        self.get("/")
        body = self.browser.find_element_by_tag_name("body")
        self.assertEqual(
         [element.tag_name for element in body.find_elements_by_xpath("./*")],
         ["header", "nav", "main", "footer"]
        )

        # The header has the name in it
        header = self.browser.find_element_by_tag_name("header")
        self.assertEqual(header.text, "Sam Ireland")

        # The nav has a list of links
        nav = self.browser.find_element_by_tag_name("nav")
        ul = nav.find_element_by_tag_name("ul")
        links = ul.find_elements_by_tag_name("li")
        self.assertEqual(links[0].text, "Home")
        self.assertEqual(links[1].text, "Research")
        self.assertEqual(links[2].text, "Projects")
        self.assertEqual(links[3].text, "Writing")
        self.assertEqual(links[4].text, "Blog")
        self.assertEqual(links[5].text, "About")

        # The footer has a bunch of icons
        footer = self.browser.find_element_by_tag_name("footer")
        icons = footer.find_elements_by_class_name("social-icon")
        self.assertGreaterEqual(len(icons), 4)



class HomePageTests(FunctionalTest):

    def test_home_page_structure(self):
        # The user goes to the home page
        self.get("/")
        self.check_title("Home")


        # There is an introductory section
        intro = self.browser.find_element_by_class_name("intro")
        with self.assertRaises(self.NoElement):
            intro.find_element_by_tag_name("a")



class AuthTests(FunctionalTest):

    def test_can_log_in(self):
        self.get("/")

        # The 'l' is a link and it is the only one
        header = self.browser.find_element_by_tag_name("header")
        links = header.find_elements_by_tag_name("a")
        self.assertEqual(links[0].text, "l")
        self.assertEqual(len(links), 1)

        # Clicking it goes to the login page
        self.click(links[0])
        self.check_page("/authenticate/")
        self.check_title("Log In")
        self.check_h1("Log In")

        # There is a login form
        login_form = self.browser.find_element_by_tag_name("form")
        name_entry = login_form.find_elements_by_tag_name("input")[0]
        password_entry = login_form.find_elements_by_tag_name("input")[1]
        submit_button = login_form.find_elements_by_tag_name("input")[-1]

        # They login
        name_entry.send_keys("testsam")
        password_entry.send_keys("testpassword")
        submit_button.click()

        # They are on the home page
        self.check_page("/")

        # There is a logout button
        header = self.browser.find_element_by_tag_name("header")
        logout_link = header.find_elements_by_tag_name("a")[-1]


    def test_can_prevent_login(self):
        self.get("/authenticate/")
        login_form = self.browser.find_element_by_tag_name("form")
        name_entry = login_form.find_elements_by_tag_name("input")[0]
        password_entry = login_form.find_elements_by_tag_name("input")[1]
        submit_button = login_form.find_elements_by_tag_name("input")[-1]
        name_entry.send_keys("badguy1337")
        password_entry.send_keys("h4ck0r")
        submit_button.click()

        # The attempt fails.
        self.check_page("/authenticate/")
        login_form = self.browser.find_element_by_tag_name("form")
        error = login_form.find_element_by_class_name("error-message")
        self.assertEqual(error.text, "Nope!")
