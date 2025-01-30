from django.db import models
from django.utils.text import slugify
from django.core.files import File
from PIL import Image
from io import BytesIO

from parler.models import TranslatableModel, TranslatedFields

from catalog.utils import resize_image


class Category(TranslatableModel):
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    translations = TranslatedFields(
        name=models.CharField(max_length=100),
    )
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='images/categories/', blank=True, null=True, default='images/default.webp')
    thumbnail = models.ImageField(upload_to='images/categories/thumbnails/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.safe_translation_getter('name', any_language=True))
        
        super(Category, self).save(*args, **kwargs)
        
        if self.image and not self.thumbnail:
            self.thumbnail = resize_image(self.image, (640, 480))
            super(Category, self).save(update_fields=['thumbnail'])


    def __str__(self):
        if self.safe_translation_getter('name', any_language=True):
            return self.safe_translation_getter('name', any_language=True)
        return self.id

class Manufacturer(TranslatableModel):
    class Meta:
        verbose_name = "Ishlab chiqaruvchi"
        verbose_name_plural = "Ishlab chiqaruvchilar"


    translations = TranslatedFields(
        name=models.CharField(max_length=100, unique=True),
    )

    def __str__(self):
        if self.safe_translation_getter('name', any_language=True):
            return self.safe_translation_getter('name', any_language=True)
        return self.id


class Product(TranslatableModel):
    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'

    translations = TranslatedFields(
        name=models.CharField(max_length=100, blank=True, null=True),
        description=models.TextField(null=True, blank=True),
    )
    manufactures = models.ForeignKey('Manufacturer', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='images/products/', blank=True, null=True, default='images/default.webp')
    thumbnail = models.ImageField(upload_to='images/products/thumbnails/', blank=True, null=True)
    price = models.FloatField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    pdf = models.FileField(upload_to='pdfs/products/', blank=True, null=True, verbose_name="Инструкция (PDF)")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.safe_translation_getter('name', any_language=True))
        
        super(Product, self).save(*args, **kwargs)  # Сохранение первичного объекта
        
        if self.image and not self.thumbnail:
            self.thumbnail = resize_image(self.image, (640, 480))
            super(Product, self).save(update_fields=['thumbnail'])  # Обновляем только thumbnail

    def __str__(self):
        if self.safe_translation_getter('name', any_language=True):
            return self.safe_translation_getter('name', any_language=True)
        return self.id
