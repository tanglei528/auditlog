打包
====

项目使用setuptools创建源代码包和二进制rpm包。由于使用了pbr扩展，发布包的版本号会根据git中的tag或者commit hash生成，因此在正式发布之前需要创建相关版本名称的tag。

开发版本
--------

如果在开发过程中需要临时发布项目，可以直接执行以下命令创建发布包。创建完成的发布包在项目根目录下的dist子目录中。

源代码包
::

    python setup.py sdist

rpm包
::

    python setup.py bdist_rpm

发布版本
--------

在正式发布项目之前，需要先将代码合并到stable分支，并创建以版本号命名的tag，然后执行发布开发版本的打包命令。
