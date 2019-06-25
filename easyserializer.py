#coding=utf8

import json
import six
import datetime


__all__ = ['obj_to_dict', 'obj_to_json', 'serialize', 'SerializeableObject']


"""
简易对象序列化工具
serialize a object 
"""


VERSION = '0.2.11'
TOO_DEEP = 'TOO_DEEP'


def obj_to_dict(obj, *filter_fields, **kwargs):
    """
    filter_fields:  指定输出字段(默认输出所有)
                    示例: obj_to_dict(obj, 'field1', 'field2', filter_fields=['field3', 'field4'])
    exclude_fields: 指定不要输出字段
    limit_deep:     限制递归深度, 默认5层. 设为0则不限制递归深度(不建议设为0!)
    prune:          精简模式(只取 `__dict__` 中的字段, 默认不开启)  
    """

    filter_fields = list(filter_fields) + list(kwargs.get('filter_fields', []))
    exclude_fields = kwargs.get('exclude_fields', [])
    limit_deep = kwargs.get('limit_deep', 5)
    prune = kwargs.get('prune', False)

    if isinstance(obj, SerializeableObject):
        filter_fields += obj.serialize_filter_fields()
        exclude_fields += obj.serialize_exclude_fields()

    # 当指定了 filter_fields 时，exclude_fields 不生效
    if filter_fields:
        exclude_fields = []

    current_deep = kwargs.get('current_deep', 0)  # 当前递归深度(程序自己维护,不要手动传入!)

    if limit_deep and limit_deep < current_deep:
        # 超出限制递归深度 返回 `TOO_DEEP` 字符串
        return TOO_DEEP

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
            result.append(obj_to_dict(item, **kwargs))
        return result

    if isinstance(obj, dict):
        result = {}
        for sub_key, sub_value in obj.items():
            result[sub_key] = obj_to_dict(sub_value, **kwargs)
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
            
        # 无法正常获取到值就设为 None
        try:
            value = getattr(obj, key)
            # callable 的方法不输出
            if callable(value):
                continue
            v = obj_to_dict(value, **kwargs)
        except Exception as e:
            v = None

        result[key] = v

    return result


def obj_to_json(obj, *filter_fields, **kwargs):
    data = obj_to_dict(obj, *filter_fields, **kwargs)
    kwargs.pop('prune', None)
    kwargs.pop('filter_fields', None)
    kwargs.pop('exclude_fields', None) 
    kwargs.pop('limit_deep', None)
    kwargs.pop('current_deep', None)
    return json.dumps(data, **kwargs)


# ==== serialize is the same as obj_to_json ====
serialize = obj_to_dict
# ==============================================


class SerializeableObject(object):

    def serialize(self, *filter_fields, **kwargs):
        return obj_to_dict(self, *filter_fields, **kwargs)

    def to_dict(self, *filter_fields, **kwargs):
        return obj_to_dict(self, *filter_fields, **kwargs)

    def to_json(self, *filter_fields, **kwargs):
        return obj_to_json(self, *filter_fields, **kwargs)

    def serialize_filter_fields(self):
        return []

    def serialize_exclude_fields(self):
        return []



if __name__ == '__main__':

    # $ pip install easyserializer
    # from easyserializer import SerializeableObject, obj_to_dict, obj_to_json
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

    # =============== 传参说明 =================
    # filter_fields:  指定输出字段，可使用 list 和 dict 两种传参形式
    #                 示例: obj_to_dict(obj, 'field1', 'field2', filter_fields=['field3', 'field4'])
    #                 默认为输出所有字段
    # exclude_fields: 过滤不要输出字段
    # limit_deep:     限制递归深度, 默认5层. 设为0则不限制递归深度(不建议这么做!)
    # prune:          精简模式(只取 `__dict__` 中的字段, 默认不开启)

    # 继承自 SerializeableObject 的对象直接调用 serialize 方法，该对象转换为 dict 返回
    print(t.serialize())
    print(t.serialize('name', 'students'))
    

    # 调用对象的 to_json 方法，对象以 json 字符串形式返回 (可传入 json.dump 的参数如 `indent`)
    print(t.to_json())
    print(t.to_json(exclude_fields=['role'], indent=4))

    # 也可以直接使用 obj_to_dict, obj_to_json 这些函数
    print(obj_to_dict(t, limit_deep=2))
    print(obj_to_json(t, prune=True, indent=4))




