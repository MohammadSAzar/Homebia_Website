from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, DetailView

from .models import Counseling, Session, Visit

# Counseling Views
class CounselingCreateView(CreateView):
    model = Counseling
    fields = ['customer_type', 'counseling_type', 'date', 'time', 'name_and_family', 'phone_number']
    template_name = 'services/counseling.html'

class CounselingDetailView(DetailView):
    context_object_name = 'counseling'
    template_name = 'services/counseling_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(klass=Counseling, id=self.kwargs.get("id"))

# Counseling Views
# def services_counseling_create_view(request):
#     if request.method == 'POST':
#         form = CounselingForm(request.POST)
#         if form.is_valid():
#             form.save()
#             context = {
#                 'form': form,
#             }
#             return render(request, 'services/counseling.html', context)
#     else:
#         form = CounselingForm()
#     return render(request, 'services/counseling.html', {'form': form})

# def services_counseling_detail_view(request, counseling_id):
#     counseling = Counseling.objects.get(id=counseling_id)
#     context = {
#         'counseling': counseling,
#     }
#     return render(request, 'services/counseling_detail.html', context)


# Session Views
class SessionCreateView(CreateView):
    model = Session
    fields = ['city', 'customer_type', 'date', 'time', 'name_and_family', 'phone_number']
    template_name = 'services/session.html'

class SessionDetailView(DetailView):
    context_object_name = 'session'
    template_name = 'services/session_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(klass=Session, id=self.kwargs.get("id"))


# Visit Views
class VisitCreateView(CreateView):
    model = Visit
    fields = ['city', 'date', 'time', 'name_and_family', 'phone_number']
    template_name = 'services/visit.html'

class VisitDetailView(DetailView):
    context_object_name = 'visit'
    template_name = 'services/visit_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(klass=Visit, id=self.kwargs.get("id"))



