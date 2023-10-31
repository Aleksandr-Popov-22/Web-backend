
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Category, SellRequest, RequestCategory, Users
import psycopg2

'''
categorys = [
    {'title': 'Электроника', 'id': 1, 'img': 'image/c1.jpg', 'info': 'Новые модели телефонов, планшетных компьютеров, ноутбуков, фотоаппаратов и многое другое.'},
    {'title': 'Одежда', 'id': 2, 'img': 'image/c2.jpg', 'info': 'Широкий спектр одежды, которая подходит для каждого времени года.'},
    {'title': 'Обувь', 'id': 3, 'img': 'image/c3.png', 'info': 'Высококачественная обувь - это один из важных элементов нашего образа и заботы о нашем комфорте.'},
    {'title': 'Бытовая техника', 'id': 4, 'img': 'image/c4.jpg', 'info': 'Стильная и современная техника для дома.'},
    {'title': 'Мебель', 'id': 5, 'img': 'image/c5.jpg', 'info': 'Для обстановки жилых и общественных помещений и различных зон пребывания человека.'},
    {'title': 'Книги', 'id': 6, 'img': 'image/c6.jpg', 'info': 'От классики до современных бестселлеров.'},
    {'title': 'Дом и сад', 'id': 7, 'img': 'image/c7.jpg', 'info': 'Для любого сезона найдется все.'},
    {'title': 'Детские товары', 'id': 8, 'img': 'image/c8.jpg', 'info': 'Игрушки, школьные принадлежности, книги, товары для школьников.'},
    {'title': 'Красота и здоровье', 'id': 9, 'img': 'image/c9.jpg', 'info': 'Здоровый и веселый дух является источником красоты.'},
    {'title': 'Спорт и отдых', 'id': 10, 'img': 'image/c10.jpg', 'info': 'Спорт и отдых всегда ассоциируется с физический активностью и здоровым образом жизни.'},
    {'title': 'Строительство и ремонт', 'id': 11, 'img': 'image/c11.jpg', 'info': 'Строительство, эксплуатация, ремонт зданий.'},
    {'title': 'Продукты питания', 'id': 12, 'img': 'image/c12.jpg', 'info': 'Продукты питания характеризует их пищевая, биологическая и энергетическая ценность.'},
    {'title': 'Аптека', 'id': 13, 'img': 'image/c13.jpg', 'info': 'Обеспечение лекарствами по рецептам; продажа готовых лекарств.'},
    {'title': 'Товары для животных', 'id': 14, 'img': 'image/c14.jpg', 'info': 'Огромный выбор различных зоотоваров.'},
    {'title': 'Автотовары', 'id': 15, 'img': 'image/c15.jpg', 'info': 'Большой выбор нструментов и средств для ухода и ремонта автомобилей.'},
    {'title': 'Аксессуары', 'id': 16, 'img': 'image/c16.jpg', 'info': 'Аксессуары часто выбирают, чтобы завершить наряд и дополнить образ.'},

    ]
    UPDATE Category 
	   SET Status = 'Удалён' 
	   WHERE Id = 1001;
    
    
    
    


def DelCategory(request, id):
    if request.GET.get("delCat"):
        conn = psycopg2.connect(dbname="Marketplace", host="localhost", user="postgres", password="alex22", port="5432")
        cursor = conn.cursor()
        cursor.execute("UPDATE Category SET Status ='Deleted' WHERE Id=%s", [id])
        conn.commit()  # реальное выполнение команд sql1
        cursor.close()
        conn.close()
    return render(request, 'index.html', {'data': {'categorys': Category.objects.all()}})
'''
def GetCategory(request, id):

    if request.GET.get("delCategory"):
        conn = psycopg2.connect(dbname="Marketplace", host="localhost", user="postgres", password="alex22", port="5432")
        cursor = conn.cursor()
        cursor.execute("UPDATE Category SET Status ='Удалён' WHERE Id=%s", [id])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('sendCategory')
        #return render(request, 'index.html',
         #           {'data': {'categorys': Category.objects.filter(status="Действует").order_by('id')}})

    return render(request, 'category.html', {'data': {'categorys': Category.objects.filter(id=id)[0]}})
def sendCategory(request):

    if request.GET.get("category"):
        input_text = request.GET.get("category")
        return render(request, 'index.html',
        {'data': {'categorys': (Category.objects.filter(name_category=input_text) & Category.objects.filter(status="Действует").order_by('id')), 'find': input_text}})
    return render(request, 'index.html',
                  {'data': {'categorys': Category.objects.filter(status="Действует").order_by('id')}})






