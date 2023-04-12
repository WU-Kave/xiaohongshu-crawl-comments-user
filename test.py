# This sample code uses the Appium python client v2
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

import time
import pandas as pd
comment_list = []

search_keyword = '留学'

from appium.webdriver.common.touch_action import TouchAction


# 向上滑动一屏
def swipe_up(driver):
    # 获取当前屏幕分辨率
    screen_size = driver.get_window_size()
    width = screen_size['width']
    height = screen_size['height']

    # 计算起始和结束点的坐标
    start_x = width / 2
    start_y = int(height * 0.8)
    end_x = start_x
    end_y = int(height * 0.2)

    # 使用TouchAction类执行向上滑动操作
    touch_action = TouchAction(driver)
    touch_action.press(x=start_x, y=start_y).move_to(x=end_x, y=end_y).release().perform()

    driver.swipe(start_x, start_y, end_x, end_y, 5000)

# 获取当前首条屏幕的id、用户名、留言
def get_current_screen(title):
    firstComments = driver.find_elements(by=AppiumBy.ID, value="com.xingin.xhs:id/cgl")
    for firstComment in firstComments:
        nickname = firstComment.find_element(by=AppiumBy.ID, value="com.xingin.xhs:id/dng").text
        comment = firstComment.find_element(by=AppiumBy.ID, value="com.xingin.xhs:id/dkk").text
        firstComment.find_element(by=AppiumBy.ID, value="com.xingin.xhs:id/bt6").click() # 进入主页
        xhs_id = driver.find_element(by=AppiumBy.ID, value="com.xingin.xhs:id/cm5").text
        driver.find_element(by=AppiumBy.ID, value="com.xingin.xhs:id/cli").click() # 返回评论区
        common = {
            "标题": title,
            "用户名": nickname,
            "评论": comment,
            "小红书号": xhs_id
        }
        comment_list.append(common)
        print((nickname, comment, xhs_id))

caps = {}
caps["platformName"] = "Android"
caps["appium:platformVersion"] = "9"
caps["appium:deviceName"] = "127.0.0.1:62025 device"
caps["appium:appPackage"] = "com.xingin.xhs"
caps["appium:appActivity"] = ".index.v2.IndexActivityV2"
caps["appium:noReset"] = True
caps["appium:ensureWebviewsHavePages"] = True
caps["appium:nativeWebScreenshot"] = True
caps["appium:newCommandTimeout"] = 3600
caps["appium:connectHardwareKeyboard"] = True
caps["automationName"] = 'UiAutomator1'
caps['unicodeKeyboard'] = True
# 'automationName'：'UiAutomator1'
# "unicodeKeyboard": True  # 解决不能输入中文的问题
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)

time.sleep(6)

el1 = driver.find_element(by=AppiumBy.ID, value="com.xingin.xhs:id/cy9")
el1.click()
el2 = driver.find_element(by=AppiumBy.ID, value="com.xingin.xhs:id/brl")
el2.send_keys(search_keyword)
el3 = driver.find_element(by=AppiumBy.ID, value="com.xingin.xhs:id/brq")
el3.click()

# 搜索完成

time.sleep(1)


# 帖子
el4 = driver.find_elements(by=AppiumBy.ID, value="com.xingin.xhs:id/cab")
# len(el4)
print(f"有{len(el4)}条帖子")


for item in el4:
    print()
    item.click() # 进入帖子
    title = driver.find_element(by=AppiumBy.ID, value="com.xingin.xhs:id/cb2").text # 帖子标题
    driver.find_element(by=AppiumBy.ID, value="com.xingin.xhs:id/c_e").click() # 进入评论区

    # com.xingin.xhs:id/bdo
    is_end = False
    while is_end is not True:
        if driver.find_elements(by=AppiumBy.ID, value="com.xingin.xhs:id/bdo"):
            is_end = True
        
        get_current_screen(title)
        # 使用TouchAction类执行向上滑动操作
        firstComments = driver.find_elements(by=AppiumBy.ID, value="com.xingin.xhs:id/cgl")  
        touch_action = TouchAction(driver)
        touch_action.press(el=firstComments[0]).move_to(el=firstComments[-1]).release().perform()

    backButton = driver.find_element(by=AppiumBy.ID, value="com.xingin.xhs:id/k0")
    backButton.click() # 返回到搜索结果

touch_action = TouchAction(driver)
touch_action.press(el=el4[0]).move_to(el=el4[-1]).release().perform()

time.sleep(3)



driver.quit()

df = pd.DataFrame(comment_list)

# 将数据写入Excel文件
df.to_excel('comments.xlsx', index=False)

