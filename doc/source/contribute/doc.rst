文档
====


项目文档是一个 `Sphinx <http://sphinx-doc.org/index.html>`_ 项目，使用 `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ 格式编写文档内容。API文档则使用sphinxcontrib-pecanwsme、sphinxcontrib-docbookrestapi、sphinxcontrib-httpdomain等插件自动生成（需要在代码中编写docstring）。

项目文档可以使用以下命令生成。

::

    tox -e docs --develop

默认输出html、man两种格式的文档，分别输出到build/sphinx目录下的html和man子目录中。


