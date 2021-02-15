from poium import Page, NewPageElement, PageElement


class BaiduPage(Page):
    """ 百度Page,封装页面操作到的元素 """
    search_input = NewPageElement(css='#kw', timeout=10, describe='搜索栏')
    search_enter = NewPageElement(css='#su', timeout=10, describe='搜索按钮')
    # navigation_news = NewPageElement(css=[text='新闻'])
