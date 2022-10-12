from django.urls import path
from . import views
from .views import HomePageView,EspecialidadListView,EspecialidadDetail, GuardiaDetail, TablaDetail, RegionesListView,GuardiaRegionDetail,SubEspecialidadDetail,GuardiasEspecialistasListView,GuardiasEspecialistasUpdateView, GuardiasEspecialistasDeleteView,GuardiaSemanalCreate



app_name= 'core'
urlpatterns = [
	path('', HomePageView.as_view(), name="home"),
	path('especialidades/', EspecialidadListView.as_view(), name="especialidades_list"),
	path('regiones/', RegionesListView.as_view(), name="regiones_list"),
	path('region/<int:pk>/', GuardiaRegionDetail.as_view(), name="guardia_region_detail"),


	path('especialidad/<int:pk>/', EspecialidadDetail.as_view(), name="especialidad_detail"),
	path('subespecialidad/<int:pk>/', SubEspecialidadDetail.as_view(), name="subespecialidad_detail"),
	path('guardia/<int:pk>/', GuardiaDetail.as_view(), name="guardia_detail"),
	path('tabla/<int:pk>/', TablaDetail.as_view(), name="tabla_detail"),


	path('create_guardia_semanal/', GuardiaSemanalCreate.as_view(), name='guardiaSemanal_create'),

	path('guardias/especialistas/', GuardiasEspecialistasListView.as_view(), name="guardias_especialistas_list"),
	path('guardias/especialistas/update/<int:pk>/', GuardiasEspecialistasUpdateView.as_view(), name="guardias_especialistas_update"),
	path('guardias/especialistas/delete/<int:pk>/', GuardiasEspecialistasDeleteView.as_view(), name="guardias_especialistas_delete"),

	path('guardias/calendario/', views.calendario, name="calendario"),


]