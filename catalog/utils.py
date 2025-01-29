def resize_image(image_field, target_size=(640, 480)):
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