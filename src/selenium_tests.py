import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re

class KnowWayTests(unittest.TestCase):

    ptsprev = 0

    def setUp(self):
        self.driver = webdriver.Firefox()

    #Test 1.1
    def test11RegisterAndLogin(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/register")
        
        elem = driver.find_element_by_name("username")
        elem.send_keys("username123")
        elem = driver.find_element_by_name("password")
        elem.send_keys("abcdef123")
        elem = driver.find_element_by_name("password2")
        elem.send_keys("abcdef123")
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        
        driver.get("http://127.0.0.1:5000/main")

        assert driver.current_url=="http://127.0.0.1:5000/main"
        driver.get("http://127.0.0.1:5000/logout")

    
        #Test 1.2
    def test12SearchWiki(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/login")

        elem = driver.find_element_by_name("username")
        elem.send_keys("username123")
        elem = driver.find_element_by_name("password")
        elem.send_keys("abcdef123")
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        driver.get("http://127.0.0.1:5000/main")

        assert driver.current_url=="http://127.0.0.1:5000/main"
        elem = driver.find_element_by_name("searchWiki")
        elem.send_keys("Maria Curie")
        elem.send_keys(Keys.RETURN)
        time.sleep(15) #loading may take a while
        assert driver.current_url=="http://127.0.0.1:5000/wiki?title=Marie+Curie"
        assert "Maria Salomea Skłodowska" in driver.page_source
        driver.get("http://127.0.0.1:5000/logout")
        
        #Test 1.3
    def test13SearchPolona(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/login")

        elem = driver.find_element_by_name("username")
        elem.send_keys("username123")
        elem = driver.find_element_by_name("password")
        elem.send_keys("abcdef123")
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        driver.get("http://127.0.0.1:5000/main")

        time.sleep(2)
        assert driver.current_url=="http://127.0.0.1:5000/main"

        elem = driver.find_element_by_name("searchPolona")
        elem.send_keys("Mickiewicz Pan Tadeusz")
        elem.send_keys(Keys.RETURN)
        time.sleep(15)
        assert driver.current_url=="http://127.0.0.1:5000/polona?title=pisma-adama-mickiewicza-t-5&page=0"
        driver.get("http://127.0.0.1:5000/logout")
    

    #Test 2.1
    def test21AddComment(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/login")
        
        elem = driver.find_element_by_name("username")
        elem.send_keys("username123")
        elem = driver.find_element_by_name("password")
        elem.send_keys("abcdef123")
        elem.send_keys(Keys.RETURN)
        time.sleep(5)
        driver.get("http://127.0.0.1:5000/main")
        time.sleep(5)

        assert driver.current_url=="http://127.0.0.1:5000/main"
        elem = driver.find_element_by_name("searchWiki")
        elem.send_keys("Cracow")
        elem.send_keys(Keys.RETURN)
        time.sleep(15) #loading may take a while
        elem = driver.find_element_by_name("content")
        elem.send_keys("grzegorz brzeczyszczykiewicz")
        elem = driver.find_element_by_name("submit")
        elem.click()
        time.sleep(15) #loading may take a while
        elem = driver.find_element_by_name("content")
        elem.send_keys(Keys.BACKSPACE)
        assert "grzegorz brzeczyszczykiewicz" in driver.page_source
        driver.get("http://127.0.0.1:5000/logout")

        #Test 2.2
    def test22AddCommentTwoUsers(self):

        driver = self.driver
        driver.get("http://127.0.0.1:5000/register")

        elem = driver.find_element_by_name("username")
        elem.send_keys("username123b")
        elem = driver.find_element_by_name("password")
        elem.send_keys("abcdef123")
        elem = driver.find_element_by_name("password2")
        elem.send_keys("abcdef123")
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        driver.get("http://127.0.0.1:5000/main")
        time.sleep(5)

        assert driver.current_url=="http://127.0.0.1:5000/main"
        elem = driver.find_element_by_name("searchWiki")
        elem.send_keys("Cracow")
        elem.send_keys(Keys.RETURN)
        time.sleep(15) #loading may take a while
        elem = driver.find_element_by_name("content")
        elem.send_keys("cudne miasto polecam")
        elem = driver.find_element_by_name("submit")
        elem.click()
        time.sleep(15) #loading may take a while
        elem = driver.find_element_by_name("content")
        elem.send_keys(Keys.BACKSPACE) #in case the element still has "qwertyuiop" delete 'p'
        assert "grzegorz brzeczyszczykiewicz" in driver.page_source
        assert "cudne miasto polecam" in driver.page_source
        driver.get("http://127.0.0.1:5000/logout")

    #Test 2.3
    def test23AddCommentThreeUsers(self):

        driver = self.driver
        driver.get("http://127.0.0.1:5000/register")
        
        elem = driver.find_element_by_name("username")
        elem.send_keys("username123c")
        elem = driver.find_element_by_name("password")
        elem.send_keys("abcdef123")
        elem = driver.find_element_by_name("password2")
        elem.send_keys("abcdef123")
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        driver.get("http://127.0.0.1:5000/main")
        time.sleep(5)

        assert driver.current_url=="http://127.0.0.1:5000/main"
        elem = driver.find_element_by_name("searchWiki")
        elem.send_keys("Cracow")
        elem.send_keys(Keys.RETURN)
        time.sleep(10) #loading may take a while
        elem = driver.find_element_by_name("content")
        elem.send_keys("qwertyuiop")
        elem = driver.find_element_by_name("submit")
        elem.click()
        time.sleep(10) #loading may take a while
        elem = driver.find_element_by_name("submit")
        elem.click()
        time.sleep(10) #loading may take a while
        assert "grzegorz brzeczyszczykiewicz" in driver.page_source
        assert "cudne miasto polecam" in driver.page_source
        elem = driver.find_element_by_name("content")
        elem.send_keys(Keys.BACKSPACE) #in case the element still has "qwertyuiop" delete 'p'
        assert "qwertyuiop" in driver.page_source
        assert 2==driver.page_source.count("qwertyuiop")
        driver.get("http://127.0.0.1:5000/logout")


    #Test 3.1
    def test31SeeViews(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/login")
        
        elem = driver.find_element_by_name("username")
        elem.send_keys("username123")
        elem = driver.find_element_by_name("password")
        elem.send_keys("abcdef123")
        elem.send_keys(Keys.RETURN)
        time.sleep(5)
        driver.get("http://127.0.0.1:5000/main")
        time.sleep(60)
        driver.get("http://127.0.0.1:5000/main") #reload page

        assert "<a href=\"http://127.0.0.1:5000/wiki?title=Krak%C3%B3w\">Kraków</a> - 3 views <br>" in driver.page_source
        driver.get("http://127.0.0.1:5000/logout")

    #Test 3.2
    def test32SeeViews(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/login")
        time.sleep(5)
        elem = driver.find_element_by_name("username")
        elem.send_keys("username123")
        elem = driver.find_element_by_name("password")
        elem.send_keys("abcdef123")
        elem.send_keys(Keys.RETURN)
        time.sleep(5)
        driver.get("http://127.0.0.1:5000/main")
        time.sleep(2)

        assert driver.current_url=="http://127.0.0.1:5000/main"

        elem = driver.find_element_by_name("searchPolona")
        elem.send_keys("Lalka Bolesław Prus")
        elem.send_keys(Keys.RETURN)
        time.sleep(60)
        driver.get("http://127.0.0.1:5000/main")
        
        assert "<a href=\"http://127.0.0.1:5000/polona?title=lalka-powiesc-w-trzech-tomach-t-1\">lalka powiesc w trzech tomach t 1</a> - 1 views <br>" in driver.page_source
        driver.get("http://127.0.0.1:5000/logout")

    #Test 3.3
    def test33NewUserSeeViews(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/register")
        
        elem = driver.find_element_by_name("username")
        elem.send_keys("viewer123")
        elem = driver.find_element_by_name("password")
        elem.send_keys("abcdef123")
        elem = driver.find_element_by_name("password2")
        elem.send_keys("abcdef123")
        elem.send_keys(Keys.RETURN)
        time.sleep(60)
        driver.get("http://127.0.0.1:5000/main")
        time.sleep(2)
        assert driver.current_url=="http://127.0.0.1:5000/main"
        assert "<a href=\"http://127.0.0.1:5000/polona?title=lalka-powiesc-w-trzech-tomach-t-1\">lalka powiesc w trzech tomach t 1</a> - 1 views <br>" in driver.page_source
        assert "<a href=\"http://127.0.0.1:5000/wiki?title=Krak%C3%B3w\">Kraków</a> - 3 views <br>" in driver.page_source
        driver.get("http://127.0.0.1:5000/logout")

    
    #Test 4.1
    def test41PointAdding(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/register")
        
        elem = driver.find_element_by_name("username")
        elem.send_keys("adamsmith")
        elem = driver.find_element_by_name("password")
        elem.send_keys("smith0000")
        elem = driver.find_element_by_name("password2")
        elem.send_keys("smith0000")
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        driver.get("http://127.0.0.1:5000/main")
        time.sleep(2)
        assert driver.current_url=="http://127.0.0.1:5000/main"

        elem = driver.find_element_by_name("searchWiki")
        elem.send_keys("Moscow")
        elem.send_keys(Keys.RETURN)
        time.sleep(90)
        driver.get("http://127.0.0.1:5000/user/adamsmith")
        pts = re.search("[0-9.]+ Pts", driver.page_source).group()
        pts = pts.split(' ',-1)[0]
        pts = float(pts)
        self.__class__.ptsprev = pts
        assert pts > 0 #check if any points have been added
        driver.get("http://127.0.0.1:5000/logout")

    #Test 4.2
    def test42PointAdding(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/login")
        
        elem = driver.find_element_by_name("username")
        elem.send_keys("adamsmith")
        elem = driver.find_element_by_name("password")
        elem.send_keys("smith0000")
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        driver.get("http://127.0.0.1:5000/main")
        time.sleep(2)
        assert driver.current_url=="http://127.0.0.1:5000/main"

        elem = driver.find_element_by_name("searchWiki")
        elem.send_keys("Moscow")
        elem.send_keys(Keys.RETURN)
        time.sleep(90)
        driver.get("http://127.0.0.1:5000/user/adamsmith")
        pts = re.search("[0-9.]+ Pts", driver.page_source).group()
        pts = pts.split(' ',-1)[0]
        pts = float(pts)
        assert pts > self.__class__.ptsprev #check if any points have been added
        self.__class__.ptsprev = pts
        driver.get("http://127.0.0.1:5000/logout")


    #Test 4.3
    def test43PointAdding(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/login")
        
        elem = driver.find_element_by_name("username")
        elem.send_keys("adamsmith")
        elem = driver.find_element_by_name("password")
        elem.send_keys("smith0000")
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        driver.get("http://127.0.0.1:5000/main")
        time.sleep(2)
        assert driver.current_url=="http://127.0.0.1:5000/main"

        elem = driver.find_element_by_name("searchPolona")
        elem.send_keys("Dziady Adam Mickiewicz")
        elem.send_keys(Keys.RETURN)
        time.sleep(90)
        driver.get("http://127.0.0.1:5000/user/adamsmith")
        pts = re.search("[0-9.]+ Pts", driver.page_source).group()
        pts = pts.split(' ',-1)[0]
        pts = float(pts)
        assert pts > self.__class__.ptsprev #check if any points have been added
        driver.get("http://127.0.0.1:5000/logout")


    #Test 6.1
    def test61CheckRanking(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/login")

        elem = driver.find_element_by_name("username")
        elem.send_keys("username123")
        elem = driver.find_element_by_name("password")
        elem.send_keys("abcdef123")
        elem.send_keys(Keys.RETURN)
        
        driver.get("http://127.0.0.1:5000/main")
        time.sleep(30)
        driver.get("http://127.0.0.1:5000/ranking")
        time.sleep(2)
        assert '''1. 
                    <a href="user/adamsmith">''' in driver.page_source
        driver.get("http://127.0.0.1:5000/logout")

    #test 6.2
    def test62NewLeader(self):

        driver = self.driver
        driver.get("http://127.0.0.1:5000/register")
        
        elem = driver.find_element_by_name("username")
        elem.send_keys("aabbleader")
        elem = driver.find_element_by_name("password")
        elem.send_keys("aabbleader1")
        elem = driver.find_element_by_name("password2")
        elem.send_keys("aabbleader1")
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        driver.get("http://127.0.0.1:5000/main")

        elem = driver.find_element_by_name("searchWiki")
        elem.send_keys("Moscow")
        elem.send_keys(Keys.RETURN)
        time.sleep(300)

        driver.get("http://127.0.0.1:5000/main")

        elem = driver.find_element_by_name("searchWiki")
        elem.send_keys("Tokyo")
        elem.send_keys(Keys.RETURN)
        time.sleep(300)

        driver.get("http://127.0.0.1:5000/ranking")
        assert '''1. 
                    <a href="user/aabbleader">''' in driver.page_source
        assert '''2. 
                    <a href="user/adamsmith">''' in driver.page_source

        driver.get("http://127.0.0.1:5000/logout")

    #test 6.3
    def test63Consistency(self):

        driver = self.driver
        driver.get("http://127.0.0.1:5000/register")
        
        elem = driver.find_element_by_name("username")
        elem.send_keys("checker123")
        elem = driver.find_element_by_name("password")
        elem.send_keys("1234password")
        elem = driver.find_element_by_name("password2")
        elem.send_keys("1234password")
        elem.send_keys(Keys.RETURN)
        driver.get("http://127.0.0.1:5000/main")

        driver.get("http://127.0.0.1:5000/user/aabbleader")
        assert "Moscow" in driver.page_source
        assert "Tokyo" in driver.page_source

        driver.get("http://127.0.0.1:5000/user/checker123")
        assert "0 Pts." in driver.page_source

        driver.get("http://127.0.0.1:5000/logout")
        

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)