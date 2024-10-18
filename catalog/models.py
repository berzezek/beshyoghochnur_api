from django.db import models
from django.utils.text import slugify
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    class Meta:
        verbose_name = "Katalog"
        verbose_name_plural = "katalog"

    translations = TranslatedFields(
        name=models.CharField(max_length=100, unique=True),
    )
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='images/categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Сначала сохраняем объект, чтобы получить первичный ключ (ID)
        super(Category, self).save(*args, **kwargs)

        # После получения ID можно работать с переводами и генерировать slug
        if not self.slug:
            name = self.safe_translation_getter('name', any_language=True)
            self.slug = slugify(name)
            # Сохраняем снова, чтобы обновить slug
            super(Category, self).save(update_fields=['slug'])

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)


class Product(TranslatableModel):
    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'mahsulot'

    translations = TranslatedFields(
        name=models.CharField(max_length=100, unique=True),
        description=models.TextField(null=True, blank=True),
    )
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='images/products/', blank=True, null=True)
    price = models.FloatField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Сначала сохраняем объект, чтобы получить первичный ключ (ID)
        super(Product, self).save(*args, **kwargs)

        # После получения ID можно работать с переводами и генерировать slug
        if not self.slug:
            name = self.safe_translation_getter('name', any_language=True)
            self.slug = slugify(name)
            # Сохраняем снова, чтобы обновить slug
            super(Product, self).save(update_fields=['slug'])

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)
