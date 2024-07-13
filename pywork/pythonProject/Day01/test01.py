print('hellow,word')

# 斐波那契数列
def fac(n):
    if n==1 or n==2:
        return 1
    else:
        return fac(n-1)+fac(n-2)

print(fac(9))

class Cat:
    # 类属性
    a="类中的属性"

    #初始化方法
    def __init__(self,xm,age):
        self.xm=xm  #差不多相当于set方法
        self.age=age

    # 类中定义的函数，称为方法
    def show(self):
        print(self.xm,self.age)

    # 静态方法
    @staticmethod
    def sm():
        print("静态方法，不能调用实例属性和方法")

    #类方法
    @classmethod
    def cm(cls):
        print("类方法，不能调用实例属性和方法")

c=Cat("姓名",99)
c.b="新增的实例属性"
print(c.b)

def xinfangfa():
    print("新增加的方法")

c.fangfa=xinfangfa()
c.fangfa
# print(cat.xm,cat.age)
# print(cat.a)
# c.show()
# Cat.sm()
# Cat.cm()