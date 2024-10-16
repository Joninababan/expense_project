from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreferences
import datetime

# Create your views here.

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) 
        
        data = expenses.values()
        # return JsonResponse('sadasd')

        return JsonResponse(list(data), safe=False)



@login_required(login_url='authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner=request.user)

    paginator = Paginator(expenses, 5)
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
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }

    return render(request,'expenses/index.html', context)


def add_expenses(request):
    print (request.POST)

    categories = Category.objects.all()
    context = {
        'categories':categories
        }
    if request.method == 'GET':        
        return render(request,'expenses/add_expenses.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date'] if request.POST['expense_date'] else None
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)
        Expense.objects.create(amount=amount, description=description, category=category, date=date, owner=request.user)
        messages.success(request, 'Expenses created')

        # return render(request,'expenses/index.html', context)
        return redirect('expenses')
    
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories':categories
    }
    print (context['values'].date)
    if request.method=='GET':
        return render(request, 'expenses/edit_expense.html', context)
    
    # category need to do
    if request.method=='POST':

        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date'] if request.POST['expense_date'] else None
        category_id = request.POST['category']
        print (category_id)
        category = Category.objects.get(id=category_id)
        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.date = date
        expense.category = category


        expense.save()

        messages.info(request, 'Expenses Saved')
        return redirect ('expenses')
    

def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expenses deleted')
    return redirect('expenses')


def expenses_category_summary(request):
    print ('expenses_category_summary')
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=180)
    expenses = Expense.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=todays_date)

    result = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount



    for exp in expenses:
        for categ in category_list:
            result[categ.name] = get_expense_category_amount(categ)
    print (result)
    return JsonResponse({'expense_category_data' : result}, safe=False)

def stats_view(request):
    return render(request, 'expenses/stats.html')
        
    