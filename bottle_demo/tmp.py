def digui(x):
    if x>0:
        print("我在"+str(x),end="")
        digui(x-1)
        print("看电视"+str(x),end="")
    else :
        print("写作业"+str(x),end="")

digui(3)