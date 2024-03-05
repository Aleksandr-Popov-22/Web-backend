from django.shortcuts import render
from django.shortcuts import redirect
from .models import Category, SellRequest, RequestCategory, Users
import psycopg2


def DelCategory(request, id):
    if request.POST:
        conn = psycopg2.connect(dbname="MarketDB", host="localhost", user="postgres", password="alex22", port="5432")
        cursor = conn.cursor()
        cursor.execute("UPDATE Category SET Status ='Удалён' WHERE Id=%s", [id])
        conn.commit()
        cursor.close()
        conn.close()


    return redirect('categorys')



def GetCategoryId(request, id):

    return render(request, 'category.html', {'data': {'categorys': Category.objects.filter(id=id)[0]}})
def GetCategorys(request):

    categorys = Category.objects.filter(status="Действует")
    input_text = request.GET.get("category")

    if input_text is not None:
        categorys = (Category.objects.filter(name_category__icontains=input_text) & Category.objects.filter(status="Действует"))

    else:
        input_text = ""

    sell_req = SellRequest.objects.filter(status="Черновик").last()
    cat = Category.objects.filter(requestcategory__id_request=sell_req)
    k = cat.count()

    return render(request, 'index.html',{'data': {'categorys': categorys, 'find': input_text, "len": k}})

def GetRequest(request):
    sell_req = SellRequest.objects.filter(status="Черновик").last()
    cat = Category.objects.filter(requestcategory__id_request=sell_req)
    return render(request, 'request.html', {'data': {'categorys': cat}})
