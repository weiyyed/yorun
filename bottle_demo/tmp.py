class A():
    def __init__(self):
        print("111")
    def a(self):
        print('a')

class B(A):
    def __init__(self):
        super().__init__()
        print('2222')

b=B()
