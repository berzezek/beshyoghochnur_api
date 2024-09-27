from django.contrib import admin
from .models import Category, Product
from django.contrib.auth.models import Group, User
from django.utils.html import format_html


admin.site.unregister(Group)
admin.site.unregister(User)



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'image_tag')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active',)
    ordering = ('name',)
    actions = ['make_inactive', 'make_active']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return "Нет изображения"
    image_tag.short_description = 'Изображение'

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Сделать неактивными выбранные категории"

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Сделать активными выбранные категории"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_active', 'image_tag')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category', 'is_active')
    ordering = ('name',)
    actions = ['make_inactive', 'make_active']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return "Нет изображения"
    image_tag.short_description = 'Изображение'

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Сделать неактивными выбранные товары"

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Сделать активными выбранные товары"

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
