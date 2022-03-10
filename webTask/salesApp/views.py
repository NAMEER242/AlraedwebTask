import time
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.decorators import api_view
from . import serialaizers
from .models import *


@api_view(['POST'])
def signup(request):
    u = str(request.query_params.get('user'))
    p = str(request.query_params.get('pass'))
    e = str(request.query_params.get('email'))
    fName = str(request.query_params.get('fname'))
    lName = str(request.query_params.get('lname'))
    image = request.FILES['img']

    if not CustomUser.objects.filter(username=u).exists():
        user = CustomUser.objects.create_user(
            username=u,
            email=e,
            password=p,
            image=image,
            first_name=fName,
            last_name=lName,
        )
        user.save()

        return HttpResponse(user.id)
    else:
        return HttpResponse("Username already used!!")


@api_view(['POST'])
def log_in(request):
    u = request.query_params.get('user')
    p = request.query_params.get('pass')
    user = authenticate(request, username=u, password=p)
    if user is not None:
        login(request, user)
        return HttpResponse(request.user.username)
    else:
        return HttpResponse('Error!!')


@api_view(['POST'])
def logout_user(request):
    logout(request)
    return HttpResponse('logged out')


@api_view(['GET'])
def get_me(request):
    return HttpResponse(request.user.username)


# ----------------------------------------------------------------------------------------------------------------------#


@api_view(['GET'])
def get_top_items(request):
    if len(Items.objects.all()) > 0:
        items = Items.objects.all().order_by('totalSoldProduct')[::-1][:3]

        res = ""
        j = 0
        for i in items:
            res += (str(items[j].IID) + ",")
            ++j
        print(items)

        return JsonResponse(serialaizers.ItemsSer.topItemsSer(items), safe=False)
    return HttpResponse("None")


@api_view(['GET'])
def getItems(request):
    Item = None

    if len(Items.objects.all()) > 0:
        if str(list(request.query_params.keys())[0]) == "level":
            level = int(request.query_params.get('level'))
            Item = Items.objects.all()[level * 20:(level + 1) * 20]
        elif str(list(request.query_params.keys())[0]) == "date":
            date = int(request.query_params.get('date'))
            Item = Items.objects.get(uploadDate=date)
        elif str(list(request.query_params.keys())[0]) == "IID":
            IID = request.query_params.get('IID')
            Item = Items.objects.filter(IID=IID)

        if Item:
            return JsonResponse(serialaizers.ItemsSer.Items(Item), safe=False)
        else:
            return HttpResponse("None")
    else:
        return HttpResponse("None")


@api_view(['GET'])
def getReceipts(request):
    receipts = None
    if str(list(request.query_params.keys())[0]) == "level":
        level = int(request.query_params.get('level'))
        receipts = Receipts.objects.all()[level * 20:(level + 1) * 20]
    elif str(list(request.query_params.keys())[0]) == "len":
        length = int(request.query_params.get('len'))
        receipts = Receipts.objects.all()[0:length]
    elif str(list(request.query_params.keys())[0]) == "rid":
        RID = int(request.query_params.get('rid'))
        receipts = Receipts.objects.filter(RID=RID)
    if receipts:
        return JsonResponse(serialaizers.CompanyReceiptsSer.receipts(receipts), safe=False)
    else:
        return HttpResponse("None")


# ----------------------------------------------------------------------------------------------------------------------#


@api_view(['POST'])
def addReceipt(request):
    seller = str(request.query_params.get('slr'))
    buyer = str(request.query_params.get('byr'))
    item = request.query_params.get('prod')
    notes = str(request.query_params.get('notes'))
    price = request.query_params.get('price')
    dateTime = int(time.time() * 1000)
    if Items.objects.filter(IID=item).exists():
        r = Receipts.objects.create(
            seller=seller,
            buyer=buyer,
            product=item,
            notes=notes,
            price=float(price),
            datetime=dateTime,
        )
        itm = Items.objects.get(IID=item)
        itm.totalSoldProduct = itm.totalSoldProduct + 1
        itm.save()
        return HttpResponse(r.RID)
    else:
        return HttpResponse("InputError!!")


@api_view(['POST'])
def addItem(request):
    itemImage = request.FILES['img']
    title = str(request.query_params.get('title'))
    description = str(request.query_params.get('des'))
    totalSoldProduct = request.query_params.get('totSld')
    productPrice = float(request.query_params.get('price'))
    uploadDate = int(time.time() * 1000)

    i = Items.objects.create(
        itemImage=itemImage,
        title=title,
        description=description,
        totalSoldProduct=totalSoldProduct,
        productPrice=productPrice,
        uploadDate=uploadDate,
    )

    return HttpResponse(i.IID)


# ----------------------------------------------------------------------------------------------------------------------#


@api_view(['PATCH'])
def editReceipt(request):
    RID = str(request.query_params.get('id'))
    seller = str(request.query_params.get('slr'))
    buyer = str(request.query_params.get('byr'))
    product = request.query_params.get('prod')
    notes = str(request.query_params.get('notes'))
    price = request.query_params.get('price')
    if len(Items.objects.filter(IID=product)) > 0:
        cr = Receipts.objects.get(RID=RID)
        if seller is not None:
            cr.seller = seller
        if buyer is not None:
            cr.buyer = buyer
        if product is not None:
            cr.product = product
        if notes is not None:
            cr.notes = notes
        if price is not None:
            cr.price = float(price)
        cr.save()
        return HttpResponse(cr.RID)
    else:
        return HttpResponse("Error!!")


@api_view(['PATCH'])
def editItems(request):

    IID = str(request.query_params.get('id'))
    itemImage = request.FILES['img'] if 'img' in request.FILES else None
    title = str(request.query_params.get('title'))
    description = str(request.query_params.get('des'))
    totalSoldProduct = request.query_params.get('totSld')
    productPrice = request.query_params.get('price')

    if len(Items.objects.filter(IID=IID)) > 0:
        i = Items.objects.get(IID=IID)
        if itemImage is not None:
            i.itemImage = itemImage
        if title is not None:
            i.title = title
        if description is not None:
            i.description = description
        if totalSoldProduct is not None:
            i.totalSoldProduct = totalSoldProduct
        if productPrice is not None:
            i.productPrice = float(productPrice)

        i.save()

        return HttpResponse(i.IID)
    else:
        return HttpResponse("Error!!")


# ----------------------------------------------------------------------------------------------------------------------#

@api_view(['DELETE'])
def deleteItem(request):
    IID = str(request.query_params.get('id'))
    if Items.objects.filter(IID=IID).exists():
        p = Items.objects.get(IID=IID)
        p.delete()
        return HttpResponse("Done!!")
    else:
        return HttpResponse("Error!!")


# ----------------------------------------------------------------------------------------------------------------------#


@api_view(['GET'])
def test(request):
    return HttpResponse("testing!")
