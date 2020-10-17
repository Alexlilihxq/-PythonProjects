class HouseItem:
    def __init__(self,name,area):
        self.name = name
        self.area = area
    def __str__(self) :
        return "[%s] 占地 %.2f 平米" %(self.name,self.area)

class House:
    def __init__(self,house_type,area):
        self.house_type = house_type
        self.area = area
        self.free_area = area
        self.item_list = []
    def __str__(self):
        return ("户型： %s\n总面积：%.2f[剩余：%.2f]\n家具：%s"
                %(self.house_type,self.area,
                 self.free_area,self.item_list))
    def add_item(self,item):
        if item.area > self.free_area:
            print("%s 的面积太大，超出面积" %item.name)
            return
        #加入家具列表
        self.item_list.append(item.name)
        #计算剩余面积
        self.free_area -= item.area