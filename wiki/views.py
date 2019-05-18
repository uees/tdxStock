from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import ConceptForm
from .models import Concept


class ConceptListView(ListView):
    context_object_name = 'concept_list'
    paginate_by = settings.PAGINATE_BY
    model = Concept

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            query = Q()
            for key in q.split():
                query = query & (Q(name__icontains=key) | Q(description__icontains=key))

            return Concept.objects.filter(query).all()

        return super().get_queryset()


class ConceptDetailView(DetailView):
    model = Concept

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ConceptCreateView(LoginRequiredMixin, CreateView):
    form_class = ConceptForm
    template_name = 'wiki/concept_form.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        concept = form.save(False)
        concept.description_html = self.request.POST.get('description_html')
        concept.created_at = timezone.now()
        concept.updated_at = concept.created_at
        concept.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wiki:concept-detail', kwargs={'pk': self.object.id})


class ConceptUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ConceptForm
    template_name = 'wiki/concept_form.html'
    model = Concept

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        self.object.name = form.cleaned_data['name']
        self.object.description = form.cleaned_data['description']
        self.object.description_html = self.request.POST.get('description_html')
        self.object.updated_at = timezone.now()
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wiki:concept-detail', kwargs={'pk': self.object.id})


@login_required
def delete(request, concept_id):
    concept = get_object_or_404(Concept, pk=concept_id)
    concept.delete()

    return redirect(reverse('wiki:concept-list'))


class IndexView(ConceptListView):
    """首页"""
    pass
