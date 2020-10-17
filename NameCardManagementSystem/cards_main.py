import cards_tools
while True:
    action_str=cards_tools.show_menu()  #显示菜单
    if action_str in ["0","1","2","3"]:
        if action_str =="1":
            cards_tools.new_card()
        elif action_str =="2":
            cards_tools.show_all()
        elif action_str =="3":
            cards_tools.sch_card()
        elif action_str =="0":
            print("正在退出...欢迎下次使用本系统")
            break
    else: print("您的输入有误，请重新输入")