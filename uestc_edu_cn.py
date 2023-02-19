# encoding=utf-8
import os
from time import sleep 
import ddddocr
from PIL import Image
from main import suofang, ksfz, kpass, start_browser, succeed, workpath

def process():
    global limit
    ocr = ddddocr.DdddOcr()
    browser = start_browser()
    url = "https://zsgl.uestc.edu.cn/ksxt/login.aspx"
    try:
        browser_curl = browser.current_url
    except:
        browser_curl = "1"
    while(browser_curl != "https://zsgl.uestc.edu.cn/ksxt/Default.aspx"):
        browser.get(url)
        browser.find_element('id', 'txtPassWord').send_keys(kpass)
        browser.find_element('id', 'txtLoginName').send_keys(ksfz)
        rpic = browser.find_element('id', 'myCode')
        loc = rpic.location
        size = rpic.size
        left = loc['x']*suofang
        top = loc['y']*suofang
        right = (loc['x'] + size['width'])*suofang
        botom = (loc['y'] + size['height'])*suofang
        val = (left, top, right, botom)
        result = "1"
        while(len(result) != 4):
            browser.find_element_by_xpath("//a[contains(text(),'看不清')]").click()
            sleep(1)
            browser.save_screenshot(workpath+'login1.png')
            login_pic = Image.open(workpath+'login1.png')
            #通过上下左右的值，去截取验证码
            yzm_pic = login_pic.crop(val)
            login_pic.close()
            yzm_pic.save(workpath+'login1.png')
            login_pic = open(workpath+'login1.png', 'rb')
            img_bytes = login_pic.read()
            login_pic.close()
            result = ocr.classification(img_bytes)
        os.remove(workpath+'login1.png')
        browser.find_element('id', 'txtyzm').send_keys(result)
        browser.find_element('id', 'btnLogin').click()
        sleep(2)
        try:
            browser_curl = browser.current_url
        except:
            browser_curl = "1"      
    while(True):
        browser.switch_to.default_content()
        browser.switch_to.frame("MenuFrame")
        browser.find_element_by_partial_link_text('初试成绩查询').click()
        browser.switch_to.default_content()
        browser.switch_to.frame("PageFrame")
        if "该功能暂时关闭" not in browser.page_source:
            succeed(browser,"成电网站")
            break
    browser.quit()


def main():
    global limit
    limit = 5000
    process()

main()