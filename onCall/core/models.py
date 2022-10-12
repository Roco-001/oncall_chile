from django.db import models
from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from django.utils import  timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, m2m_changed
from .task import telegram_api
now = timezone.now

# Create your models here.

def numeros_validos(value):
    value = str(value)
    if len(value) != 11:
        raise ValidationError("La longitud no corresponde con la establecidad de 11 digitos...")

    elif value[0] != '5':
        raise ValidationError("No comienza con 5")

    elif value[1] != '6':
        raise ValidationError("No contiene el  6 como segundo digito")




NIVEL = (
    (1, 'Especialista'),
    (2, 'Supervisor'),
    (3, 'Jefe de área'),
    (4, 'Gerente de área'),
    (5, 'Gerente'),
)


class Especialidad(models.Model):
    name  = models.CharField(max_length=200, verbose_name="Nombre de la Especialidad", blank=True, null=True)


    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"
        # Ordena de mas nuevo a mas antiguo
        ordering = ["name"]

    def __str__(self):
        return self.name


class SubEspecialidad(models.Model):
    name  = models.CharField(max_length=200, verbose_name="Nombre", blank=True, null=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name="get_especialidad",
                                verbose_name="Especialidad")


    class Meta:
        verbose_name = "Sub-Especialidad"
        verbose_name_plural = "Sub-Especialidades"
        # Ordena de mas nuevo a mas antiguo
        ordering = ["name"]

    def __str__(self):
        return self.name




class Zona(models.Model):
    name = models.CharField(max_length=200, verbose_name="Zona", blank=True, null=True)


    class Meta:
        verbose_name = "Zona"
        verbose_name_plural = "Zonas"
        # Ordena de mas nuevo a mas antiguo
        ordering = ["name"]

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre de la region", blank=True, null=True)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE, related_name="get_zona",
                                verbose_name="Zona", blank=True, null=True)



    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regiones"
        # Ordena de mas nuevo a mas antiguo
        ordering = ["name"]

    def __str__(self):
        return self.name


class Guardia(models.Model):
    name  = models.CharField(max_length=200, verbose_name="Nombre", blank=True, null=True)
    sub_especilidad = models.ForeignKey(SubEspecialidad, on_delete=models.CASCADE, related_name="get_sub_especilidad",
                                verbose_name="Sub-especilidad", blank=True, null=True)

    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="get_region",
                                        verbose_name="Región", blank=True, null=True)
    color_fondo = ColorField(verbose_name="Color de fondo", blank=True, null=True, default='#FFFFFF')
    color_texto = ColorField(verbose_name="Color del texto", blank=True, null=True, default='#FFFFFF')



    class Meta:
        verbose_name = "Guardia"
        verbose_name_plural = "Guardias"
        # Ordena de mas nuevo a mas antiguo
        ordering = ["name"]

    def __str__(self):
        return self.name



class Profile(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del Especialista", blank=True, null=True)
    email = models.EmailField(max_length=100, verbose_name="Email del Especialista", blank=True, null=True)
    nivel = models.IntegerField(choices=NIVEL, verbose_name="Nivel de Escalamiento", blank=True, null=True)
    phone_guardia = models.CharField(max_length=20, verbose_name="Teléfono de Guardia", blank=True, null=True, validators=[numeros_validos], help_text='Debe contener 11 digitos y empezar con 56')
    phone_asignado = models.CharField(max_length=20, verbose_name="Teléfono Asignado", blank=True, null=True, validators=[numeros_validos], help_text='Debe contener 11 digitos y empezar con 56')
    phone_otro = models.CharField(max_length=20, verbose_name="Teléfono de Otra Compañia", blank=True, null=True, validators=[numeros_validos], help_text='Debe contener 11 digitos y empezar con 56')
    fijo_oficina = models.CharField(max_length=20, verbose_name="Fijo Oficina", blank=True, null=True)
    fijo_casa = models.CharField(max_length=20, verbose_name="Fijo Casa", blank=True, null=True, validators=[numeros_validos], help_text='Debe contener 11 digitos y empezar con 56')
    guardia = models.ManyToManyField(Guardia, related_name="get_guardias", verbose_name="Guardia", blank=True)


    class Meta:
        verbose_name = "Especialista"
        verbose_name_plural = "Especialistas"
        # Ordena de mas nuevo a mas antiguo
        ordering = ["nivel"]

    def __str__(self):
        return self.name



class GuardiaEspecialista(models.Model):
    name = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="get_especialistas",
                              verbose_name="Seleccione el especialista", blank=True, null=True)
    activo = models.BooleanField(verbose_name="Trae la Guardia", blank=True, null=True, default=True)
    fecha_inicio = models.DateTimeField(verbose_name="Fecha Inicio", blank=True, null=True,  default=now)
    fecha_fin = models.DateTimeField(verbose_name="Fecha Fin", blank=True, null=True,  default=now)
    guardia =  models.ManyToManyField(Guardia, related_name="get_guardiasespecialistas", verbose_name="Guardia", blank=True)



    class Meta:
        verbose_name = "Guardia por Especialista"
        verbose_name_plural = "Guardias por Especialistas"
        # Ordena de mas nuevo a mas antiguo
        ordering = ["name",]

    def __str__(self):
        return str(self.name.name)






"""
@receiver(pre_save, sender=Especialista)
def historico(sender,instance, **kwargs):
    try:
        old_instance = sender.objects.get(pk=instance.pk)
        if (old_instance.activo != instance.activo or old_instance.fecha_inicio != instance.fecha_inicio or old_instance.fecha_fin != instance.fecha_fin) and instance.activo ==True:
            guardias = Guardia.objects.filter(get_guardias=instance.pk)
            lista = []
            for guardia in guardias:
                lista.append(guardia.name)
            strA = "\n".join(lista)
            Historico.objects.create(name=old_instance.name, fecha_inicio= old_instance.fecha_inicio,fecha_fin=old_instance.fecha_fin, activo= old_instance.activo, guardia=strA)
            texto = f'Se notifica el siguiente cambio para la guardia de la {instance.zona}/{instance.region}:\n Acutalmente está de guardia {instance.name} con sus telefonos de contactos...'

            telegram_api(texto, '1663958489')

    except sender.DoesNotExist:
        pass



@receiver(m2m_changed, sender=Especialista.guardia.through)
def historico_m2m(sender,instance,action, **kwargs):
    try:
        if action =="pre_add":
            lista_pre = []
            for guardia in instance.guardia.all():
                lista_pre.append(guardia.name)
            str_pre = "\n".join(lista_pre)
            texto= f'Hubo un cambio en la guardia de {instance.name}:\nAntes tenia las siguientes guardias\n{str_pre}'
            telegram_api(texto, '1663958489')

        elif action=="post_add":
            lista_post = []
            for guardia in instance.guardia.all():
                lista_post.append(guardia.name)
            str_post = "\n".join(lista_post)
            texto = f'Ahora tiene las siguientes guardias:\n {str_post}'
            telegram_api(texto, '1663958489')
            Historico.objects.create(name=instance.name, fecha_inicio=instance.fecha_inicio,
                                     fecha_fin=instance.fecha_fin, activo=instance.activo,
                                     guardia=f'Guardias actualizadas:\n{str_post}')

    except sender.DoesNotExist:
        pass


"""

