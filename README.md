# 点睛网律师职业申请课程自动播放/自动刷课
本代码是基于点睛网网页结构，利用python+selenium实现网站自动登录和视频自动播放。本项目仅供学习交流，禁止用以商业盈利！

## 改动说明
1. 基于原版修改为适配 https://sqzy.zfwx.com/wxqt/ 申请律师职业的版本
2. 适配了4.0版本以上的selenium
3. 增加了视频播放切换为2倍速的功能

## 使用说明
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