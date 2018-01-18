from .base import FunctionalTest
from samireland.models import BlogPost

class BlogPageTests(FunctionalTest):

    def test_blog_page_layout(self):
        # The user goes to the blog page
        self.get("/")
        nav = self.browser.find_element_by_tag_name("nav")
        nav_links = nav.find_elements_by_tag_name("a")
        self.click(nav_links[4])

        # The page has the correct heading
        self.check_page("/blog/")
        self.check_title("Blog")
        self.check_h1("Blog")

        # There is a posts section
        posts = self.browser.find_element_by_id("blog-posts")
        self.assertIn("no blog posts", posts.text)
        with self.assertRaises(self.NoElement):
            posts.find_element_by_tag_name("a")


    def test_blog_posts_order(self):
        BlogPost.objects.create(date="2017-01-01", title="T1", body="1\n\n2")
        BlogPost.objects.create(date="2017-01-03", title="T2", body="1\n\n2")
        BlogPost.objects.create(date="2017-01-02", title="T3", body="1\n\n2")

        # They go to the page and look at the posts - there are 3
        self.get("/blog/")
        posts = self.browser.find_element_by_id("blog-posts")
        posts = posts.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 3)

        # They are in the correct order
        self.assertEqual(
         posts[0].find_element_by_tag_name("h2").text, "T2"
        )
        self.assertEqual(
         posts[1].find_element_by_tag_name("h2").text, "T3"
        )
        self.assertEqual(
         posts[2].find_element_by_tag_name("h2").text, "T1"
        )


    def test_blog_navigation(self):
        BlogPost.objects.create(date="2017-01-01", title="T1", body="1\n\n2")
        BlogPost.objects.create(date="2017-01-03", title="T2", body="1\n\n2")
        BlogPost.objects.create(date="2017-01-02", title="T3", body="1\n\n2")

        # The user goes to the blog page and none of the posts have navigations
        self.get("/blog/")
        posts = self.browser.find_element_by_id("blog-posts")
        posts = posts.find_elements_by_class_name("blog-post")
        for post in posts:
            with self.assertRaises(self.NoElement):
                post.find_element_by_id("posts-nav")

        # They go to the most recent post
        self.click(posts[0].find_element_by_tag_name("a"))
        self.check_page("/blog/2017/1/3/")

        # There is a nav section with a link to the previous page
        nav = self.browser.find_element_by_id("posts-nav")
        previous = nav.find_element_by_class_name("previous-page")
        with self.assertRaises(self.NoElement):
            nav.find_element_by_class_name("next-page")
        self.assertIn("Previous", previous.text)
        self.click(previous)
        self.check_page("/blog/2017/1/2/")

        # This page has both links, and they can still go back
        nav = self.browser.find_element_by_id("posts-nav")
        previous = nav.find_element_by_class_name("previous-page")
        next_ = nav.find_element_by_class_name("next-page")
        self.assertIn("Next", next_.text)
        self.assertIn("Previous", previous.text)
        self.click(previous)
        self.check_page("/blog/2017/1/1/")

        # The last page has no previous, but they can follow the next links
        nav = self.browser.find_element_by_id("posts-nav")
        previous = nav.find_element_by_class_name("previous-page")
        next_ = nav.find_element_by_class_name("next-page")
        self.assertEqual(previous.text, "")
        self.assertIn("Next", next_.text)
        self.click(next_)
        self.check_page("/blog/2017/1/2/")
        nav = self.browser.find_element_by_id("posts-nav")
        next_ = nav.find_element_by_class_name("next-page")
        self.click(next_)
        self.check_page("/blog/2017/1/3/")






class BlogPostAdditionTests(FunctionalTest):

    def test_can_add_blog_post(self):
        self.login()
        self.get("/blog/")

        # There is a link to create a new post
        posts = self.browser.find_element_by_id("blog-posts")
        link = posts.find_element_by_tag_name("a")
        self.click(link)

        # They are on the new project page
        self.check_page("/blog/new/")
        self.check_title("New Blog Post")
        self.check_h1("New Blog Post")

        # There is a form
        form = self.browser.find_element_by_tag_name("form")
        date_input = form.find_elements_by_tag_name("input")[0]
        title_input = form.find_elements_by_tag_name("input")[1]
        body_input = form.find_elements_by_tag_name("textarea")[0]

        # They enter some data and submit
        date_input.send_keys("01-06-2017")
        title_input.send_keys("My First Post")
        body_input.send_keys("Line 1\n\nLine 2")
        submit = form.find_elements_by_tag_name("input")[-1]
        self.click(submit)

        # They are on the page for the new article
        self.check_page("/blog/2017/06/01/")
        self.check_title("My First Post")

        # The blog post is there
        post = self.browser.find_element_by_class_name("blog-post")
        date = post.find_element_by_class_name("date")
        title = post.find_element_by_tag_name("h2")
        self.assertEqual(date.text, "1 June, 2017")
        self.assertEqual(title.text, "My First Post")
        body = post.find_element_by_class_name("blog-body")
        paragraphs = body.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 2)
        self.assertEqual(paragraphs[0].text, "Line 1")
        self.assertEqual(paragraphs[1].text, "Line 2")
        with self.assertRaises(self.NoElement):
            post.find_element_by_id("posts-nav")

        # They go back to the blog page and the post is there too
        self.get("/blog/")
        posts = self.browser.find_element_by_id("blog-posts")
        self.assertNotIn("no publications", posts.text)
        posts = posts.find_elements_by_class_name("blog-post")
        self.assertEqual(len(posts), 1)
        self.assertEqual(
         posts[0].find_element_by_class_name("date").text,
         "1 June, 2017"
        )
        self.assertEqual(
         posts[0].find_element_by_tag_name("h2").text,
         "My First Post"
        )
        with self.assertRaises(self.NoElement):
            posts[0].find_element_by_id("posts-nav")
        self.click(posts[0].find_elements_by_tag_name("a")[1])
        self.check_page("/blog/2017/6/1/")


    def test_blog_date_must_be_unique(self):
        self.login()
        self.get("/blog/new/")

        # There is a form
        form = self.browser.find_element_by_tag_name("form")
        date_input = form.find_elements_by_tag_name("input")[0]
        title_input = form.find_elements_by_tag_name("input")[1]
        body_input = form.find_elements_by_tag_name("textarea")[0]

        # They enter some data and submit
        date_input.send_keys("01-06-2017")
        title_input.send_keys("My First Post")
        body_input.send_keys("Line 1\n\nLine 2")
        submit = form.find_elements_by_tag_name("input")[-1]
        self.click(submit)

        # They do it again
        self.get("/blog/new/")
        form = self.browser.find_element_by_tag_name("form")
        date_input = form.find_elements_by_tag_name("input")[0]
        title_input = form.find_elements_by_tag_name("input")[1]
        body_input = form.find_elements_by_tag_name("textarea")[0]
        date_input.send_keys("01-06-2017")
        title_input.send_keys("My First Post")
        body_input.send_keys("Line 1\n\nLine 2")
        submit = form.find_elements_by_tag_name("input")[-1]
        self.click(submit)

        # They are on the same page
        self.check_page("/blog/new/")

        # The form is still filled in
        form = self.browser.find_element_by_tag_name("form")
        date_input = form.find_elements_by_tag_name("input")[0]
        title_input = form.find_elements_by_tag_name("input")[1]
        body_input = form.find_elements_by_tag_name("textarea")[0]
        self.assertEqual(date_input.get_attribute("value"), "2017-06-01")
        self.assertEqual(title_input.get_attribute("value"), "My First Post")
        self.assertEqual(body_input.get_attribute("value"), "Line 1\n\nLine 2")

        # There is an error message
        error = form.find_element_by_class_name("error-message")
        self.assertIn("already", error.text)



class BlogPostEditingTests(FunctionalTest):

    def setUp(self):
        FunctionalTest.setUp(self)
        BlogPost.objects.create(date="2011-01-01", title="T1", body="1\n\n2")


    def test_can_edit_blog_post(self):
        self.login()

        # The user goes to the article page
        self.get("/blog/2011/1/1/")

        # There is an edit link
        edit = self.browser.find_element_by_class_name("edit")
        self.click(edit)

        # They are on the edit page, and there is a filled in form
        self.check_page("/blog/2011/1/1/edit/")
        self.check_title("Edit Blog Post")
        self.check_h1("Edit Blog Post")
        form = self.browser.find_element_by_tag_name("form")
        date_input = form.find_elements_by_tag_name("input")[0]
        title_input = form.find_elements_by_tag_name("input")[1]
        body_input = form.find_elements_by_tag_name("textarea")[0]
        self.assertEqual(date_input.get_attribute("value"), "2011-01-01")
        self.assertFalse(date_input.is_enabled())
        self.assertEqual(title_input.get_attribute("value"), "T1")
        self.assertEqual(body_input.get_attribute("value"), "1\n\n2")

        # They make a bunch of edits and save
        title_input.send_keys("T")
        body_input.send_keys("B")
        submit = form.find_elements_by_tag_name("input")[-1]
        self.click(submit)

        # They are on the blog page and it is changed
        self.check_page("/blog/2011/1/1/")
        self.check_title("T1T")
        date = self.browser.find_element_by_class_name("date")
        self.assertEqual(date.text, "1 January, 2011")
        body = self.browser.find_element_by_class_name("blog-body")
        paragraphs = body.find_elements_by_tag_name("p")
        self.assertEqual(len(paragraphs), 2)
        self.assertEqual(paragraphs[0].text, "1")
        self.assertEqual(paragraphs[1].text, "2B")


    def test_blog_post_deletion(self):
        # User goes to edit the post
        self.login()
        self.get("/blog/2011/1/1/")
        edit = self.browser.find_element_by_class_name("edit")
        self.click(edit)
        self.check_page("/blog/2011/1/1/edit/")

        # There is a deletion button
        delete_button = self.browser.find_element_by_tag_name("button")
        self.assertIn("Delete", delete_button.text)

        # They click it and a form appears
        deletion_form = self.browser.find_elements_by_tag_name("form")[1]
        self.check_invisible(deletion_form)
        self.click(delete_button)
        self.check_visible(deletion_form)

        # The form asks them if they really want to delete and they back down
        self.assertIn("sure", deletion_form.text)
        no = deletion_form.find_element_by_tag_name("button")
        self.assertIn("No", no.text)
        self.click(no)
        self.check_invisible(deletion_form)

        # They change their mind and delete
        self.click(delete_button)
        self.check_visible(deletion_form)
        yes = deletion_form.find_elements_by_tag_name("input")[-1]
        self.assertIn("Yes", yes.get_attribute("value"))
        self.click(yes)

        # They are back on the blog page and the post is gone
        self.check_page("/blog/")
        posts = self.browser.find_element_by_id("blog-posts")
        self.assertIn("no blog posts", posts.text)
