from django.db import models

class Comment(models.Model):
    u1_text = models.CharField(max_length=255)
    np_label = models.CharField(max_length=10, null=True)
    np_score = models.DecimalField(null=True, max_digits=5, decimal_places=2)
    data_added = models.DateTimeField(auto_now_add=True)