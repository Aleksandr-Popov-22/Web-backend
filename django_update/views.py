from django.shortcuts import render


categorys = [
    {'title': 'Электроника', 'id': 1, 'img': 'static/image/c1.jpg', 'info': 'Новые модели телефонов, планшетных компьютеров, ноутбуков, фотоаппаратов и многое другое.'},
    {'title': 'Одежда', 'id': 2, 'img': 'static/image/c2.jpg', 'info': 'Широкий спектр одежды, которая подходит для каждого времени года.'},
    {'title': 'Обувь', 'id': 3, 'img': 'static/image/c3.png', 'info': 'Высококачественная обувь - это один из важных элементов нашего образа и заботы о нашем комфорте.'},
    {'title': 'Бытовая техника', 'id': 4, 'img': 'static/image/c4.jpg', 'info': 'Стильная и современная техника для дома.'},
    {'title': 'Мебель', 'id': 5, 'img': 'static/image/c5.jpg', 'info': 'Для обстановки жилых и общественных помещений и различных зон пребывания человека.'},
    {'title': 'Книги', 'id': 6, 'img': 'static/image/c6.jpg', 'info': 'От классики до современных бестселлеров.'},
    {'title': 'Дом и сад', 'id': 7, 'img': 'static/image/c7.jpg', 'info': 'Для любого сезона найдется все.'},
    {'title': 'Детские товары', 'id': 8, 'img': 'static/image/c8.jpg', 'info': 'Игрушки, школьные принадлежности, книги, товары для школьников.'},
    ]

sell_request = [categorys[1], categorys[5], categorys[4]]

def GetCategoryId(request, id):
    category = next((cat for cat in categorys if cat["id"] == id), None)
    return render(request, "category.html", {"data": {"categorys": category}})


def GetCategorys(request):
    query = request.GET.get("сategory")
    res = []
    k = len(sell_request)

    if query is None:
        return render(
            request, "index.html", {"data": {"categorys": categorys, "find": "", "len": k}}
        )
    else:
        for cat in categorys:
            if query is not None:
                if query.lower() in cat["title"].lower():
                    res.append(cat)
            else:
                res = categorys

    return render(
        request, "index.html", {"data": {"categorys": res, "find": query, "len": k}}
    )

def GetRequest(request):
    return render(request, "request.html", {'data': {'request': sell_request}})
