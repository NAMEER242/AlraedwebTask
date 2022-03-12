from rest_framework import serializers
from .models import *


class ItemsSer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'

    @staticmethod
    def topItemsSer(items):
        data = []
        for i in items:
            IID = i.IID
            title = i.title
            projImage = str(i.itemImage)
            totalSoldProduct = i.totalSoldProduct
            des = i.description
            price = i.productPrice
            uploadDate = i.uploadDate
            d = {
                IID: {
                    "title": title,
                    "itemImage": projImage,
                    "totalSoldProduct": totalSoldProduct,
                    "description": des,
                    "price": price,
                    "uploadDate": uploadDate,
                }
            }
            data.append(d)

        return data

    @staticmethod
    def Items(items):
        data = []
        if len(items) > 0:
            for i in items:
                d = {
                    i.IID: {
                        "title": i.title,
                        "description": i.description,
                        "itemImage": str(i.itemImage),
                        "totalSoldProduct": i.totalSoldProduct,
                        "Price": i.productPrice,
                        "uploadDate": i.uploadDate,
                    }
                }
                data.append(d)
            return data
        else:
            return "None"


class CustomUserSer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CompanyReceiptsSer(serializers.ModelSerializer):
    class Meta:
        model = Receipts
        fields = '__all__'

    @staticmethod
    def receipts(rcpts):
        data = []
        for r in rcpts:
            d = {
                "seller": r.seller,
                "buyer": r.buyer,
                "product": r.product,
                "notes": r.notes,
                "price": r.price,
                "datetime": r.datetime,
                "RID": r.RID,
            }
            data.append(d)
        return data
