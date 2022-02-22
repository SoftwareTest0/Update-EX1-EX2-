
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
driver = None
#it will run before all the test
@pytest.fixture()
def setup(request):
    global driver
    driver = webdriver.Chrome(executable_path="C:\\temp\\chromedriver.exe") # or driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://radiothek.orf.at/search")
    driver.maximize_window()
    driver.implicitly_wait(10)
    #Accept cookies
    driver.find_element(By.ID, "didomi-notice-agree-button").click()
    request.cls.driver = driver
    yield
    driver.close()

class TestRadio:
    #requirment 1
    def test_BasicSearch(self,setup):
        searchValue="Radio Tirol"
        self.driver.find_element(By.XPATH,"//input[@type='search']").send_keys(searchValue)
        self.driver.find_element(By.CSS_SELECTOR,"[type='submit']").click()
        time.sleep(5)
        resultlist=self.driver.find_elements(By.XPATH,"//li[@class='search-hit']//p/span[@class='type']")
        print(len(resultlist))
        for elm in resultlist:
            print(elm.text)
            self.driver.execute_script("arguments[0].scrollIntoView();", elm)
            assert searchValue==elm.text

    # requirment 2
    def test_searchandCollect_result(self,setup):
        searchQuery="Nachmittag"
        elment=self.driver.find_element(By.XPATH,"//input[@type='search']")
        self.driver.execute_script("arguments[0].scrollIntoView();", elment)
        elment.send_keys(searchQuery)
        self.driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()
        time.sleep(5)
        resultlist = self.driver.find_elements(By.XPATH, "//li[@class='search-hit']//p/span[@class='type']")
        result=[]
        for elm in resultlist:
            self.driver.execute_script("arguments[0].scrollIntoView();", elm)
            result.append(elm.text)
        resultDict={}
        for i in result:
            if i in resultDict:
                resultDict[i]=resultDict[i]+1
            else:
                resultDict[i]=1
        print(resultDict)
        assert len(resultDict.keys())>1

    # requirment 3
    def test_filter_search_result_usingSearchOption(self,setup):
        searchQuery = "oi"
        elment = self.driver.find_element(By.XPATH, "//input[@type='search']")
        self.driver.execute_script("arguments[0].scrollIntoView();", elment)
        elment.send_keys(searchQuery)
        self.driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()
        self.driver.find_element(By.XPATH, "//span[@title='Alle Sender']").click()
        checkbox=self.driver.find_element(By.XPATH, "//li[@value='oe1']")
        #self.driver.execute_script("arguments[0].scrollIntoView();", checkbox)
        driver.execute_script("arguments[0].click();", checkbox)
        #checkbox.click()
        time.sleep(5)
        resultlist = self.driver.find_elements(By.XPATH, "//li[@class='search-hit']//p/span[@class='type']")
        print(len(resultlist))
        for elm in resultlist:
            print(elm.text)
            self.driver.execute_script("arguments[0].scrollIntoView();", elm)
            assert "Ö1" == elm.text
