from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
import json

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='quotes', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='quotes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "author": self.author,
            "category": {
                "id": self.category.id if self.category else None,
                "name": self.category.name if self.category else None
            },
            "tags": [{"id": tag.id, "name": tag.name} for tag in self.tags.all()],
            "created_at": self.created_at.isoformat()
        }

    def to_json(self):
        return json.dumps(self.to_dict(), cls=DjangoJSONEncoder)

    def __str__(self):
        return f"{self.text[:50]}... by {self.author}"