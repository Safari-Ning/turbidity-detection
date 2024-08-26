from flask import Flask
from App.views import init_view
from App.settings import envs

def create_app(env):

    app = Flask(__name__)
    #加载配置
    app.config.from_object(envs.get(env))
    #初始化路由
    init_view(app) 

    return app