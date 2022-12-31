from django.shortcuts import render, redirect
from .models import Task, ExcelFile
from .form import TaskForm, AuthForm, RegForm
from django.urls import reverse, reverse_lazy
from django.db.models import Sum, Avg
from django.views.generic import ListView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd
from django.http import HttpResponse
import datetime
import csv

def export_to_csv(req):
    objs = Task.objects.filter(author=req.user).values_list('author', 'money', 'category', 'budget', 'description', 'date')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['author', 'money', 'category', 'budget', 'description', 'date'])
    for obj in objs:
        writer.writerow(obj)
    
    return response

def import_data_to_db(req):
    if req.method == 'POST':

        file = req.FILES['files']
        obj = ExcelFile.objects.create(
            file = file
        )
        path = str(obj.file)
        df = pd.read_excel(path)

        model_instances = [
            Task(
                author= req.user,
                money=df['Сумма'][i],
                category=df['Категория'][i],
                budget=df['Бюджет'][i],
                description=df['Описание'][i],
                date=df['Дата'][i],
            ) for i in range(len(df.index))
        ]
        
        Task.objects.bulk_create(model_instances)

    return render(req, 'main/import.html')

class data(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'main/data.html'
    context_object_name = 'tasks'
    ordering = ['-date']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.GET:
            category = self.request.GET.get('category', default='')
            budget = self.request.GET.get('budget', default='')
            description = self.request.GET.get('description', default='')
            date = self.request.GET.get('date', default='')
            context['tasks'] = Task.objects.filter(category__icontains=category, budget__icontains=budget, description__icontains=description, date__icontains=date).order_by('-date')
        else:
            context['tasks'] = Task.objects.all().order_by('-date')
        return context

class index(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'main/index.html'
    form_class = TaskForm
    success_url = reverse_lazy('home')   

    def form_valid(self, form):
        print('dd')
        print(form.save(commit=False))
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

class graf(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'main/graf.html'
    context_object_name = 'tasks'
    form_class = TaskForm

    def get_context_data(self, *args, **kwargs):
        start = self.request.GET.get('yearstart', default=str(datetime.date.today().year) + '-' + str(datetime.date.today().month) + '-01')
        end = self.request.GET.get('yearend', default=str(datetime.date.today().year) + '-' + str(datetime.date.today().month) + '-31')

        context = super().get_context_data(*args, **kwargs)
        context['sumbydate'] = Task.objects.filter(author=self.request.user, date__range=[start, end]).values('date').order_by('date').annotate(sum=Sum('money'))
        context['sumbycat'] = Task.objects.filter(author=self.request.user, date__range=[start, end]).values('category').order_by('category').annotate(sum=Sum('money'))
        context['sumbybud'] = Task.objects.filter(author=self.request.user, date__range=[start, end]).values('budget').order_by('budget').annotate(sum=Sum('money'))
        context['avgmoney'] = int(Task.objects.filter(author=self.request.user, date__range=[start, end]).values('date').order_by('date').annotate(sum=Sum('money')).aggregate(avg=Avg('sum')).get('avg') or 0)
        context['balance'] = 140000 - int(Task.objects.filter(author=self.request.user, date__range=[start, end]).aggregate(sum=Sum('money')).get('sum') or 0)
        return context

def delete(req, pk):
    del_task = Task.objects.get(pk=pk)
    del_task.delete()
    return redirect(reverse('data'))

class auth(LoginView):
    template_name = 'main/auth.html'
    form_class = AuthForm
    success_url = reverse_lazy('home')  
    def get_success_url(self):
        return self.success_url

class reg(CreateView):
    model = User
    template_name = 'main/reg.html'
    form_class = RegForm
    success_url = reverse_lazy('auth')    

class logOut(LogoutView):
    next_page = reverse_lazy('auth')   
