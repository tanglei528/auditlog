审计日志过滤器
==============

审计日志过滤器用于采集各个API服务中用户的行为日志，基于 `WSGI中间件 <http://en.wikipedia.org/wiki/Web_Server_Gateway_Interface>`_ 技术实现，可以在不侵入API实现代码的前提下完成审计日志采集。

每个middleware只需要实现下面的接口：

::

    class Middleware(object):
        def process_request(self, req):
            pass
        def process_response(self, response):
            pass

precess_request方法中采集用户信息、项目信息、请求资源、方法、请求内容、开始时间，process_response方法中采集处理结果、完成时间，并存储到数据存储。

但是，各个API项目对中间件的实现进行了封装，导致项目无法实现一个适用于所有API项目的过滤器，目前只能在项目中引入各个API定义的过滤器基类，并针对每个API服务实现一个过滤器。
