开发相关
========

从源代码运行项目
----------------

在开发进程中会经常修改代码，需要能够立即运行最新的代码以检查实现，项目建议使用虚拟环境运行项目，具体步骤如下：

1. 安装mongo

::

   yum install -y mongodb mongodb-server
   service mongod start
2. 安装虚拟环境以及依赖

::

   python tools/install_venv.py
3. 准备配置文件

::

   mkdir /etc/auditlog
   cp etc/auditlog/* /etc/auditlog


4. 修改配置

按照 :ref:`configuration` 修改上面的配置文件

5. 启动服务

::

   source .venv/bin/activate
   python tools/run_server.py


其它内容
--------

.. toctree::
   :maxdepth: 1

   package
   test
   doc
   ../sourcecode/autoindex
