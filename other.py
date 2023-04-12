import time
from appium import webdriver
from appium.webdriver.common import mobileby
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


desired_capabilities = {
  "platformName": "Android",
  "deviceName": "05157df5f51db3",
  "appPackage": "com.xingin.xhs",
  "appActivity": ".activity.SplashActivity",
  "platformVersion": "7.0",
  "noReset": True,
  "fullReset": False
}

DRIVER_SERVER = 'http://localhost:4723/wd/hub'

class AppiumDemo(object):
    def __init__(self):
        self.driver = webdriver.Remote(DRIVER_SERVER, desired_capabilities=desired_capabilities)                               
        self.by = mobileby.MobileBy()
        
    def test(self):
        el1 = self.driver.find_element_by_id("com.xingin.xhs:id/ak0")   #点击搜索框，打开搜索页
        el1.click()
        #el2 = self.driver.find_element_by_id("com.xingin.xhs:id/al8")    #搜索框输入文字
        el2 = self.wait_find_element(by_type=self.by.ID, value='com.xingin.xhs:id/al8')
        el2.send_keys("tf")
        el3 = self.driver.find_element_by_id("com.xingin.xhs:id/ala")     #点击搜索
        el3.click()
        for i in range(4):
            el5 = self.driver.find_elements_by_id("com.xingin.xhs:id/aj4")
            print(i)
            for j in el5:
                
                try:
                    print('11')
                    print(j.text)
                except:
                    try:
                        print('12')
                        print(str(j.translate(non_bmp_map)))
                    except:
                        print('error')
            self.swipe_up()           
       

    def get_size(self, driver: WebDriver = None):
        """
        获取屏幕大小
        :param driver:
        :return:
        """
        driver = driver or self.driver
        if not driver:
            return driver

        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        return [x, y]

    def swipe_up(self, driver: WebDriver = None, _time: int = 1000):
        """
        向上滑动
        :param driver:
        :param _time:
        :return:
        """
        driver = driver or self.driver
        if not driver:
            return driver
        try:
            size = self.get_size(driver)
            x1 = int(size[0] * 0.5)  # 起始x坐标
            y1 = int(size[1] * 0.80)  # 起始y坐标
            y2 = int(size[1] * 0.30)  # 终点y坐标
            driver.swipe(x1, y1, x1, y2, _time)
            return True
        except:
            return False

def main():
    spider = AppiumDemo()
    spider.test()

if __name__ == '__main__':
    main()