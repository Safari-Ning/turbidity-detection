import os
from App import create_app
from flask_cors import CORS

env = os.environ.get("FLASK_ENV","develop")

app = create_app(env)
CORS(app,resources=r'/*')  #解决跨域问题

if __name__ =='__main__':
    app.run() 