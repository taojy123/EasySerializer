#coding=utf8

from setuptools import setup
import easyserializer


long_description = """
$ pip install easyserializer

    class Student(object):
        role = 'student'

        def __init__(self, name, birthday):
            self.name = name
            self.birthday = birthday

        @property
        def age(self):
            return int(((datetime.datetime.now().date() - self.birthday).days) / 365)
        

    class Teacher(SerializeableObject):
        role = 'teacher'

        def __init__(self, name, subject, students):
            self.name = name
            self.subject = subject
            self.students = students

    s0 = Student('Dad', datetime.date(1963, 7, 28))
    s1 = Student('Mom', datetime.date(1964, 11, 2))
    t = Teacher('Tao', 'physics', [s0, s1])

    print(t.serialize())

    print(t.to_json(prune=True, limit_deep=2, indent=4))

    print(serialize(t, filter_fields=['name', 'students']))

    print(obj_to_json(s1, exclude_fields=['role']))


"""

setup(
    name='easyserializer',
    version=easyserializer.VERSION,
    description='serialize a object | 简易对象序列化工具',
    long_description=long_description,
    author='tao.py',
    author_email='taojy123@163.com',
    maintainer='tao.py',
    maintainer_email='taojy123@163.com',
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
