from django.db import models


# Create your models here.
class ObjectModel(models.Model):
    product_id = models.CharField(max_length=100)
    review_title = models.CharField(max_length=100, blank=True)
    review_rating = models.IntegerField(null=True, blank=True)
    review_content = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.product_id

