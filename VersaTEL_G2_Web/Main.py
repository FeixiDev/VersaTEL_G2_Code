# -*- coding: utf-8 -*-
from versatelG2 import app

if __name__ == '__main__':
  app.run(host='0.0.0.0',  # 任何ip都可以访问
      port=7777,  # 端口
      debug=True
      )

