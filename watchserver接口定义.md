#watchserver服务器

---

###1. 用户
路径|参数|方法|返回|功能描述
:---:|:---:|:---:|:---:|---
signup|username，email，password|post|ok|注册
signin| username，password|post|userId|登录


###2. 设备发出（也即服务器需要响应处理以下请求）
路径|参数|方法|返回|功能描述
:---:|:---:|:---:|:---:|---
online|deviceId|get|ok|手机上线，通知服务器。服务器需要保存设备状态，因为当用户从网页发送请求指令时，需要根据设备状态来决定动作：设备在线，马上把指令发送出去，否则放入暂存队列，等待设备上线后再发送
offline|deviceId|get|ok|手机下线，这个消息不一定会发送，但是一旦发送，立刻把状态改为“下线状态”
heartbeat|deviceId|get|ok|每隔1分钟发送一次的心跳信号，证明设备在线。若超过`3次`没有收到信号，则更改状态为“下线”
bind|deviceId|get|ok|绑定设备，将用户和对应的设备绑定，所有从服务器发出的指令都需要用设备ID来标识（最好能做成一个用户能绑定多个设备）

###3. 服务器发出（通过信鸽推送）
因为消息只是一串字符串，所以我们需要约定解析这个消息的格式。

暂时约定使用类似json的格式：
路径+'{'+参数名+':'+参数内容+','+参数名+','+参数内容...+'}'

例如请求file_upload的，使用以下消息格式：

	file_upload{deviceId:sa4d33tre2,filePath:/sdcard/folder/test.txt}

下面的参数做了更改，因为仅使用设备ID就可以唯一确定手机，而用户验证在服务器下发推送时已经指定了。

路径|参数|功能描述
:---:|:---:|---
gps|deviceId|请求设备GPS数据
alarm|deviceId|控制手机响铃
disalarm|deviceId|控制响铃关闭
lock|deviceId|锁定手机
unlock|deviceId|解锁手机
erase|deviceId|擦除手机数据。这个功能由于太危险，在网页操作时需要弹小窗输入用户密码后才能发送
state|deviceId|查询手机`安全状态`，分为“safe”和“danger”两个。这个仅仅是为了在网页上显示更好看一点，也可以舍去
file_list|deviceId|请求手机的文件列表，手机返回SD卡上的文件目录，使用json格式保存
file_upload|deviceId，filePath|请求手机SD卡上该文件路径的文件

当手机收到以上的推送消息时，向服务器发起对应的以下链接，并把请求的数据上传：

消息命令|对应服务器请求路径|参数|方法|返回|功能描述
:---:|:---:|:---:|:---:|:---:|---
gps|gps|latitude，longitude|get|无需返回|上传gps数据，double格式，对应表示经纬度
alarm|alarm|没有|get|无需返回|表示已经响应了alarm请求，手机成功开启响铃
disalarm|disalarm|没有|get|无需返回|同上
unlock|unlock|没有|get|无需返回|同上
erase|erase|没有|get|无需返回|同上
state|state|state|get|无需返回|state只有两种内容：safe和danger
file_list|file_list|deviceId|post|ok|json
file_upload|file_upload|userId, deviceId, filePath, fileName|post|ok|这个还得再商量怎么设计，如果有比较好的方案就直接用吧，我以前倒是在picker里边做过文件上传，但是当时出了挺多bug


---
###服务器总体结构
![server](/Users/ay27/Downloads/server_img/server - New Page.png)

###绑定手机
![bind](/Users/ay27/Downloads/server_img/server_bind_server - New Page.png)

###服务器需要保存手机的两种状态
![state](/Users/ay27/Downloads/server_img/server_device_state - New Page.png)

###服务器向手机发送离线指令
![send_cmd](/Users/ay27/Downloads/server_img/server_send_cmd - New Page.png)

###文件上传
![file_upload](/Users/ay27/Downloads/server_img/server_file_upload - New Page.png)

---
##附上我们作品报告里关于服务器的描述
###功能概述服务器作为用户与失窃手机交互的桥梁，起着不可忽视的作用。用户可通过服务器获取失窃手机的位置信息，控制其响铃，擦除数据，拉取重要文件等。尽可能帮助用户保护手机上的重要数据，并寻回手机。
###功能实现服务器由以下模块组成：
1.	用户管理模块，完成用户注册，登录；2.	设备管理功能模块，完成设备绑定，获取GPS数据，控制响铃，数据上传，文件存储，远程数据擦除功能；3.	设备连接模块，完成指令暂存，伺机下发指令。