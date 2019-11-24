# ihome

爱家租房项目案例学习



##### 环境

python3,  redis数据库， mysql数据库

##### 使用方式

python manage.py runserver -h 运行ip地址 -p 运行端口

##### 介绍

使用redis数据库保存缓存信息, 如session，图片验证码,  短信验证码等

使用mysql数据库保存用户, 房屋, 城区, 房屋, 设施等等信息

使用容联云第三方短信平台

### 依赖

captcha==0.3

cos-python-sdk-v5==1.7.5

Flask==0.10.1
Flask-Login==0.4.1
Flask-Migrate==2.5.2
Flask-Script==2.0.6
Flask-Session==0.3.1
Flask-SQLAlchemy==2.4.0
Flask-WTF==0.14.2

PyMySQL==0.9.3

redis==3.3.11

SQLAlchemy==1.3.8