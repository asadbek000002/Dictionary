from django.db import models
from ckeditor.fields import RichTextField


class Regions(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"

    def __str__(self):
        return self.name


class Words(models.Model):
    name = models.CharField(max_length=250)
    grammatical_description = models.TextField(max_length=1000)
    lexical_form = models.TextField(max_length=1000)
    comment = models.TextField(max_length=1000)
    region = models.ForeignKey(Regions, on_delete=models.SET_NULL, null=True, related_name='words')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Word"
        verbose_name_plural = "Words"

    def __str__(self):
        return self.name


class Text(models.Model):
    source = models.CharField(max_length=255)
    content = models.TextField()
    word = models.ForeignKey(Words, on_delete=models.SET_NULL, null=True, related_name='text')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Text"
        verbose_name_plural = "Texts"

    def __str__(self):
        return self.content[:50]  # Matnning birinchi 50 belgisini ko'rsatadi


class Suffix(models.Model):
    suffix = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Suffix"
        verbose_name_plural = "Suffixes"

    def __str__(self):
        return self.suffix


class News(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField(max_length=20000)
    image = models.ImageField(upload_to='news/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "New"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title


class UsefulLink(models.Model):
    title = models.CharField(max_length=150)
    last_title = models.CharField(max_length=150)
    text = models.TextField(max_length=20000)
    link = models.URLField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='news/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Useful Link"
        verbose_name_plural = "Useful Links"

    def __str__(self):
        return self.title


class Employees(models.Model):
    image = models.ImageField(upload_to="employees/")
    full_name = models.CharField(max_length=50)
    info_text = models.TextField(max_length=10000)
    degree = models.CharField(max_length=250)
    position = models.CharField(max_length=250)
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class SearchHistory(models.Model):
    word = models.ForeignKey(Words, on_delete=models.SET_NULL, null=True, )
    missing_word = models.CharField(max_length=250)
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.word:
            return f"{self.word.name} - {self.count} ta qidirilgan"
        return f"{self.missing_word} - {self.count} ta qidirilgan"


class Contact(models.Model):
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    message = models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone


class Publications(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="publications/")
    file = models.FileField(upload_to="publications/pdf/")
    text = models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class About(models.Model):
    phone = models.CharField(max_length=13)
    email = models.EmailField()
    location_name = models.CharField(max_length=255)
    location_link = models.URLField()

    def __str__(self):
        return self.phone


class CategoryProject(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kategoriyaning nomi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category Project"
        verbose_name_plural = "Category Projects"


class AboutProject(models.Model):
    category = models.ForeignKey(CategoryProject, on_delete=models.CASCADE, related_name="loyhalar", verbose_name="Kategoriya")
    tasnif = RichTextField(verbose_name="Loyha tasnifi (Qollanma)", help_text="Loyha haqida to'liq qollanma yozing",
                           blank=True)

    def __str__(self):
        return f"Loyha: {self.category.name}"

    class Meta:
        verbose_name = "About Project"
        verbose_name_plural = "About Projects"
