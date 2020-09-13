from django.contrib import admin
from reviewapp.models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(ActivityLog)
admin.site.register(RatingEvaluationString)
