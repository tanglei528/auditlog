.. AuditLog documentation master file, created by
   sphinx-quickstart on Thu Jul  3 13:45:09 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

审计日志项目文档
================

审计日志项目是从VSCloud集群各个API服务采集用户的行为日志，
保存并提供给其它工具进行行为审计的项目。
该项目支持云平台的主要API服务，包括nova、glance、neutron、cinder等，
也支持针对将来新增的服务进行扩展。

项目目标
--------

* 非侵入地从API服务采集用户行为
* 通过REST API向第三方发布审计日志，支持条件查询
* 查看审计日志有权限控制
* 对云平台的可管理资源进行分类

文档目录
========

.. toctree::
   :maxdepth: 2

   installation
   configuration
   architecture
   resource
   filter
   api/index
   contribute/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

