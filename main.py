import platform, time
from selenium import webdriver
import requests
#配置
suofang = 1.5 #电脑缩放率
kname = '****'#考生名字
kksh = "****"#考生号
ksfz = "******"#身份证号
kpass = "****"#成电网站密码
sendkey = 'SCT****' #在https://sct.ftqq.com/网站中登录可以找到
workpath = 'D:\\OneDrive\\' #chromedriver、图片保存目录

#防识别自动化控制， 返回一个browser对象
def start_browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation' ])
    options.add_argument("-disable-blink-features-AutomotionControlled")
    if platform.system() == "Windows" :
        browser = webdriver.Chrome(executable_path=workpath+"Chromedriver.exe", options=options)
    else:
        browser = webdriver.Chrome(executable_path="./webdriver/Chromedriver", options=options)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source":"""
                        object. defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                        ))
                """
    })
    return browser  

def succeed(browser,website):
    browser.maximize_window( )
    filename = str(time.time()) + '.png'
    browser.save_screenshot(workpath+filename)
    send(website+"成绩已出","成绩已查询到，前往电脑查看")
         
def send(title, content):
    
    url = 'https://sctapi.ftqq.com/'+sendkey+'.send'
    data = {
        "text":title,
        "desp":content,
        "channel":"9|18"
    }
    requests.post(url,data=data)
