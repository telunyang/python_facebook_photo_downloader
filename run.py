import sys, os, time, re
from urllib.request import urlopen
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

# Selenium 初始化
driver = webdriver.Chrome(os.path.join(os.getcwd(), 'plugin\chromedriver.exe'))

# 將視窗放到最大，因為 Facebook 會隨著瀏覽器長寬，來決定不同的圖片尺寸
driver.maximize_window()

# 登入 FaceBook
def loginFacebook(url):
    # 走訪連結
    driver.get(url_login)
    
    # 填入 email 帳號
    elem_email = driver.find_element_by_name("email")
    elem_email.clear()
    elem_email.send_keys("your-facebook-email")
    
    # 輸入密碼
    elem_pass = driver.find_element_by_name("pass")
    elem_pass.clear()
    elem_pass.send_keys("your-facebook-password")
    
    # 按下登入鈕（這個 loginbutton 是個 label）
    elem_btn_login = driver.find_element_by_id("loginbutton")
    elem_btn_login.click()

def parseFriendPhotoPage(url):
    # 走訪連結
    driver.get(url)
    
    # 按下 ESC，讓半透明背景消失
    driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
    
    # 取得 Photo 列表的照片連結
    elm_li = driver.find_elements_by_css_selector("ul._69n li")
    
    # 轉成 list 後進行迭代處理
    for index, li in enumerate(elm_li):
        # 取得圖片連結並按下，使其跳出實際的圖片
        elm_a = li.find_elements_by_css_selector('a._6i9')
        elm_a[0].click()

        # 由於圖片讀取時，縱然未下載完成，也當成讀取完成（FB 可能用串流讀取），
        # 所以這裡單純讓程式停置幾秒，讓圖片可以順利下載，而非縮圖
        time.sleep(3)
        
        # 取得圖片放大後的連結
        elm_img = driver.find_element_by_css_selector('img.spotlight')
        image_src = elm_img.get_attribute("src")
        
        # 用正規表達式，來取得檔案名稱與副檔名
        p = re.compile('([0-9]+[_0-9a-zA-Z]+\.(png|jpg|gif))')
        m = p.findall(image_src)
        
        # 按下關閉圖示，準備開下一張圖片
        driver.find_element_by_css_selector('a._418x').click()
        
        # 下載圖片到本機端
        try:
            image = urlopen(image_src)
            f = open( os.path.join(os.getcwd(), 'downloads/friend/' + m[0][0]), 'wb' )
            f.write( image.read() )
            f.close()
        except:
            print("{} cant't be read".format(m[0][0]))

def parseFanGroupPhotoPage(url):
    # 走訪連結
    driver.get(url)
    
    # 按下 ESC，讓半透明背景消失
    driver.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
    
    # 有時半透明背景消失，需要一點時間，所以刻意停留 1 秒，不然有可能 點擊不到元素
    time.sleep(1)
    
    # 取得粉絲團 All Photos 列表的照片連結
    elm_div = driver.find_elements_by_css_selector("div._2eec div._2eea")
    
    # 轉成 list 後進行迭代處理
    for index, div in enumerate(elm_div):
        # 按下圖片圖層上方的 div，使其跳出實際的圖片
        div.click()

        # 由於圖片讀取時，縱然未下載完成，也當成讀取完成（FB 可能用串流讀取），
        # 所以這裡單純讓程式停置幾秒，讓圖片可以順利下載，而非縮圖
        time.sleep(3)
        
        # 取得圖片放大後的連結
        elm_img = driver.find_element_by_css_selector('img.spotlight')
        image_src = elm_img.get_attribute("src")
        
        # 用正規表達式，來取得檔案名稱與副檔名
        p = re.compile('([0-9]+[_0-9a-zA-Z]+\.(png|jpg|gif))')
        m = p.findall(image_src)
        
        # 按下關閉圖示，準備開下一張圖片
        driver.find_element_by_css_selector('a._418x').click()
        
        # 下載圖片到本機端
        try:
            image = urlopen(image_src)
            f = open( os.path.join(os.getcwd(), 'downloads/fan_group/' + m[0][0]), 'wb' )
            f.write( image.read() )
            f.close()
        except:
            print("{} cant't be read".format(m[0][0]))

try:
    # 登入頁面
    url_login = 'https://www.facebook.com/'
    loginFacebook(url_login)
    
    # 分析照片頁面
    #url_photo = 'https://www.facebook.com/DarrenYang1002/photos'
    #parseFriendPhotoPage(url_photo)
    
    # 粉絲團照片一覽
    #url_photo_fan_group = 'https://www.facebook.com/pg/turtledrawturtle/photos/'
    #parseFanGroupPhotoPage(url_photo_fan_group)
    
except TimeoutException:
    print("TimeoutException: \n", sys.exc_info())

except WebDriverException:
    print("WebElementException: \n", sys.exc_info())

except NoSuchElementException:
    print("NoSuchElementException: \n", sys.exc_info())

except:
    print("Unexpected error: \n", sys.exc_info())
    
finally:
    driver.quit()