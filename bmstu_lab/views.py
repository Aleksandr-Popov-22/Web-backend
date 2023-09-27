
from django.shortcuts import render

categorys = [
    {'title': 'Электроника', 'id': 1, 'img': 'image/c1.jpg', 'info': 'Не упустите возможность приобрести новые модели телефонов, планшетных компьютеров, ноутбуков, фотоаппаратов и многое другое.'},
    {'title': 'Одежда', 'id': 2, 'img': 'image/c2.jpg', 'info': 'Вы найдёте широкий спектр одежды, которая подходит для каждого времени года.'},
    {'title': 'Обувь', 'id': 3, 'img': 'image/c3.png', 'info': 'Высококачественная обувь - это один из самых важных элементов нашего образа и заботы о нашем комфорте.'},
    {'title': 'Бытовая техника', 'id': 4, 'img': 'image/c4.jpg', 'info': 'Стильная и современная техника для дома.'},
    {'title': 'Мебель', 'id': 5, 'img': 'image/c5.jpg', 'info': 'Совокупность передвижных или встроенных изделий для обстановки жилых и общественных помещений и различных зон пребывания человека.'},
    {'title': 'Книги', 'id': 6, 'img': 'image/c6.jpg', 'info': 'От классики до современных бестселлеров.'},
    {'title': 'Дом и сад', 'id': 7, 'img': 'image/c7.jpg', 'info': 'Для любого сезона найдется все.'},
    {'title': 'Детские товары', 'id': 8, 'img': 'image/c8.jpg', 'info': 'Одежда и обувь, игрушки, школьные принадлежности, книги, товары для школьников и многое другое.'},
    {'title': 'Красота и здоровье', 'id': 9, 'img': 'image/c9.jpg', 'info': 'Здоровый и веселый дух является источником красоты. Здоровые люди всегда оптимистично настроены.'},
    {'title': 'Спорт и отдых', 'id': 10, 'img': 'image/c10.jpg', 'info': 'Спорт и отдых всегда ассоциируется с физический активностью и здоровым образом жизни. Активная форма отдыха призвана помочь в поддержании физической эффективности и общего состояния здоровья.'},
    {'title': 'Строительство и ремонт', 'id': 11, 'img': 'image/c11.jpg', 'info': 'Строительство, эксплуатация, ремонт зданий — это сложные многоуровневые задачи, которые требуют участия специалистов и постоянного контроля качества.'},
    {'title': 'Продукты питания', 'id': 12, 'img': 'image/c12.jpg', 'info': 'Продукты питания характеризует их пищевая, биологическая и энергетическая ценность.'},
    {'title': 'Аптека', 'id': 13, 'img': 'image/c13.jpg', 'info': 'Обеспечение лекарствами по рецептам; продажа готовых лекарств, разрешенных к отпуску без рецепта, предметов санитарии, гигиены, ухода за больными, лекарственных трав, перевязочных материалов и других медицинских изделий.'},
    {'title': 'Товары для животных', 'id': 14, 'img': 'image/c14.jpg', 'info': 'Огромный выбор различных зоотоваров. Качественные корма, витамины, аксессуары и многое другое.'},
    {'title': 'Автотовары', 'id': 15, 'img': 'image/c15.jpg', 'info': 'Большой выбор нструментов и средств для ухода и ремонта автомобилей.'},
    {'title': 'Аксессуары', 'id': 16, 'img': 'image/c16.jpg', 'info': 'Аксессуары часто выбирают, чтобы завершить наряд и дополнить образ. Они обладают способностью дополнительно выражать личность человека.'},

    ]
'''
applications = {'id': 1, 1: [
        {'title': 'Смартфон Apple iPhone 11 128 ГБ, черный', 'img': 'image/iphone.jpg', 'price': '55000',
         'status': 'yes', 'info': 'Устаревшая модель'},
        {'title': '16" Игровой ноутбук Lenovo LEGION R9000P', 'img': 'image/lenovo.jpg', 'price': '107000',
         'status': 'yes', 'info': 'Самый мощный из линейки'},
        {'title': 'Смартфон Samsung Galaxy S23 Ultra 512 ГБ, бежевый', 'img': 'image/samsung.jpg', 'price': '68000',
         'status': 'no', 'info': 'Южнокорейский флагман'},
        {'title': '17.3" Игровой ноутбук MSI Katana 17 B12VFK-424RU', 'img': 'image/msi.jpg', 'price': '94000',
         'status': 'yes', 'info': 'Многоядерный и быстрый'},
        {'title': 'Телевизор Samsung UE50AU7100UXCE 50" Ultra HD, серый', 'img': 'image/uhd.jpg', 'price': '65000',
         'status': 'no', 'info': 'Самая яркая картинка'},
    ], 2: [
        {'title': 'Футболка adidas Mens Yoga Tee', 'img': 'image/adidas.jpg', 'price': '5000', 'status': 'yes', 'info': 'Размер M'},
        {'title': "Джинсы Levi's 501 Original Canyon Kings", 'img': 'image/levis.jpg', 'price': '7000',
         'status': 'yes', 'info': 'Размер 32'},
        {'title': 'Рубашка HENDERSON', 'img': 'image/henderson.jpg', 'price': '3000', 'status': 'no', 'info': 'Нестареющая классика'},
        {'title': 'Шорты Nike', 'img': 'image/nike.jpg', 'price': '2000', 'status': 'yes', 'info': 'Идеально для спорта'},
    ], 3: [
        {'title': 'Кроссовки Reebok Nfx Trainer', 'img': 'image/reebok.jpg', 'price': '5000', 'status': 'yes', 'info': 'Легкие и удобные'},
        {'title': 'Кроссовки adidas Forum Low', 'img': 'image/forum.jpg', 'price': '7000', 'status': 'yes', 'info': 'Новинка!'},
        {'title': 'Ботинки Timberland', 'img': 'image/timberland.jpg', 'price': '10000', 'status': 'no', 'info': 'На суровую зиму'},
    ], 4: [
        {'title': 'Холодильник Indesit ES 20', 'img': 'image/indesit.jpg', 'price': '15000', 'status': 'yes', 'info': 'Почти бесшумный'},
        {'title': 'Узкая стиральная машина Hotpoint NSB 7225 ZS V RU, белый', 'img': 'image/hotpoint.jpg',
         'price': '27000', 'status': 'yes', 'info': 'Новинка!'},
    ], 5: [
        {'title': 'Кресло ASKONA Moony', 'img': 'image/askona.jpg', 'price': '15000', 'status': 'yes', 'info': 'Самое мягкое в линейке'},
        {'title': 'Стол обеденный Раздвижной SALVADORE', 'img': 'image/stol.jpg', 'price': '7000', 'status': 'yes', 'info': 'Для большой семьи'},
        {'title': 'Кресло компьютерное HALMAR AREZZO', 'img': 'image/kreslo.jpg', 'price': '8000', 'status': 'no', 'info': 'Для гейминга'},
        {'title': 'Тумба "Wallstreet" 3', 'img': 'image/komod.jpg', 'price': '4000', 'status': 'yes', 'info': 'Хит продаж!'},
    ], 6: [
        {'title': 'Война и мир (в 2-х книгах)', 'img': 'image/book1.jpg', 'price': '500', 'status': 'yes', 'info': 'Вечная классика'},
        {'title': 'Преступление и наказание | Достоевский Федор Михайлович', 'img': 'image/book2.jpg', 'price': '700',
         'status': 'yes', 'info': 'Обязательна к прочтению'},
    ]}
'''

def GetCategory(request, id):
    data = {}
    for cat in categorys:
        if cat['id'] == id:
            data = cat
    print(data)
    return render(request, 'category.html', {'data': data})

def sendText(request):

    if request.GET.get("text"):
        input_text = request.GET.get("text")
        if input_text == None:
            input_text = ''
        result = list(filter(lambda x: str(x['title']).lower() == input_text.lower(), categorys))
        return render(request, 'index.html', {'data': {'categorys':result, 'find': input_text}})
    return render(request, 'index.html', {'data': {'categorys':categorys}})




