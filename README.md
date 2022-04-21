放我出去！工作日自动发送临时出入校申请【北邮】
---

受够了每日自己填写临时出入校申请，做了一个按需自动提交申请的小玩具——

锵锵！

1. 依靠selenium获取登陆后的cookie，使用requests库向服务器提交信息
2. 自动查找辅导员和导师工号（如果出错那就说明导师和辅导员是大众名字，建议自己填一下）。
3. 按需发送临时出入校申请，今天发明天的申请，永远快人一步，不会被卡在门口
4. 节假日不发申请，休息。



**本脚本只能自动发申请给辅导员，至于辅导员批不批你的申请那就无能为力了。**



哦我亲爱的朋友，如果您也想解放双手，首先请安装一些依赖库和chromedriver：

```
pip install -r requirements.txt
```

按自己的chrome浏览器版本下载chromedriver：

```
https://chromedriver.chromium.org/
```

随后将自己的基本信息填入settings文件：

```python
#  Copyright (c) 2022 by Chiayen
# 学号
STUDENT_ID = ''
# 密码
PASSWORD = ''
# 手机号
MOBILE_NUMBER = ''
# 辅导员姓名
COUNSELOR_NAME = ''
# 导师姓名
MENTER_NAME = ''
# 外出去向
DESTINATION = ''
# 外出原因
REASON = ''
# 出校时间 只支持整数 24小时制
OUT_TIME = 9
# 入校时间 只支持整数 24小时制
BACK_TIME = 22
# 星期几出入校？留空默认天天出校
# 0=星期一 1=星期二 2=星期三 3=星期四 4=星期五 5=星期六 6=星期日
WANT_OUT_WEEKDAY = []
```

再设置定时启动（以windows为例）

1. 打开`自动申请出入校.xml`
2. 设置`StartBoundary`为你自己想几点发申请给辅导员
3. 更改`Command`为你自己的python地址
4. 更改`Arguments`为main脚本的绝对路径
5. 保存后打开任务计划程序，选择导入任务。导入修改后的`自动申请出入校.xml`。
6. 成功！



#### 一些其他的碎碎念：

如果有问题可以自行修改脚本和代码，或者提issue~

