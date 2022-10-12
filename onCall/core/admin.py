from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class onCallResource(resources.ModelResource):
    class meta:
        model=(Especialidad, SubEspecialidad , Guardia,  Profile)



@admin.register(Especialidad)
class EspecialidadProject(ImportExportModelAdmin, admin.ModelAdmin):
    resouce_class = onCallResource

    list_display = ('name', )
    search_fields = ('name',)


@admin.register(SubEspecialidad)
class SubEspecialidadProject(ImportExportModelAdmin, admin.ModelAdmin):
    resouce_class = onCallResource

    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Guardia)
class GuardiaProject(ImportExportModelAdmin, admin.ModelAdmin):
    resouce_class = onCallResource

    list_display = ('name', )
    search_fields = ('name', )





@admin.register(Profile)
class ProfileProject(ImportExportModelAdmin, admin.ModelAdmin):
    resouce_class = onCallResource
    #readonly_fields = ('created', 'updated')
    list_display = ('name','nivel','phone_guardia', 'phone_asignado','phone_otro', 'fijo_oficina', 'fijo_casa','guardias_especialistas')
    #list_filter = ('region','region__zona__name' ,'guardia__name')
    search_fields = ('name', )
    raw_id_fields = ('guardia', )
    #list_editable = ('fecha_inicio', 'fecha_fin', 'activo')

    def guardias_especialistas(self, obj):
        return "; \n".join(
            [c.name  for c in obj.guardia.all().order_by("name")])

    guardias_especialistas.short_description = "Guardias"

    #def regionZona(self, obj):
     #   return Zona.objects.get(get_zona__id = obj.id)


    #regionZona.short_description = "Zona"







@admin.register(GuardiaEspecialista)
class GuardiaEspecialistaProject(ImportExportModelAdmin, admin.ModelAdmin):
    resouce_class = onCallResource
    list_display = ('name', 'fecha_inicio', 'fecha_fin','guardiasespecialistas')


    def guardiasespecialistas(self, obj):
        return "; \n".join(
            [c.name  for c in obj.guardia.all().order_by("name")])

    guardiasespecialistas.short_description = "Guardias"


@admin.register(Zona)
class ZonaProject(ImportExportModelAdmin, admin.ModelAdmin):
    resouce_class = onCallResource
    list_display = ('name',)



@admin.register(Region)
class RegionProject(ImportExportModelAdmin, admin.ModelAdmin):
    resouce_class = onCallResource
    list_display = ('name',)





