from django.shortcuts import render, redirect
# importing our Class-Based-Views (CBVs)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Finch, Toy
from .forms import FeedingForm


# GET - Home
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def finches_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', { 'finches': finches })
 
def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    toys_finch_doesnt_have = Toy.objects.exclude(id__in = finch.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'finches/detail.html', {
        'finch': finch, 
        'feeding_form': feeding_form, 
        'toys': toys_finch_doesnt_have,
    })

# CREATE, UPDATE, DELETE VIEWS

# inherit from the CBV - CreateView, then specify the model and fields

class FinchCreate(CreateView):
    model = Finch
    fields = '__all__'
    success_url = '/finches'





# Update View - extends the UpdateView class
class FinchUpdate(UpdateView):
    model = Finch
    
    fields = ['breed', 'description', 'age']

# Delete View - extends DeleteView
class FinchDelete(DeleteView):
    model = Finch

    success_url = '/finches'

# FEEDING AND RELATIONSHIP VIEW FUNCTIONS
def add_feeding(request, finch_id):
    # create a ModelForm instance using the data in request.POST
    form = FeedingForm(request.POST)

    if form.is_valid():
   
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('detail', finch_id=finch_id)

# LIST OF TOY VIEWS HERE
# ToyList
class ToyList(ListView):
    model = Toy
    template_name = 'toys/index.html'

# ToyDetail
class ToyDetail(DetailView):
    model = Toy
    template_name = 'toys/detail.html'

# ToyCreate
class ToyCreate(CreateView):
    model = Toy
    fields = ['name', 'color']

    def form_valid(self, form):
        return super().form_valid(form)

# ToyUpdate
class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']
    
# ToyDelete
class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys'
    
    
    
    
def assoc_toy(request, finch_id, toy_id):
  Finch.objects.get(id = finch_id).toys.add(toy_id)
  return redirect('detail', finch_id=finch_id)

def unassoc_toy(request, finch_id, toy_id):
  Finch.objects.get(id = finch_id).toys.remove(toy_id)
  return redirect('detail', finch_id=finch_id)