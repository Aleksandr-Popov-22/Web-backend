
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Category, SellRequest, RequestCategory, Users
import psycopg2
import base64

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
'''


def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def insert_blob(id_cat, photo):
    conn = psycopg2.connect(dbname="Marketplace", host="localhost", user="postgres", password="alex22",
                            port="5432")
    cursor = conn.cursor()

    blob_photo = convert_to_binary_data(photo)

    cursor.execute("UPDATE Category SET Image=%s WHERE Id=%s", [blob_photo, id_cat])
    conn.commit()
    print("Изображение и файл успешно вставлены как BLOB в таблиу")
    cursor.close()
    conn.close()


def convert_to_img():
    images = []
    for obj in Category.objects.filter(status='Действует'):
        # obj = Category.objects.get(id=i)
        image_data = base64.b64encode(obj.image).decode()
        images.append(image_data)
    return images


def convert_to_img_id(name_cat):
    images = []
    obj = Category.objects.get(name_category=name_cat)
    image_data = base64.b64encode(obj.image).decode()
    images.append(image_data)
    return images





def DelCategory(request, id):
    if request.POST:
        conn = psycopg2.connect(dbname="Marketplace", host="localhost", user="postgres", password="alex22", port="5432")
        cursor = conn.cursor()
        cursor.execute("UPDATE Category SET Status ='Удалён' WHERE Id=%s", [id])
        conn.commit()
        cursor.close()
        conn.close()


    return redirect('sendCategory')
    #return render(request, 'index.html',{'data': {'categorys': category_full}})



def GetCategory(request, id):

    return render(request, 'category.html', {'data': {'categorys': Category.objects.filter(id=id)[0]}})
def SendCategory(request):

    '''
    insert_blob(1,  "bmstu_lab/static/image/c1.jpg")
    insert_blob(2, "bmstu_lab/static/image/c2.jpg")
    insert_blob(3, "bmstu_lab/static/image/c3.png")
    insert_blob(4, "bmstu_lab/static/image/c4.jpg")
    insert_blob(5, "bmstu_lab/static/image/c5.jpg")
    insert_blob(6, "bmstu_lab/static/image/c6.jpg")
    insert_blob(7, "bmstu_lab/static/image/c7.jpg")
    insert_blob(8, "bmstu_lab/static/image/c8.jpg")
    insert_blob(9, "bmstu_lab/static/image/c9.jpg")
    insert_blob(10, "bmstu_lab/static/image/c10.jpg")
    insert_blob(11, "bmstu_lab/static/image/c11.jpg")
    
    '''

    #insert_blob(12, "bmstu_lab/static/image/c12.jpg")
    #convert_to_img(12)


    category_full = zip(Category.objects.filter(status="Действует"), convert_to_img())

    if request.GET.get("sendCategory"):
        input_text = request.GET.get("sendCategory")
        category_full = zip(Category.objects.filter(name_category=input_text) & Category.objects.filter(status="Действует"), convert_to_img_id(input_text))


        return render(request, 'index.html',{'data': {'categorys': category_full, 'find': input_text}})
    return render(request, 'index.html',
                  {'data': {'categorys': category_full}})