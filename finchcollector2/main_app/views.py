from django.shortcuts import render, redirect
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


class FinchCreate(CreateView):
    model = Finch
    fields = '__all__'
    success_url = '/finches'



class FinchUpdate(UpdateView):
    model = Finch
    
    fields = ['breed', 'description', 'age', 'notes']

class FinchDelete(DeleteView):
    model = Finch

    success_url = '/finches'

def add_feeding(request, finch_id):

    form = FeedingForm(request.POST)

    if form.is_valid():
   
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('detail', finch_id=finch_id)


class ToyList(ListView):
    model = Toy
    template_name = 'toys/index.html'


class ToyDetail(DetailView):
    model = Toy
    template_name = 'toys/detail.html'


class ToyCreate(CreateView):
    model = Toy
    fields = ['name', 'color']

    def form_valid(self, form):
        return super().form_valid(form)


class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']


class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys'
    
    
    
def assoc_toy(request, finch_id, toy_id):
  Finch.objects.get(id = finch_id).toys.add(toy_id)
  return redirect('detail', finch_id=finch_id)

def unassoc_toy(request, finch_id, toy_id):
  Finch.objects.get(id = finch_id).toys.remove(toy_id)
  return redirect('detail', finch_id=finch_id)