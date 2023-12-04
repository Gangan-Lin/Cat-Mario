# 定义一个简单的类
class Dog:
    # 类属性
    species = "Canis familiaris"

    # 构造方法
    def __init__(self , age,name):
        # 实例属性
        self.name = name
        self.age = age

    # 实例方法
    def bark(self):
        print(f"{self.name} says Woof!")

# 创建类的实例
my_dog = Dog(name="Buddy", age=3)

# 访问实例属性
print(f"{my_dog.name} is {my_dog.age} years old.")

# 调用实例方法
my_dog.bark()
