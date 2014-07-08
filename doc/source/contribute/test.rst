测试
====

项目使用 `tox <http://tox.testrun.org/>`_ 管理测试流程。项目配置了py26、py27、pep8、cover、docs虚拟python环境，默认运行py26、py27、pep8三个的测试。

.. _run_all_tests:

运行测试
--------

执行以下命令，进行所有测试并执行静态代码审查。
::

    tox --develop

选项 --develop用于临时将项目安装到python的模块搜索路径上。
如果项目依赖有变化，修改了requirements.txt或者test-requirements.txt文件，需要重新配置虚拟环境，可以在tox命令中使用 -r 参数。

运行代码审查
-----------

如果想单独执行静态代码审查，可以执行以下命令。
::

    tox -e pep8

统计代码覆盖率
--------------

项目使用coverage统计代码覆盖率，执行以下命令进行统计。
::

    tox -e cover --develop

默认生成html格式的报告，使用浏览器打开cover/index.html查看。


调试代码
--------

可以使用pdb调试代码，只需要在期望的断点位置插入以下语句，然后 :ref:`run_all_tests` 就可以进行调试了。
::

    import pdb; pdb.set_trace()
