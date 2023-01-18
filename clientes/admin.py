from django.contrib import admin
from .models import Person, Documento


class Personadmin(admin.ModelAdmin):
    fieldsets = (
        ('Dados pessoais', {'fields': ('first_name', 'last_name', 'doc')}),
        ('Dados Complementares', {
            'classes': ('collapse',),
            'fields':  ('age', 'salary', 'photo')
        })
    )
    # fields = (('doc', 'first_name'), 'last_name', ('age', 'salary'), 'bio', 'photo',)
    list_display = ('doc', 'first_name', 'last_name', 'age', 'salary', 'bio', 'photo', 'has_foto')
    search_fields = ('id', 'first_name')

    def has_foto(self, obj):
        if obj.photo:
            return 'Sim'
        else:
            return 'Não'

    has_foto.short_description = 'Possui foto'


admin.site.register(Person, Personadmin)
admin.site.register(Documento)
