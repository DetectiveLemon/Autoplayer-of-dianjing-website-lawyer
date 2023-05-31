# -*- coding: utf-8 -*-

# Original Author: github.com/JTsolon
# Update: github.com/DetectiveLemon
# Date: 2023-05-26

'''
使用说明
1. 安装Python, 安装时勾选 add python to path.
2. 把这个.py文件丢到一个文件夹里, 文件夹最好是英文.
3. 在文件夹里Shift + 右键, 在此处打开powershell(或者在此处打开cmd命令提示符).
4. 输入运行以下命令.
5. `pip config set global.index-url https://mirrors.aliyun.com/pypi/simple`
6. `pip install selenium`
7. 等待依赖安装完成
8. 修改代码里的用户名密码
9. 修改从哪节课和哪个视频开始看, 分别从上往下从0开始数 变量: v_start (第几门课) sub_v_start (这门课中第几个视频)
10. 输入 `python autoplay_videos_pro.py` 运行脚本, 尽量不要操作自动打开的chrome窗口, 以免影响脚本的运行
'''

'''
修改日志：
修改了方法名, 适配4.0以上版本的selenium
修改了部分元素的xpath, 适配点睛网执业律师页面
增加视频播放自动切换2倍速功能, 增加刷课效率

在login函数中修改了登陆网址，目前是进入第二页，所以添加了进入第二页的语句，if和else语句中都要添加
v_start和sub_v_start两个参数分别指定初始的大视频和子视频，视视频播放进度，随时可能会手动修改
增添第二页后，可能的Bug是无法自动在第二页的大视频之间自动循环播放，可能的原因是在当前页点击’返回课程列表‘后，返回的可能是第一页，所以可能需要在for循环的末相应语句后面添加进入第二页语句
后期要从第一页开始时，要注意注释点login函数的进入第二页语句和for循环末的相应语句

'''
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import time

#login函数中，如果需要进入其他页面，比如第二页，则在if和else语句末都加入转页语句，不需要时，记得注释掉
def login(driver,login_times):
    '''登陆网站并进入选课中心'''
    elem=driver.get(r'http://sqzy.zfwx.com/wxqt/')
    #这里需要休眠15秒，等待浏览器打开
    time.sleep(5)
    
    if login_times>1:
        elem=driver.find_element(By.XPATH, r'/html/body/div[2]/div[1]/div[1]/div/div[2]/div/a')
        elem.click()
        time.sleep(5)
        #调换driver的控制权
        handles = driver.window_handles
        driver.switch_to.window(handles[-1])
        #获取‘听课中心’对象，并点击进入
        elem = driver.find_element(By.XPATH, r'//*[@id="ng-app"]/body/div[3]/div[3]/div[1]/div[2]/ul/li[2]/a')
        elem.click()                         
        time.sleep(5)
        
        #由于第一页听完，点击进入第二页
        # elem = driver.find_element(By.XPATH, r'//*[@id="ng-app"]/body/div[3]/div[3]/div[2]/div/div/div[2]/div[2]/i[2]')
        # elem.click()
        # time.sleep(5)
        #转换控制权到新的页面
        #handles = driver.window_handles
        #driver.switch_to_window(handles[-1])
    else:
        #获取登录框
        elem = driver.find_element(By.XPATH, r'/html/body/div[2]/div[1]/div[1]/div/div[2]/a[1]')
        elem.click()
        time.sleep(3)
        
        #获取用户名框对象，并清空后输入用户名
        elem = driver.find_element(By.XPATH, r'//*[@id="username"]')
        elem.clear()
        elem.send_keys('your username')
        time.sleep(2)
        
        #获取密码框对象，清空后输入密码
        elem = driver.find_element(By.XPATH, r'//*[@id="password"]')
        elem.clear()
        elem.send_keys('your password')
        time.sleep(2)
        
        #获取登录键对象，并点击登录
        #print('开始登陆...')
        elem = driver.find_element(By.XPATH, r'//*[@id="login-form"]/p[5]/input')
        elem.click()
        time.sleep(5)
        
        #获取‘听课中心’对象，并点击进入
        elem = driver.find_element(By.XPATH, r'//*[@id="ng-app"]/body/div[3]/div[3]/div[1]/div[1]/ul/li[2]/a')
        elem.click()
        time.sleep(5)
        
        #由于第一页听完，点击进入第二页
        # elem = driver.find_element(By.XPATH, r'//*[@id="ng-app"]/body/div[3]/div[3]/div[2]/div/div/div[2]/div[2]/i[2]')
        # elem.click()
        # time.sleep(5)

class alert_or_relogin:
    def __call__(self,driver):
        '''用来结合webDriverWait判断是否出现alert或者需要重新登陆'''
        is_alert=bool(EC.alert_is_present()(driver))
        if is_alert:
            return True
        else:
            is_invisible=EC.invisibility_of_element_located((By.XPATH,'//*[@id="repeatcourseDialog"]/div/div[3]/a'))(driver)
            is_visible=not bool(is_invisible)
            if is_visible:
                return True
            else: return False
#test
'''v_elems[1].click()
vl_2=v_elems[1].find_element_by_css_selector("[class='videoList of ng-scope']")
print(len(vl_2))'''

#启动浏览器
driver=webdriver.Chrome()
# driver=webdriver.ChromiumEdge()

#状态变量
v_start=0 #大视频起始下标
sub_v_start=0 #子视频起始下标
login_times=0
quit_normal=False
while True:
    #定义变量以用来判断是否是第一次登录
    try_times=0
    login_times+=1
    
    #登录并进入听课中心
    login(driver,login_times)

    #对每个顶层视频进行循环处理
    for i in range(v_start,10):
       
        #获取整个table对象,这里可能返回后但是并非课程列表页面，若此，则触发异常并捕获，在处理器中重新进入选课中心的课程列表页面
        try:
            table=driver.find_element(By.CLASS_NAME, 'courseCont')
            #获取table内的所有视频顶层逻辑，目前是10个
            v_elems=table.find_elements(By.ID, 'd1')
            if len(v_elems)==0:raise Exception
        except:
            #获取‘听课中心’对象，并点击进入
            elem = driver.find_element(By.XPATH, r'//*[@id="ng-app"]/body/div[3]/div[3]/div[1]/div[2]/ul/li[2]/a')
            elem.click()
            time.sleep(5)
            table=driver.find_element(By.CLASS_NAME, 'courseCont')
            #获取table内的所有视频顶层逻辑，目前是10个
            v_elems=table.find_elements(By.ID, 'd1')
    
        #获取每个顶层逻辑下的子逻辑
        v=v_elems[-10+i]
        v.click() #需要先点击一个子逻辑，之后网页才会出现以下选取对象的元素，不然不会出现子逻辑
        
        #休眠8秒等待页面加载
        time.sleep(8)
        
        sub_v=v.find_element(By.CLASS_NAME, 'courseVideo')
        
        #获取子逻辑下的所有子视频的逻辑
        videos=sub_v.find_elements(By.CSS_SELECTOR, "[class='videoList of ng-scope']")
        
        #获取播放对象
        player=videos[sub_v_start].find_element(By.CLASS_NAME, 'player')
        
        #点击播放，并让程序休眠播放时长，然后再循环播放下一个视频
        player.click()
        time.sleep(1) #如果再次出错，导致alert窗口没有被点击的话，原因可能是这里休眠的时间过长，导致网页alert窗口早就出现，但是程序还未到等待语句，而等待语句在alert窗口出现之后再运行就会失效了
        
        #本视频没有听完，从中继续接着听,如果抛出异常，说明是不需要接着听，或者出现了‘重复听课不计入课时’的提示，两种情况都可以交给except中的语句处理
        
        #如果因为中途中断，则出现'重复听课不计入课时’的提示，点击确定键
        try:
            #print('run here!')
            #handles = driver.window_handles
            #driver.switch_to.window(handles[-1])
            invisib=EC.invisibility_of_element_located((By.XPATH,r'//*[@id="ng-app"]/body/div[3]/div[3]/div[2]/div/div/div[4]/p[3]/a[2]'))(driver)
        except:
            invisib=True
        if not bool(invisib):
            elem=driver.find_element(By.XPATH, r'//*[@id="ng-app"]/body/div[3]/div[3]/div[2]/div/div/div[4]/p[3]/a[2]')           
            elem.click()
            #time.sleep(2)
            handles = driver.window_handles
            try_times+=1
            if try_times>1:
                driver.close()
            driver.switch_to.window(handles[-1])
            WebDriverWait(driver,timeout=25,poll_frequency=1).until(EC.alert_is_present())
            driver.switch_to.alert.accept()
        #本视频没有听完，从中继续接着听
        else:
            #获取所有句柄，并关闭当前页面，然后把driver的控制对象转换成新出现的页面        
            try_times+=1
            if try_times>1:
                driver.close()
            handles = driver.window_handles
            driver.switch_to.window(handles[-1])
            try:
                WebDriverWait(driver,timeout=20,poll_frequency=1).until(EC.alert_is_present())
                driver.switch_to.alert.accept()
            except:
                print('if the script exits, here maybe wrong, line 206!')
                #WebDriverWait(driver,timeout=20,poll_frequency=1).until(EC.alert_is_present())
        
        #捕获弹出框，并确认运行flash
        #WebDriverWait(driver,timeout=60,poll_frequency=10).until(EC.alert_is_present())
        #driver.switch_to_alert().accept()
        bool_flag=False
        while sub_v_start<len(videos):
            #test_1=bool(driver.find_elements(By.XPATH, r'//*[@id="repeatcourseDialog"]/div/div[3]/a'))
            #test_2=EC.alert_is_present()(driver)
            locator=(By.XPATH,'//*[@id="repeatcourseDialog"]/div/div[3]/a')
            bool_test_1=alert_or_relogin()(driver)

            #视频播放速度切换2x
            time.sleep(3)
            move = driver.find_element(By.CLASS_NAME, r'my_mask')
            ActionChains(driver).move_to_element(move).perform()
            play_speed_current = driver.find_element(By.CLASS_NAME, r'current-rate')
            play_speed_current.click()
            play_speed_switch = driver.find_element(By.XPATH, r'//*[@class="rate-components"]/ul/li[1]')
            play_speed_switch.click()

            try:
                WebDriverWait(driver,timeout=240*60,poll_frequency=5).until(alert_or_relogin())
            except:
                print('Here is wrong! line 229')
                bool_test_2=alert_or_relogin()(driver)
            #test_3=bool(driver.find_elements(By.XPATH, r'//*[@id="repeatcourseDialog"]/div/div[3]/a'))
            #test_4=EC.alert_is_present()(driver)
            time.sleep(5)
            
            if EC.alert_is_present()(driver):
                #如果是该视频列表下的最后一个视频，则在弹窗中点击取消
                if sub_v_start==len(videos)-1:
                    driver.switch_to.alert.dismiss()
                    time.sleep(5)
                    if not bool(EC.invisibility_of_element_located(locator)(driver)): #如何可见，即如果出现了重新登陆框的提示
                        #if EC.presence_of_element_located(locator)(driver): #False是等待被写入的条件判断句
                        #driver.switch_to.window(handles[0])
                        v_start=i
                        elem=driver.find_element(By.XPATH, r'//*[@id="repeatcourseDialog"]/div/div[3]/a')
                        elem.click()
                        time.sleep(5)
                        bool_flag=True
                        break
                    else:sub_v_start+=1
                        #break
                else:
                    driver.switch_to.alert.accept()
                    time.sleep(5)
                    sub_v_start +=1
            
            else: #如果出现需要重新登陆，则跳出两个循环重新登录
                #driver.switch_to.window(handles[0])
                v_start=i
                elem=driver.find_element(By.XPATH, r'//*[@id="repeatcourseDialog"]/div/div[3]/a')
                elem.click()
                time.sleep(5)
                bool_flag=True
                break
        if bool_flag:
            driver.switch_to.window(handles[0])
            quit_normal=False
            break
        #返回课程列表
        sub_v_start=0  #初始化子视频索引，因为下一个大视频一定从0开始
        # elem=driver.find_element(By.XPATH, '/html/body/div[1]/a[1]')
        # elem.click()
        driver.close()
        driver.switch_to.window(handles[0])
        time.sleep(5)
        quit_normal=True
    #如果视频播放完毕，则跳出循环
    if quit_normal==True:
        break
    #双重保险，防止判断条件出错，陷入死循环
    #break
    
