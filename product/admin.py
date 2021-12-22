from functools import partial
from django.forms import ModelChoiceField
from django.contrib import admin

from .models import Category, Computers, Laptops, Comment


class autoslugAdmin(admin.ModelAdmin):
    """Creating autoslug and autocategory form to the model"""
    prepopulated_fields = {'slug': ('name',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if(request.path.split('/')[-2] == 'change'):
            category_name = request.path.split('/')[-4]
        else:
            category_name = request.path.split('/')[-3]
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug=category_name))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
        


admin.site.register(Category, autoslugAdmin)
admin.site.register(Computers, autoslugAdmin)
admin.site.register(Comment)
admin.site.register(Laptops, autoslugAdmin)
