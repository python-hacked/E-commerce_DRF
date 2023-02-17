from django.contrib import admin
from django.utils.html import format_html

from .models import Products, Category, SubCategory, Seller, Collections,\
    Feature, AvailableOffer, Cart, Address

# Register your models here


admin.site.register(SubCategory)
admin.site.register(Seller)
admin.site.register(Feature)
admin.site.register(AvailableOffer)
admin.site.register(Address)


class CollectionsAdmin(admin.ModelAdmin):
    """ product Collections interface configure"""
    list_display = ['id', 'collection_name', 'photo_pre']
    readonly_fields = ('photo_pre',)

    def photo_pre(self, obj):
        """ image view in admin panel"""
        return format_html(f'<img style="height:100px;" src="/media/{obj.image}"/>')


admin.site.register(Collections, CollectionsAdmin)


class CategoryAdmin(admin.ModelAdmin):
    """ product categories interface configure"""
    list_display = ['id', 'name', 'photo_pre']
    readonly_fields = ('photo_pre',)

    def photo_pre(self, obj):
        """ image view in admin panel"""
        return format_html(f'<img style="height:100px;" src="/media/{obj.icon}"/>')


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    """ product admin interface configure"""
    list_display = ['id', 'title', 'actual_price', 'discount_price', 'photo_pre']
    readonly_fields = ('photo_pre',)
    # fields = ('title', 'photo_pre', 'discount_price')

    def photo_pre(self, obj):
        """ image view in admin panel"""
        return format_html(f'<img style="height:100px;" src="/media/{obj.image}"/>')


admin.site.register(Products, ProductAdmin)
admin.site.register(Cart)

