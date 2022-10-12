from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from .forms import GuardiaEspecialistaForm
from django.views.generic.list import ListView, MultipleObjectMixin
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

now = timezone.now()
# Vista para la pagina Home y ordenar productos en la portada
class HomePageView(TemplateView):
    template_name = "core/index.html"







#Funcional Muestra las Especialidades
class EspecialidadListView(ListView):
    template_name = "core/especialidades_list.html"
    model = Especialidad
    paginate_by = 10


    def get_context_data(self, **kwargs):
        object_list = Especialidad.objects.all()
        context = super(EspecialidadListView, self).get_context_data(object_list=object_list, **kwargs)
        queryset = self.request.GET.get('search')

        if queryset:
            object_list = Guardia.objects.filter(Q(name__icontains=queryset)).distinct()
            context = super(EspecialidadListView, self).get_context_data(object_list=object_list, buscar =True, **kwargs)
        return context



#Funcional Muestra las regiones
class RegionesListView(ListView):
    template_name = "core/regiones_list.html"
    model = Region

    def get_context_data(self, **kwargs):
        object_list = Especialidad.objects.all()
        context = super(RegionesListView, self).get_context_data(object_list=object_list, **kwargs)
        queryset = self.request.GET.get('search')

        if queryset:
            object_list = Guardia.objects.filter(Q(name__icontains=queryset)).distinct()
            context = super(RegionesListView, self).get_context_data(object_list=object_list, buscar =True, **kwargs)
        return context




class GuardiaRegionDetail(DetailView, MultipleObjectMixin):
    template_name = "core/guardia_region_detail.html"
    model = Region
    """ 
    def get_context_data(self, **kwargs):
        object_list = Especialidad.objects.filter(
            Q(get_especialidad__get_sub_especilidad__region__id=self.object.id)
            ).distinct()
        context = super(GuardiaRegionDetail, self).get_context_data(object_list=object_list, **kwargs)
        queryset = self.request.GET.get('search')
        if queryset:
            object_list = Especialidad.objects.filter(get_especialidad__get_sub_especilidad__region__id=self.object.id).filter(
                Q(name__icontains=queryset)
            ).distinct()
            context = super(GuardiaRegionDetail, self).get_context_data(object_list=object_list, **kwargs)
        return context
    """

    def get_context_data(self, **kwargs):
        object_list = Especialidad.objects.filter(
            Q(get_especialidad__get_sub_especilidad__region__id=self.object.id)
            ).distinct()
        context = super(GuardiaRegionDetail, self).get_context_data(object_list=object_list, **kwargs)
        queryset = self.request.GET.get('search')

        if queryset:
            object_list = Guardia.objects.filter(Q(name__icontains=queryset)).distinct()
            context = super(GuardiaRegionDetail, self).get_context_data(object_list=object_list, buscar=True, **kwargs)
        return context



class EspecialidadDetail(DetailView, MultipleObjectMixin):
    template_name = "core/sub_especialidad_list.html"
    model = Especialidad
    """ 
    def get_context_data(self, **kwargs):
        object_list = SubEspecialidad.objects.filter(especialidad_id=self.object.id)
        context = super(EspecialidadDetail, self).get_context_data(object_list=object_list, **kwargs)
        queryset = self.request.GET.get('search')
        if queryset:
            object_list = SubEspecialidad.objects.filter(especialidad_id=self.object.id).filter(
                Q(name__icontains=queryset)
            ).distinct()
            context = super(EspecialidadDetail, self).get_context_data(object_list=object_list, **kwargs)

        return context
    """

    def get_context_data(self, **kwargs):
        object_list = SubEspecialidad.objects.filter(especialidad_id=self.object.id)
        context = super(EspecialidadDetail, self).get_context_data(object_list=object_list, **kwargs)
        queryset = self.request.GET.get('search')

        if queryset:
            object_list = Guardia.objects.filter(Q(name__icontains=queryset)).distinct()
            context = super(EspecialidadDetail, self).get_context_data(object_list=object_list, buscar=True, **kwargs)
        return context



    def get_success_url(self):
        return reverse_lazy('core:especialidad_detail', args=[self.object.id])





class SubEspecialidadDetail(DetailView, MultipleObjectMixin):
    template_name = "core/guardia_list.html"
    model = SubEspecialidad

    def get_context_data(self, **kwargs):
        object_list = Guardia.objects.filter(sub_especilidad_id=self.object.id)
        context = super(SubEspecialidadDetail, self).get_context_data(object_list=object_list, **kwargs)

        queryset = self.request.GET.get('search')
        if queryset:

            object_list = Guardia.objects.filter(sub_especilidad_id=self.object.id).filter(
                Q(name__icontains=queryset)
            ).distinct()
            context = super(SubEspecialidadDetail, self).get_context_data(object_list=object_list, **kwargs)


        return context






class GuardiaDetail(DetailView):
    template_name = "core/guardia_detail.html"
    model = Guardia

    def get_context_data(self, **kwargs):
        object_list = GuardiaEspecialista.objects.filter(guardia__id=self.object.id).filter(fecha_inicio__lte=now).filter(fecha_fin__gte=now)
        context = super(GuardiaDetail, self).get_context_data(object_list=object_list, **kwargs)

        queryset = self.request.GET.get('search')
        if queryset:
            object_list =GuardiaEspecialista.objects.filter(guardia__id=self.object.id).filter(fecha_inicio__lte=now).filter(fecha_fin__gte=now).filter(
                Q(name__name__icontains=queryset)
            ).distinct()
            context = super(GuardiaDetail, self).get_context_data(object_list=object_list, **kwargs)

        return context




class TablaDetail(DetailView):
    template_name = "core/tabla.html"
    model = Guardia

    def get_context_data(self, **kwargs):
        object_list = Profile.objects.filter(guardia__id=self.object.id).filter(activo=True)
        context = super(TablaDetail, self).get_context_data(object_list=object_list, **kwargs)
        return context



class GuardiaSemanalCreate(CreateView):
    model = GuardiaEspecialista
    form_class = GuardiaEspecialistaForm
    template_name = "core/guardia_Semanal.html"

    def get_success_url(self):
        return reverse_lazy('core:guardiaSemanal_create') + "?ok"

    def get(self, request, *args, **kwargs):
        form = GuardiaEspecialistaForm
        guardias = Guardia.objects.none()
        profiles = Profile.objects.all()

        if request.is_ajax():
            id_profile = request.GET.get('id', None)
            #profiles = Profile.objects.all().filter(pk=id_profile)
            guardias = Guardia.objects.filter(get_guardias__id=id_profile)
            response_content = list(guardias.values())
            return JsonResponse(response_content, safe= False)

        context = {
            'form':form,
            'guardias': guardias,
            'profiles': profiles,

        }
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.cleaned_data)
            return self.get(request)


class GuardiasEspecialistasListView(ListView):
    template_name = "core/guardias_especialidades_list.html"
    model = GuardiaEspecialista
    paginate_by = 4

    def get_queryset(self):
        object_list = GuardiaEspecialista.objects.all()
        queryset = self.request.GET.get('search')
        if queryset:
            object_list = GuardiaEspecialista.objects.filter(
                Q(name__name__icontains=queryset)
            ).distinct()
        return object_list



class GuardiasEspecialistasUpdateView(UpdateView):
    template_name = "core/guardias_especialidades_update.html"
    model = GuardiaEspecialista
    #fields = ['fecha_inicio','fecha_fin','guardia']
    form_class = GuardiaEspecialistaForm


    def get_success_url(self):
        return reverse_lazy('core:guardias_especialistas_update', args=[self.object.id]) + "?ok"






class GuardiasEspecialistasDeleteView(DeleteView):
    template_name = "core/guardias_especialidades_delete.html"
    model = GuardiaEspecialista
    success_url = reverse_lazy('core:guardias_especialistas_list')


# Create your views here.
def calendario(request):
    guardias_especialistas = GuardiaEspecialista.objects.none()
    guardias = Guardia.objects.all()
    queryset = request.GET.get('guardia')
    guardia_color = None

    if queryset:
        if queryset == ('Seleccione...'):
            guardias_especialistas = GuardiaEspecialista.objects.none()


        elif queryset:
            guardias_especialistas =  GuardiaEspecialista.objects.filter(
                    Q(guardia__id=queryset)
                ).distinct()

            guardia_color = Guardia.objects.get(pk=queryset)



    context = {
        'guardias_especialistas': guardias_especialistas,
        'guardias': guardias,
        'guardia_color': guardia_color,
    }
    return render(request, "core/calendario.html", context)


