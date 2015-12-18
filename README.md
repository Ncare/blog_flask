
基于Flask简单博客系统，目前比较简单。功能还在添加之中....


2015-12-18 跟新
   - 尝试跑在Nginx上，使用uwsgi

   - 使用 virtualenv

   - 配置 nginx.conf 如下

   ```
       server {
        listen       80;
        server_name  www.app.com;

        #charset koi8-r;

        location / {
            include uwsgi_params;
            uwsgi_pass 127.0.0.1:8001;

            uwsgi_param UWSGI_PYHOME /Users/ncare-pc/Code/Python/Flask_blog/venv;
            uwsgi_param UWSGI_CHDIR /Users/ncare-pc/Code/Python/Flask_blog;
            uwsgi_param UWSGI_SCRIPT manager:app;
        }
   ```

   - 添加 uwsgi_config.ini 文件，然后终端 uwsgi uwsgi_config.ini 开启； 
   - 停止 uwsgi 服务   killall -9 uwsgi
 



---
更新:
	- 添加评论管理功能


keep on ...

	- 使用了Bootstrap, jQuery
	- 引入了ckeditor作为编辑器
	- 实现了简单搜索功能
	- 实现分页
	- 添加了标签功能
	- 无刷新评论提交
	- 添加文章时的预览




