card_list = []
def show_menu():
    """显示主菜单选项"""
    print("1.新增名片\n"
          "2.显示所有名片\n"
          "3.搜索名片\n\n"
          "0.退出系统\n")
    print("^"* 50)
    action_str = input("请选择希望执行的操作：")
    return action_str
def return_menu():
    while True:
        action_str=input("\n输入0返回主界面")
        if action_str=="0":
            break
def new_card():
    """
    添加新名片信息
    """
    print("^"*50)
    print("新增名片")
    #1.提示用户输入名片信息
    name  = input("请输入姓名 ：")
    phone = input("请输入电话 ：")
    qq    = input("请输入QQ号 ：")
    email = input("请输入Email ：")
    #2.将输入的信息存入字典格式
    card_dict = {"name":name,
                "phone":phone,
                "qq":qq,
                "email":email}
    #3.将名片字典存入List
    card_list.append(card_dict)
    #4.提示添加成功
    print("添加' %s '的名片成功！"%name)
    return_menu()
def show_all():
    print("^" * 50)
    print("显示所有名片")
    #判断是否存在记录
    if len(card_list)==0:
        print("当前没有名片记录，请添加名片")
        return
    # 遍历列表打印所有信息
    for table_name in ["姓名","电话","QQ ","邮箱"]:
        print(table_name,end="\t")
    print("")
    print("-"*50)
    for card_dict in card_list:
        print("%s\t\t%s\t\t%s\t\t%s\t\t"%(card_dict["name"],
                                  card_dict["phone"],
                                  card_dict["qq"],
                                  card_dict["email"]),end="\t\n")
    return_menu()
def sch_card():
    print("^" * 50)
    #1.提示用户输入要搜索的用户名
    find_name= input ("搜索名片\n请输入要搜索的姓名：")
    #2.遍历名片列表，找到信息并提示
    index=find_card(find_name)
    #3.可能继续执行的操作
    deal_card(index)
    return_menu()
def find_card(find_name):
    """
    查找指定名字的名片
    :param find_name: 要找的姓名
    :return: 返回在card_list中的索引
    """
    for card_dict in card_list:
        if find_name==card_dict["name"]:
            print("姓名：%s\n电话：%s\nQQ：%s\n邮箱：%s" %(card_dict["name"],
                                                         card_dict["phone"],
                                                         card_dict["qq"],
                                                         card_dict["email"]))
            found_name=find_name
            index=card_list.index(card_dict)
            break
        else:
            print("未找到用户")
            found_name = ""
    return index
def deal_card(index):
    action_str = input("1.修改\n"
                       "2.删除\n"
                       "0.无需其他操作")
    if action_str == "1":
        edit_card(index)
    elif action_str == "2":
        delete_card(index)
    elif action_str =="0":
        show_menu()
def edit_card(index):
    action_str = input("请问要修改该用户的哪项信息：\n"
                        "1.姓名\n2.电话\n3.QQ\n4.邮箱\n0.返回上一层")
    if action_str=="1":
        card_list[index]["name"]=input("请输入新的姓名：")
    elif action_str=="2":
        card_list[index]["phone"] = input("请输入新的电话：")
    elif action_str=="3":
        card_list[index]["qq"] = input("请输入新的QQ：")
    elif action_str=="4":
        card_list[index]["email"] = input("请输入新的邮箱：")
    elif action_str=="0":
        deal_card(index)
def delete_card(index):
    card_list.remove(index)