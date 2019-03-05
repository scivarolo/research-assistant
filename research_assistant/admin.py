from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Paper)
admin.site.register(Tag)
admin.site.register(List)
admin.site.register(Author)
admin.site.register(Journal)