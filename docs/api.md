# API 文档

1. 所有的请求都可以带上 `gps` 参数
2. 所有的请求都必须包含 `deviceid` 参数
2. 除了文件上传以外的请求全部使用 `GET`

## 设备 API 列表

1.  `/heartbeat`  
    发送心跳包,不返回任何值  

    ```
	GET /heartbeat?gps=<latitude>|<longtitude>&devieceid=<RandomString>
	```

2. `/offline`  
   设备下线

   ```
   GET /offline?gps=<latitude>|<longtitude>&devieceid=<RandomString>
   ```

3. `/online`
	设备上线

	```
	GET /online?gps=<latitude>|<longtitude>&devieceid=<RandomString>
	```

4. `/upload_file`
   上传文件

5. `/push_file_list`
   上传文件列表

6. `/bind`
   绑定设备

   ```
   GET /bind?gps=<latitude>|<longtitude>&devieceid=<RandomString>&uid=<userid>
   ```

## 用户 API

1. `/signin`
	用户登录

    ```
    POST /signin_device
	```
    ```
    {
        "err": 0,
        "msg": "登陆成功",
        "user": {
            "devices": [],
            "email": "pandada8@gmail.com",
            "uid": 1,
            "username": "pandada8"
        }
    }
    ```
2.
