# Veisearch 技术无罪
我们不生产资源，我们不存储资源，我们也不是资源搬运工。

### 项目演示地址
+ 项目演示地址：[http://www.veisearch.com/](http://www.veisearch.com/)  
仅界面演示，上传脚本并未执行。由于并未找到可靠的免费代理池，而我写脚本爬取的网站对访问限制比较严重，所以多次尝试后最终放弃在服务器上运行，不过本地运行完全可以。
+ 开发者后台地址：[http://www.veisearch.com/pro/](http://www.veisearch.com/pro/)  
用户可以在后台开发者页面浏览其他用户上传的脚本，并对脚本进行相应的测试，评论，点赞等操作。
+ 代理接口地址：[http://www.veisearch.com/proxy/](http://www.veisearch.com/proxy/)  
将数据库中有效的代理开放给用户在脚本中使用。
+ 网站后台地址：[http://www.veisearch.com/admin/](http://www.veisearch.com/admin/)  
后台采用开源框架[django-simpleui](https://github.com/newpanjing/simpleui)，一款基于vue+element-ui的django admin现代化主题。
  - 账号：admin
  - 密码：admin123456  
### 实现功能
1. 搜索页。当用户选择搜索类型并输入搜索关键词点击搜索时，后台会运行数据库中对应类型的非停止状态下的所有脚本并将结果返回。后台多脚本的执行使用多线程。
2. 开发者后台首页。各种数据的展示，包括滚动条、轮播图、已上传脚本展示、脚本运行情况、系统已安装Python库、最新评论、代理展示。由于后台页面多处属于重复区块，我们将一些重复数据存在session中以减少服务器与数据库的交互，从而加速网页的渲染。
3. 脚本上传页面。用户首先上传脚本文件，系统会将脚本详细内容显示在页面上，用户确认无误后需正确填写脚本相关信息的表单后点击提交。注意脚本的书写格式有硬性要求，否则后台无法调用执行。数据返回格式也需要遵守严格格式。例：电影脚本返回数据格式如下  
```python
[
	{
		"movie_name":"斗破苍穹",    # 电影名
		"movie_size":"1.3G",    # 文件大小
		"thunder_link":"thunder://QUFtYWduZXQ6P3h0PXVybjpidGloOjkyNTcyMDYzNjI4NUVCODBEMUFFMTc1OEM0NzMwQTI0MTIzQTlFOEFaWg==",     # 迅雷链接
		"movie_online_view_address":"https://bili.meijuzuida.com/share/8a27c2ddc3d3fe74aa037f4b7d262e34"    # 在线观看地址
		"source":"80s电影网"       # 资源来源网站
	},
	# 注意，属性获取不到的必须填null；
]
```
4. 脚本列表页。分类展示脚本信息。
5. 脚本详情页。对于不同状态的脚本，会有不同状态的展示，主要体现在脚本测试方面。除此之外，用户可以对脚本进行无登录点赞及评论操作。注意，点赞数据亦存储在session中。展示不同之处如下：
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/success.PNG)  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/error.PNG)  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/stop.PNG)

6. 脚本报错记录。无论用户执行搜索或者在后太对单个脚本进行调试，只要脚本运行系统都会对脚本进行监测，一旦报错会立马记录在数据库。当报错记录超过50条系统会自动修改脚本的状态为`error`，即`出现问题`。同理，当报错记录超过100条系统会自动修改脚本的状态为`stop`，即`停止运行`，并停止脚本的运行。
7. Celery+redis任务管理。  
    1. 邮件任务  
    *因为没有企业邮箱，使用个人邮箱极不稳定*
        1. 当用户上传脚本后脚本处于待审核状态，此时需要管理员对脚本代码进行安全性检查，检查完成后可在后台修改脚本状态。此时系统会给开发者发送邮件提醒用户脚本审核通过
        2. 除此之外，当系统监测到脚本报错次数达到限制后会自动修改脚本状态，此时也会触发邮件事件给上传当前脚本的用户发送邮件进行提醒。 
    2. 代理定时任务
        1. 代理爬取。我们设定每10分钟爬取一批代理并存入数据库。
        2. 测试代理。我们设定每20分钟检测所有库中ip代理。
    ```python
          CELERYBEAT_SCHEDULE = {
        u'获取代理': {
            "task": "vei.tasks.getproxy",
            "schedule": timedelta(minutes=10),
            "args": (),
        },
        u'测试代理': {
            "task": "vei.tasks.proxytest",
            "schedule": timedelta(minutes=10),
            "args": (),
        },
      }
    ```
8. 验证码。使用Pillow模块生成验证码，前端ajax异步调用获取验证码信息（图片及code），将code存入session中用于提交时验证。
9. 代理接口。定时任务自动筛选出可使用的代理，设置一个接口供用户脚本使用。用户每次访问接口可以获取到最新的100条可用代理（若不足100条则有多少显示多少）
### 代理脚本示例
+ [89免费代理](https://github.com/Weibw162/Veisearch/blob/master/proxy_spider/proxy_89ip.py)--->[官网地址](http://www.89ip.cn/)
+ [西刺代理](https://github.com/Weibw162/Veisearch/blob/master/proxy_spider/proxy_xici.py)--->[官网地址](https://www.xicidaili.com/)
+ [站大爷代理](https://github.com/Weibw162/Veisearch/blob/master/proxy_spider/proxy_zdy.py)--->[官网地址](http://ip.zdaye.com/)
### 脚本示例
+ [80s电影网](https://github.com/Weibw162/Veisearch/blob/master/media/spider_files/Spider_80s.py)  
使用requests+threading实现多线程并发爬取
+ [80s电影网](https://github.com/Weibw162/Veisearch/blob/master/media/spider_files/Spider_80s_t.py)  
使用asyncio+aiohttp实现多协程并发爬取

### 网站页面展示
+ 搜索页（PC端）  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/index_pc.PNG)
+ 搜索页（移动端）  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/index_m.PNG)
+ 搜索结果展示（PC端）  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/result_pc.PNG)
+ 搜索结果展示（移动端）  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/result_m.PNG)
+ 开发者后台首页（PC端）  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/pro_pc.PNG)
+ 开发者后台首页（完整展示移动端）  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/pro_m.jpg)
+ 脚本上传页  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/upload.jpg)
+ 脚本详情页  
![](https://github.com/Weibw162/Veisearch/blob/master/readmeimg/detail.jpg)
