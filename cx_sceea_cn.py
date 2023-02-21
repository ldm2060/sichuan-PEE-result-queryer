# encoding=utf-8
import os
from time import sleep 
import ddddocr
from PIL import Image
from main import suofang, ksfz, start_browser, succeed, send, kksh, kname,workpath

ocr = ddddocr.DdddOcr()

issuccess = False

def process(browser):
    global issuccess
    url = "https://cx.sceea.cn/html/YJCJ.htm"
    browser.get(url)
    browser.switch_to.window(browser.window_handles[0])
    browser.find_element('id', 'ksh').send_keys(kksh)
    browser.find_element('id', 'sfzh').send_keys(ksfz)
    browser.find_element('id', 'input_ValidateCode').click()
    sleep(1)
    rpic = browser.find_element('id', 'ranImg')
    loc = rpic.location
    size = rpic.size
    left = loc['x']*suofang
    top = loc['y']*suofang
    right = (loc['x'] + size['width'])*suofang
    botom = (loc['y'] + size['height'])*suofang
    val = (left, top, right, botom)
    result = "1"
    while(len(result) != 4):
        browser.find_element('id', 'kbq').click()
        sleep(1)
        browser.save_screenshot(workpath+'login.png')
        login_pic = Image.open(workpath+'login.png')
        #通过上下左右的值，去截取验证码
        yzm_pic = login_pic.crop(val)
        login_pic.close()
        yzm_pic.save(workpath+'login.png')
        login_pic = open(workpath+'login.png', 'rb')
        img_bytes = login_pic.read()
        login_pic.close()
        result = ocr.classification(img_bytes)
    os.remove(workpath+'login.png')
    browser.find_element('id', 'input_ValidateCode').send_keys(result)
    #browser.find_elements_by_class_name("btn")[0].click()
    browser.execute_script("window.open('YJCJResult.htm');");
    sleep(1)
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    if kname in browser.page_source:
       succeed(browser,"省教育考试院")
       issuccess = True
    #succeed(browser,"省教育考试院")
 
def main():
    browser = start_browser()
    while True:
        if issuccess:
            break
        process(browser)
    if issuccess != True:
        send("错误","查询成绩出错")
        browser.quit()

main()
