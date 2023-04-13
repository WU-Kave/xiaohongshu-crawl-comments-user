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
wordCloud_Analysis_text = ''

search_keyword = '租房好物'

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
    touch_action.press(x=start_x, y=start_y).move_to(x=end_x, y=end_y).wait(3000).release().perform()

    # driver.swipe(start_x, start_y, end_x, end_y, 5000)

# 获取当前首条屏幕的id、用户名、留言
def get_current_screen(title, firstComments):
    global wordCloud_Analysis_text
    for firstComment in firstComments:
        
        is_nickname_exist = firstComment.find_elements(by=AppiumBy.ID, value="com.xingin.xhs:id/dng")
        is_comment_exist = firstComment.find_elements(by=AppiumBy.ID, value="com.xingin.xhs:id/dkk")
        # 防止只露出了半截
        if is_nickname_exist and is_comment_exist:
            nickname = is_nickname_exist[0].text
            comment = is_comment_exist[0].text
            print(nickname, comment)
            is_nickname_exist[0].click() # 进入主页
            # 滑动之后第一次点不进去，需要点2次
            is_in_user_index = driver.find_elements(by=AppiumBy.ID, value="com.xingin.xhs:id/cm5")
            if not is_in_user_index:
                is_nickname_exist[0].click()
                is_in_user_index = driver.find_elements(by=AppiumBy.ID, value="com.xingin.xhs:id/cm5")
            xhs_id = is_in_user_index[0].text
            # driver.find_element(by=AppiumBy.ID, value="com.xingin.xhs:id/cli").click() # 返回评论区
            driver.back() # 返回评论区
            comment = comment.split(' ')
            ipaddr = comment.pop()
            date = comment.pop()
            if date == ' ':
                date = comment.pop()
            if comment[-1] == '昨天':
                date = comment.pop() + date
            comment = ''.join(comment)
            common = {
                "标题": title,
                "用户名": nickname,
                "评论": comment,
                "IP地址": ipaddr,
                "评论日期": date,
                "小红书号": xhs_id
            }
            comment_list.append(common)
            wordCloud_Analysis_text += comment
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
    print('进入帖子')
    title = driver.find_element(by=AppiumBy.ID, value="com.xingin.xhs:id/cb2").text # 帖子标题
    driver.find_element(by=AppiumBy.ID, value="com.xingin.xhs:id/c_e").click() # 进入评论区

    is_end = False # 评论区到底标志

    firstComments = driver.find_elements(by=AppiumBy.ID, value="com.xingin.xhs:id/cgl")
    print(f'当前屏有{len(firstComments)}条评论')
    # 一开始就 0 条评论，点击评论区后无法操作，需要触屏一次才能继续才做，且评论区到底
    if len(firstComments) == 0:
        driver.find_elements(by=AppiumBy.ID, value="android:id/content")[0].click()
        is_end = True
    
    while is_end is not True:
        firstComments = driver.find_elements(by=AppiumBy.ID, value="com.xingin.xhs:id/cgl")
        print(f'当前屏有{len(firstComments)}条评论')
        if driver.find_elements(by=AppiumBy.ID, value="com.xingin.xhs:id/bdo") or len(firstComments) == 0:
            is_end = True
        
        get_current_screen(title, firstComments)
        swipe_up(driver)
        time.sleep(2)

    driver.back()

# 继续找帖子
swipe_up(driver)

el4 = driver.find_elements(by=AppiumBy.ID, value="com.xingin.xhs:id/cab")
# len(el4)
print(f"有{len(el4)}条帖子")


for item in el4:
    print()
    item.click() # 进入帖子
    print('进入帖子')
    title = driver.find_element(by=AppiumBy.ID, value="com.xingin.xhs:id/cb2").text # 帖子标题
    driver.find_element(by=AppiumBy.ID, value="com.xingin.xhs:id/c_e").click() # 进入评论区

    is_end = False # 评论区到底标志

    firstComments = driver.find_elements(by=AppiumBy.ID, value="com.xingin.xhs:id/cgl")
    print(f'当前屏有{len(firstComments)}条评论')
    # 一开始就 0 条评论，点击评论区后无法操作，需要触屏一次才能继续才做，且评论区到底
    if len(firstComments) == 0:
        driver.find_elements(by=AppiumBy.ID, value="android:id/content")[0].click()
        is_end = True
    
    while is_end is not True:
        firstComments = driver.find_elements(by=AppiumBy.ID, value="com.xingin.xhs:id/cgl")
        print(f'当前屏有{len(firstComments)}条评论')
        if driver.find_elements(by=AppiumBy.ID, value="com.xingin.xhs:id/bdo") or len(firstComments) == 0:
            is_end = True
        
        get_current_screen(title, firstComments)
        swipe_up(driver)
        time.sleep(2)

    driver.back()


time.sleep(3)



driver.quit()

df = pd.DataFrame(comment_list)

# 将数据写入Excel文件
df.to_excel('comments.xlsx', index=False)

# 输入词频词云分析文档
fileOut = open('./wordCloud-req/分析文档.txt', 'w', encoding='UTF-8')
fileOut.write(wordCloud_Analysis_text)
fileOut.close()
