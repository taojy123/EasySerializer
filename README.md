# easyserializer


[![PyPI Downloads](https://pypistats.com/badge/easyserializer.png)](https://pypistats.com/package/easyserializer)


简易对象序列化工具
serialize a object 


```
$ pip install easyserializer
```

```python

from easyserializer import SerializeableObject, obj_to_dict, obj_to_json, serialize
import datetime

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

```
