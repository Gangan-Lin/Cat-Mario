# 腳色移動
class Move:
    # 移動
    species = "for move"

    # 構造
    def __init__(self , a, b): # << __init__(self, a, b, c) 用來設定某值, self 後來會被替換掉(self是約定成俗的使用方法)
        # 實例屬性                          如設定某值 a1 為 a 則以 self.a1 = a
        self.a1 = a
        self.b1 = b

    # 实例方法
    def say(self): # << 簡單來說就是def 原本的功能，但是可以共用同一個 Class 裡面的數據 (括號裡面要放self)
        print(f"{self.a1} say HI") #詳細的去看調用那行

# 创建类的实例 # << 在創建實例時可以理解為 以(name = Move(variable_1, variable_2))為例
                    #name.a1 = variable_1
                    #name.a2 = variable_2
a = 1            
abc = Move( a  , 3)      # << 可以理解為建立一個變數 (附帶(a, b)) << 無直接命名 (a = 某值, b = 某值)的話以順序判斷，有則已命名的名稱判斷輸入於何)
efg = Move(10,20)
# 訪問實例屬性
print(f"{abc.a1} is {abc.b1} years old.") # << 訪問時要訪問 某(創建類的實例) 的 a1值的話就是  (假設訪問abc的) abs.a1 
a = 1 + 1
# 调用实例方法
abc.say()   # << 可以理解為調用 abc 的值，執行function say #而 def say(self)的self 就是替換成abc




