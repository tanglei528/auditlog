安装
====

二进制安装
----------

项目会以rpm二进制包格式发布，在支持yum包管理工具的发行版中，
配置必要的软件源的前提下，可以使用以下步骤进行安装。

::

    yum install auditlog

Python源码包安装
----------------

Python源码包是一个tar.gz格式的压缩包，可以使用setuptools进行安装，
步骤如下：

::

    tar zxvf auditlog.<version>.tar.gz
    cd auditlog*
    python setup.py install

