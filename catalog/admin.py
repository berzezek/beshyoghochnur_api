from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.conf import settings
from django.utils.html import format_html
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from .models import Category, Product

# Убираем группы и пользователей из админки, если это необходимо
admin.site.unregister(Group)
admin.site.unregister(User)

class CategoryForm(TranslatableModelForm):

    class Meta:
        model = Category
        fields = '__all__'
        labels = {
            'name': 'Mahsulot nomi',
            'slug': 'Slug',
            'image': 'Rasm',
            'is_active': 'Faol',
        }


class CategoryAdmin(TranslatableAdmin):
    form = CategoryForm
    list_display = ('name', 'slug', 'is_active', 'image_tag')
    search_fields = ('translations__name',)
    list_filter = ('is_active',)
    ordering = ('translations__name',)
    actions = ['make_inactive', 'make_active']
    fields = ('name', 'image', 'is_active', 'slug')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.active_translations(settings.LANGUAGE_CODE).distinct()

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return "Rasm yo'q"

    image_tag.short_description = 'Rasm'

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive.short_description = "Tanlangan kategoriyalarni faol emas qilib belgilash"

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active.short_description = "Tanlangan kategoriyalarni faol qilib belgilash"

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


class ProductForm(TranslatableModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.active_translations().distinct(),
        label="Kategoriya"
    )

    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            'name': 'Mahsulot nomi',
            'slug': 'Slug',
            'description': 'Tavsif',
            'price': 'Narxi',
            'image': 'Rasm',
            'is_active': 'Faol',
        }


class ProductAdmin(TranslatableAdmin):
    form = ProductForm
    list_display = ('name', 'price', 'category', 'is_active', 'image_tag')
    search_fields = ('translations__name', 'translations__description')
    list_filter = ('category', 'is_active')
    ordering = ('translations__name',)
    actions = ['make_inactive', 'make_active']
    fields = ('name', 'description', 'category', 'image', 'price', 'is_active', 'slug')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.active_translations().distinct()

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return "Rasm yo'q"

    image_tag.short_description = 'Rasm'

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive.short_description = "Tanlangan mahsulotlarni faol emas qilib belgilash"

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active.short_description = "Tanlangan mahsulotlarni faol qilib belgilash"

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


# Регистрируем модели с обновленными настройками админки
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
