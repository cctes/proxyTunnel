proxyTunnel
===========

## 写在前面
一直想写个可以通过单一的代理配置实现ip的变换，这算是个测试版吧，基本功能应该算是实现了，如果有啥建议希望能告诉我
个人的第一个git项目

## 依赖
requests

## 怎么用
``` sever = socket.socket()
    host = "127.0.0.1"        
    port = 3080            //配置监听端口
    sever.bind((host,port))
```

```def getPX():        //按照我的格式返回ip和port
    p = requests.get("http://127.0.0.1:5010/get/").json().get("proxy")
    p = str(p)
    ip = str(p.split(":")[0])
    port = int(p.split(":")[1])
    print("new ip is:" + ip + ":" + str(port))
    return ip,port
```




