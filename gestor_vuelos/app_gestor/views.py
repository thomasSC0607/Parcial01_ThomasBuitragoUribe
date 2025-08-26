from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Flight
from django import forms
from django.core.exceptions import ValidationError
from django.views.generic import ListView
from django.db.models import Count, Avg



# Create your views here.
class HomeView(TemplateView):
    template_name = "app_gestor/home.html"
    
    
class FlightForm(forms.ModelForm):
    nombre = forms.CharField(required=True)
    tipo = forms.ChoiceField(choices=Flight.TIPO_VUELOS, required=True)
    precio = forms.FloatField(required=True)

    class Meta:
        model = Flight
        fields = ['nombre', 'tipo', 'precio']

    def clean_price(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise ValidationError('Price must be greater than zero.')
        return precio

    
    
class FlightCreateView(TemplateView):
    template_name = 'app_gestor/crear_vuelo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FlightForm()
        return context

    def post(self, request, *args, **kwargs):
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flight-list')
        return self.render_to_response(self.get_context_data(form=form))
    
    
class FlightListView(TemplateView):
    template_name = 'app_gestor/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flights'] = Flight.objects.all().order_by('precio')
        return context
    
    
class FlightStatsView(TemplateView):
    template_name = 'app_gestor/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'nacionales': Flight.objects.filter(tipo='Nacional').count(),
            'internacionales': Flight.objects.filter(tipo='Internacional').count(),
            'promedio_nacional': Flight.objects.filter(tipo='Nacional').aggregate(Avg('precio'))['precio__avg']
        }
        return context
