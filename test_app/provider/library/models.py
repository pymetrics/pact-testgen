from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey("library.Author", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
