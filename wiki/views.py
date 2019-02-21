from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView
from django.conf import settings


from .models import Concept
from .forms import ConceptForm


class ConceptListView(ListView):
    context_object_name = 'concept_list'
    paginate_by = settings.PAGINATE_BY
    model = Concept


class ConceptDetailView(DetailView):
    model = Concept

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ConceptStoreView(CreateView):
    form_class = ConceptForm
    template_name = 'wiki/concept_create.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        concept = form.save(False)
        concept.created_at = timezone.now()
        concept.updated_at = concept.created_at
        concept.save(True)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wiki:concept-detail', kwargs={'pk': self.object.id})


class IndexView(ConceptListView):
    """首页"""
    pass
