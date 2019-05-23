from django.contrib import admin

from .models import Good,Reviews,Order,GoodsInOrder

admin.site.register(Good)
admin.site.register(Reviews)
admin.site.register(Order)
admin.site.register(GoodsInOrder)
