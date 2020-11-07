from django.contrib import admin
from .models import ElectionsAminitrator, Election, Voter

admin.site.register(ElectionsAminitrator)
admin.site.register(Election)
admin.site.register(Voter)

# Register your models here.
