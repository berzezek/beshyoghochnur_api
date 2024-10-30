from django.db import models
from django.utils.text import slugify
from django.core.files import File
from PIL import Image
from io import BytesIO
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    translations = TranslatedFields(
        name=models.CharField(max_length=100, unique=True),
    )
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='images/categories/', blank=True, null=True, default='images/default.webp')
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Обрезаем изображение перед сохранением
        if self.image:
            self.image = self.resize_image(self.image, (640, 480))
        
        # Сначала сохраняем объект, чтобы получить первичный ключ (ID)
        super(Category, self).save(*args, **kwargs)

        # После получения ID можно работать с переводами и генерировать slug
        if not self.slug:
            name = self.safe_translation_getter('name', any_language=True)
            self.slug = slugify(name)
            # Сохраняем снова, чтобы обновить slug
            super(Category, self).save(update_fields=['slug'])

    def resize_image(self, image_field, target_size=(640, 480)):
        img = Image.open(image_field)
        img = img.convert('RGB')  # Убедитесь, что изображение в формате RGB

        # Вычисляем целевые размеры, сохраняя соотношение сторон 16:9
        original_width, original_height = img.size
        target_width, target_height = target_size

        # Рассчитываем целевую ширину и высоту, чтобы сохранить соотношение 16:9
        target_ratio = target_width / target_height
        original_ratio = original_width / original_height

        if original_ratio > target_ratio:
            # Оригинал слишком широкий, нужно обрезать по ширине
            new_width = int(original_height * target_ratio)
            new_height = original_height
            left = (original_width - new_width) / 2
            top = 0
            right = (original_width + new_width) / 2
            bottom = original_height
        else:
            # Оригинал слишком высокий, нужно обрезать по высоте
            new_width = original_width
            new_height = int(original_width / target_ratio)
            left = 0
            top = (original_height - new_height) / 2
            right = original_width
            bottom = (original_height + new_height) / 2

        # Обрезаем и меняем размер изображения до нужного соотношения и размера
        img = img.crop((left, top, right, bottom))
        img = img.resize(target_size, Image.Resampling.LANCZOS)

        # Сохраняем изображение в BytesIO объект
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=85)

        # Создаем новое File-объект и возвращаем его
        new_image = File(thumb_io, name=image_field.name)
        return new_image



    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

class Manufacturer(TranslatableModel):
    class Meta:
        verbose_name = "Ishlab chiqaruvchi"
        verbose_name_plural = "Ishlab chiqaruvchilar"


    translations = TranslatedFields(
        name=models.CharField(max_length=100, unique=True),
    )

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)


class Product(TranslatableModel):
    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'

    translations = TranslatedFields(
        name=models.CharField(max_length=100, unique=True),
        description=models.TextField(null=True, blank=True),
    )
    manufactures = models.ForeignKey('Manufacturer', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='images/products/', blank=True, null=True, default='images/default.webp')
    price = models.FloatField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Обрезаем изображение перед сохранением
        if self.image:
            self.image = self.resize_image(self.image, (640, 480))
        
        # Сначала сохраняем объект, чтобы получить первичный ключ (ID)
        super(Product, self).save(*args, **kwargs)

        # После получения ID можно работать с переводами и генерировать slug
        if not self.slug:
            name = self.safe_translation_getter('name', any_language=True)
            self.slug = slugify(name)
            # Сохраняем снова, чтобы обновить slug
            super(Product, self).save(update_fields=['slug'])

    def resize_image(self, image_field, target_size=(640, 480)):
        img = Image.open(image_field)
        img = img.convert('RGB')  # Убедитесь, что изображение в формате RGB

        # Вычисляем целевые размеры, сохраняя соотношение сторон 16:9
        original_width, original_height = img.size
        target_width, target_height = target_size

        # Рассчитываем целевую ширину и высоту, чтобы сохранить соотношение 16:9
        target_ratio = target_width / target_height
        original_ratio = original_width / original_height

        if original_ratio > target_ratio:
            # Оригинал слишком широкий, нужно обрезать по ширине
            new_width = int(original_height * target_ratio)
            new_height = original_height
            left = (original_width - new_width) / 2
            top = 0
            right = (original_width + new_width) / 2
            bottom = original_height
        else:
            # Оригинал слишком высокий, нужно обрезать по высоте
            new_width = original_width
            new_height = int(original_width / target_ratio)
            left = 0
            top = (original_height - new_height) / 2
            right = original_width
            bottom = (original_height + new_height) / 2

        # Обрезаем и меняем размер изображения до нужного соотношения и размера
        img = img.crop((left, top, right, bottom))
        img = img.resize(target_size, Image.Resampling.LANCZOS)

        # Сохраняем изображение в BytesIO объект
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=85)

        # Создаем новое File-объект и возвращаем его
        new_image = File(thumb_io, name=image_field.name)
        return new_image



    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)
