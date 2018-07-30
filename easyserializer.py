#coding=utf8

import json
import six
import datetime
import logging


__all__ = ['SerializeableObject', 'serialize', 'obj_to_json']


"""
简易对象序列化工具
serialize a object 
"""


VERSION = '0.2.1'


class SerializeableObject(object):

    @staticmethod
    def obj2dict(obj, **kwargs):

        prune = kwargs.get('prune', False)                  # 精简模式
        filter_fields = kwargs.get('filter_fields', [])     # 指定输出字段
        exclude_fields = kwargs.get('exclude_fields', [])   # 指定不要输出字段
        limit_deep = kwargs.get('limit_deep', 0)            # 限制递归深度
        current_deep = kwargs.get('current_deep', 0)        # 当前递归深度

        if limit_deep and limit_deep < current_deep:
            # 超出限制递归深度 返回 `[too deep]` 字符串
            return '[too deep]'

        kwargs['current_deep'] = current_deep + 1

        # 可被序列化的类型
        serializeable_types = six.integer_types + six.string_types + (six.text_type,)
        
        # 无法被序列化的类型
        disserializeable_types = (six.binary_type,)

        if isinstance(obj, serializeable_types):
            return obj

        if isinstance(obj, (datetime.datetime, datetime.date)):
            return str(obj)

        if isinstance(obj, list):
            result = []
            for item in obj:
                result.append(SerializeableObject.obj2dict(item, **kwargs))
            return result

        if isinstance(obj, dict):
            result = {}
            for sub_key, sub_value in value.items():
                result[sub_key] = SerializeableObject.obj2dict(sub_value, **kwargs)
            return result

        if isinstance(obj, disserializeable_types):
            # 无法被序列化的字段，以一个 `-` 表示
            return '-'

        # 这里上面应该更加丰富一些，尽量能囊括能想到的所有的数据类型
        # 除去上述类型的数据，将被当做一个完整的对象，尝试获取对象下面的所有字段

        # prune 为精简模式只取 `__dict__` 中的字段，默认不使用 prune
        if prune and hasattr(obj, "__dict__"):
            keys = obj.__dict__.keys()
        else:
            keys = dir(obj)

        result = {}
        for key in keys:

            # 如果定义了 `filter_fields` 那么只有这里面的字段才会被序列化输出
            if filter_fields and key not in filter_fields:
                continue

            # 如果定义了 `exclude_fields` 那么这里面的字段不会被序列化输出
            if key in exclude_fields:
                continue

            # 为了避免垃圾数据过多 过滤掉以 `_` 开头的字段，这些字段一般不需要序列化输出
            if key.startswith('_'):
                continue

            value = getattr(obj, key)

            # callable 的方法不输出
            if callable(value):
                continue

            v = SerializeableObject.obj2dict(value, **kwargs)
            result[key] = v

        return result

    def serialize(self, **kwargs):
        return self.obj2dict(self, **kwargs)

    def to_json(self, **kwargs):
        data = self.serialize(**kwargs)
        kwargs.pop('prune', None)
        kwargs.pop('filter_fields', None)
        kwargs.pop('exclude_fields', None) 
        kwargs.pop('limit_deep', None)
        kwargs.pop('current_deep', None)
        return json.dumps(data, **kwargs)


def serialize(obj, **kwargs):
    return SerializeableObject.obj2dict(obj, **kwargs)


def obj_to_json(obj, **kwargs):
    data = serialize(obj, **kwargs)
    kwargs.pop('prune', None)
    kwargs.pop('filter_fields', None)
    kwargs.pop('exclude_fields', None) 
    kwargs.pop('limit_deep', None)
    kwargs.pop('current_deep', None)
    return json.dumps(data, **kwargs)


if __name__ == '__main__':

    # $ pip install easyserializer
    # from easyserializer import *
    # import datetime

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








