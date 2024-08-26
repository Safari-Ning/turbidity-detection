import os

#设置根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config:
    DEBUG = False
    TESTING = False

#开发环境
class DevelopConfig(Config):
    DEBUG = True 
    

#测试环境
class TestConfig(Config):
    TESTING = True 

#演示环境
class StagingConfig(Config): 
    pass
#生产环境
class ProductConfig(Config):
    pass
envs = {
    "develop": DevelopConfig,
    "testing": TestConfig,
    "staging": StagingConfig,
    "product": ProductConfig,
    "default": DevelopConfig
}