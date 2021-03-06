#coding=utf8

from setuptools import setup

try:
    long_description = open('README.md', encoding='utf8').read()
except Exception as e:
    print(e)
    long_description = ''

setup(
    name='easyserializer',
    version='0.2.15',
    description='serialize a object | 简易对象序列化工具',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='tao.py',
    author_email='taojy123@163.com',
    maintainer='tao.py',
    maintainer_email='taojy123@163.com',
    install_requires=['six'],
    license='MIT License',
    py_modules=['easyserializer'],
    platforms=["all"],
    url='https://github.com/taojy123/EasySerializer',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
)
