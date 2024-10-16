from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreferences
import datetime

# Create your views here.

def search_incomes(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        incomes = Income.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
            date__istartswith=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) 
        
        data = incomes.values()

        return JsonResponse(list(data), safe=False)



@login_required(login_url='authentication/login')
def index(request):
    incomes = Income.objects.filter(owner=request.user)

    paginator = Paginator(incomes, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    # currency_id = UserPreferences.objects.get(user=request.user)
    # if currency_id:
    #     currency = currency_id.currency
    # else:
    #     currency = []
    try:
        userpreferences = UserPreferences.objects.get(user=request.user)
        currency = userpreferences.currency
    except UserPreferences.DoesNotExist:
        currency = []

    context = {
        'incomes': incomes,
        'page_obj': page_obj,
        'currency': currency
    }

    return render(request,'incomes/index.html', context)


def add_income(request):
    print ('heyy')

    sources = Source.objects.all()
    context = {
        'sources':sources
        }
    if request.method == 'GET':        
        return render(request,'incomes/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date'] if request.POST['income_date'] else None
        source_id = request.POST['source']
        source = Source.objects.get(id=source_id)
        Income.objects.create(amount=amount, description=description, source=source, date=date, owner=request.user)
        messages.success(request, 'Income created')

        return redirect('incomes')
    
def edit_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources':sources
    }
    print (context['values'].date)
    if request.method=='GET':
        return render(request, 'incomes/edit_income.html', context)
    
    if request.method=='POST':

        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date'] if request.POST['income_date'] else None
        source_id = request.POST['source']
        # print (source_id)
        source = Source.objects.get(id=source_id)
        income.owner = request.user
        income.amount = amount
        income.description = description
        income.date = date
        income.source = source


        income.save()

        messages.info(request, 'Income Saved')
        return redirect ('incomes')
    

def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income deleted')
    return redirect('incomes')


def incomes_source_summary(request):
    print ('incomes_source_summary')
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=180)
    incomes = Income.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=todays_date)

    result = {}

    def get_source(income):
        return income.source
    source_list = list(set(map(get_source, incomes)))

    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = incomes.filter(source=source)
        for item in filtered_by_source:
            amount += item.amount
        return amount



    for inc in incomes:
        for src in source_list:
            result[src.name] = get_income_source_amount(src)
    print (result)
    return JsonResponse({'income_source_data' : result}, safe=False)

def stats_view(request):
    return render(request, 'incomes/stats.html')
        
    