from django.shortcuts import render
from django.utils import timezone
from django.views.generic import FormView, DetailView

from .models import Concept
from .forms import ConceptForm


class ConceptDetailView(DetailView):
    model = Concept

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ConceptStoreView(FormView):
    form_class = ConceptForm
    template_name = 'wiki/create.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        concept = form.save(False)
        concept.created_at = timezone.now()
        concept.updated_at = concept.created_at
        concept.save(True)
        return super().form_valid(form)
