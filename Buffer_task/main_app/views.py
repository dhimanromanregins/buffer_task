from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Case, When
from .models import Items, ItemOrder
from django.contrib import messages
import json

def items_display(request):
    if request.method == "GET":
        try:
            item_order_id = ItemOrder.objects.get(user=request.user.id)
            order_list = list(map(change_strind_to_int, json.loads(item_order_id.item_order)))
            ordering = Case(*[When(id=id_val, then=index) for index, id_val in enumerate(order_list)])
            items = Items.objects.filter(id__in=order_list).order_by(ordering)
        except Exception as e:
            items = Items.objects.all()
        context = {'items': items}
        return render(request, 'home.html', context)


def update_item(request):
    try:
        if request.method == 'POST':
            queryset = dict(request.POST)
            order = queryset.get("order[]")
            user_id = request.user.id
            try:
                ItemOrder.objects.get(user=user_id)
                item_order_obj = ItemOrder.objects.filter(user=request.user).update(item_order=json.dumps(order))
            except Exception as e:
                item_order_obj = ItemOrder.objects.create(user=request.user, item_order=json.dumps(order))
            return HttpResponse('Success.')
        else:
            return HttpResponse('Invalid request.')
    except Exception as error:
        print(error)


class ItemAdd(View):
    def get(self, request):
        return render(request, "items.html")

    def post(self, request):
        itemname = request.POST.get("itemname")
        if not request.POST.get("itemname"):
            messages.error(request, 'Please fill the item name')
            return render(request, "items.html")
        items = Items.objects.create(name=itemname)
        item_id = items.id
        try:
            item_order_obj = ItemOrder.objects.get(user=request.user)
            item_order_list = json.loads(item_order_obj.item_order)
            item_order_list.insert(0, item_id)
            ItemOrder.objects.filter(user=request.user).update(item_order=json.dumps(item_order_list))
        except Exception as error:
            item_order_list = [i.id for i in Items.objects.all()] + [item_id]
            ItemOrder.objects.create(user=request.user, item_order=json.dumps(item_order_list))
        return redirect('home')
    
def change_strind_to_int(i):
    return int(i)

