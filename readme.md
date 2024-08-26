### 项目架构

1. backend：后端模块(Flask)
   
   - 依赖安装
   
   ```shell
   pip install -r requirement.txt
   ```
   
   - 启动命令
   
   ```shell
   cd backend
   python manage.py runserver -p 5000
   ```

2. frontend：前端模块(Vue+ElementUI)

### Flask

Flask是一个轻量级的Web框架，底层使用Python语言编写。和大部分人所熟知的Django框架不同的，Flask具有简洁、轻巧的特点，并且Flask还具有高度的可定制性。可以通过引入不同的第三方插件来丰富Flask的功能或者简化开发流程。Flask主要有两个核心组件：模板引擎Jinja2和工具包Werkzeug。[Flask中文文档链接](https://flask.net.cn/)

### Vue

Vue.js是一套构建用户界面的渐进式框架。与其他重量级框架不同的是，Vue采用自底向上增量开发的设计。Vue 的核心库只关注视图层，并且非常容易学习，非常容易与其它库或已有项目整合。另一方面，Vue 完全有能力驱动采用单文件组件和Vue生态系统支持的库开发的复杂单页应用。[Vue快速上手指南](https://cn.vuejs.org/guide/quick-start.html)

### ElementUI

Element-Ul是国内饿了么前端团队推出的一款基于Vue.js 2.0 的桌面端UI框架，一套为开发者、设计师和产品经理准备的基于 Vue 2.0 的桌面端组件库。[ElementUI说明文档](https://element.eleme.cn/2.13/#/zh-CN/component/installation)

### 功能简介

通过选取特定待检测图片并上传后端服务器

### 更新需求

第1，检测结果图片放到下面表格中，这样的话，后续如果点击表格中的数据，可以查看详细的检测结果；

第2，流程上再优化下，体现选择图像、图像预处理（支持多种预处理方式）、浊度检测（包括图像上传和浊度检测两个功能），界面上的名字尽量用这三个：选择图像、图像预处理、浊度检测。其中选择图像、图像预处理，只对当前选择的图像还没有上传的图像做，浊度检测是对预处理后的图像来进行检测
"# turbidity-detection" 
