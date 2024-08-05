from django.db import models
from django.conf import settings

# Model pro kategorii fóra
class Category(models.Model):
    name = models.CharField(max_length=100)  # Název kategorie
    description = models.TextField()  # Popis kategorie

    def __str__(self):
        return self.name

# Model pro vlákno v diskuzním fóru
class Thread(models.Model):
    title = models.CharField(max_length=200)  # Název vlákna
    content = models.TextField()  # Obsah vlákna
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Autor vlákna
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='threads')  # Kategorie vlákna
    created_at = models.DateTimeField(auto_now_add=True)  # Datum vytvoření vlákna
    updated_at = models.DateTimeField(auto_now=True)  # Datum poslední aktualizace vlákna

    def __str__(self):
        return self.title

# Model pro příspěvek ve vlákně
class Post(models.Model):
    content = models.TextField()  # Obsah příspěvku
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Autor příspěvku
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')  # Vlákno, ke kterému příspěvek patří
    created_at = models.DateTimeField(auto_now_add=True)  # Datum vytvoření příspěvku
    updated_at = models.DateTimeField(auto_now=True)  # Datum poslední aktualizace příspěvku

    def __str__(self):
        return f"Post by {self.author} on {self.thread}"
