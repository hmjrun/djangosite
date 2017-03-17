from django.contrib import admin

# Register your models here.
from .models import Goods
class GoodsAdmin(admin.ModelAdmin):
	pass

admin.site.register(Goods, GoodsAdmin)
