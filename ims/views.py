from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
import datetime
from itertools import chain
from datetime import timezone
from django.db.models import Q

# Create your views here.

day = datetime.datetime.now().day
month = datetime.datetime.now().month
year = datetime.datetime.now().year

@login_required(login_url='login')
def index(request):
    user = Profile.objects.get(user=request.user)
    return render(request, 'index.html', {'user':user})

@login_required(login_url='login')
def user_home(request):
    user = Profile.objects.get(user=request.user)
    return render(request, 'user-home.html', {'user':user})

@login_required(login_url='login')
def sales(request):
    user = Profile.objects.get(user=request.user)
    return render(request, 'sales.html', {'user':user})

@login_required(login_url='login')
def history(request):
    user = Profile.objects.get(user=request.user)
    histories = History.objects.all()
    return render(request, 'history.html', {'user':user, 'histories':histories})

@login_required(login_url='login')
def invoice(request, id):
    user = Profile.objects.get(user=request.user)
    invs = Sales.objects.get(id=id)
    return render(request, 'invoice.html', {'user':user, 'invs':invs})

@login_required(login_url='login')
def product(request):
    user = Profile.objects.get(user=request.user)
    products = Stock.objects.all()
    return render(request, 'products.html', {'user':user, 'products':products})

@login_required(login_url='login')
def view_sales(request):
    user = Profile.objects.get(user=request.user)
    sales = Sales.objects.all()
    sum_a = sum([tran.total_price for tran in sales])
    context = {
        'user':user,
        'sales':sales,
        'sum_a':sum_a,
    }
    return render(request, 'view-sales.html', context)

@login_required(login_url='login')
def get_product_price(request, product_name):
    try:
        stock_items = Stock.objects.filter(product_name=product_name)
        data = [{'sale_price': item.sale_price} for item in stock_items]
        return JsonResponse({'data': data})
    except Stock.DoesNotExist:
        return JsonResponse({'data': []})

@login_required(login_url='login')
def sales_form(request):
    user = Profile.objects.get(user=request.user)
    stock = Stock.objects.all()
    products = Stock.objects.values('product_name')
    c_user = User.objects.get(username=request.user)
    users = c_user.username

    if request.method == 'POST':
        client_name = request.POST['client-name']
        client_phone = request.POST['client-phone']
        client_address = request.POST['client-address']

        product_names = request.POST.getlist('product[]')
        prices = request.POST.getlist('price[]')
        quantities = request.POST.getlist('quantity[]')

        total_qtn = 0
        total_price = 0
        product_summary = []
        date = datetime.datetime.now().strftime("%d/%m/%Y")  # e.g. "01/08/2025"

        for i in range(len(product_names)):
            pname = product_names[i]
            price = int(prices[i])
            qtn = int(quantities[i])
            
            # Check quantity available
            try:
                stock_item = Stock.objects.get(product_name=pname)
            except Stock.DoesNotExist:
                messages.info(request, f"Product '{pname}' does not exist.")
                return redirect('sales-form')

            if qtn > stock_item.product_qtn:
                messages.info(request, f"The product '{pname}' is too low. Only {stock_item.product_qtn} remaining.")
                return redirect('sales-form')

            # Update total
            total_qtn += qtn
            total_price += price * qtn
            product_summary.append(pname)

        # Update stock quantities and save records
        for i in range(len(product_names)):
            pname = product_names[i]
            qtn = int(quantities[i])
            stock_item = Stock.objects.get(product_name=pname)
            stock_item.product_qtn -= qtn
            stock_item.save()

        # Save sales, history, and transaction
        Sales.objects.create(
            client_name=client_name,
            client_phone=client_phone,
            client_address=client_address,
            products=", ".join(product_summary),
            total_qtn=total_qtn,
            total_price=total_price,
            user=users,
            date=date
        )

        History.objects.create(
            client_name=client_name,
            client_phone=client_phone,
            client_address=client_address,
            products=", ".join(product_summary),
            total_qtn=total_qtn,
            total_price=total_price,
            user=users,
            date=date
        )

        Transaction.objects.create(
            date=date,
            transactions=total_price
        )

        return redirect('view-sales')

    return render(request, 'sales-form.html', {
        'user': user,
        'stock': stock,
        'products': products
    })

# @login_required(login_url='login')
# def sales2(request):
#     user = Profile.objects.get(user=request.user)
#     stock = Stock.objects.all()
#     products = Stock.objects.values('product_name')
#     c_user = User.objects.get(username=request.user)
#     users = c_user.username 

#     if request.method == 'POST':
#         client_name = request.POST['client-name']
#         client_phone = request.POST['client-phone']
#         client_address = request.POST['client-address']

#         product1 = request.POST['product1']
#         p1_price = request.POST['p1-price']
#         p1_qtn = int(request.POST['p1-qtn'])

#         product2 = request.POST['product2']
#         p2_price = request.POST['p2-price']
#         p2_qtn = int(request.POST['p2-qtn'])
#         date = f"{month}/{day}/{year}"

#         qtn1 = Stock.objects.get(product_name=product1)
#         qtn_1 = Stock.objects.filter(product_name=qtn1)
#         qtn2 = Stock.objects.get(product_name=product2)
#         qtn_2 = Stock.objects.filter(product_name=qtn2)

#         price = int(p1_qtn) * int(p1_price)
#         price2 = int(p2_qtn) * int(p2_price)

#         total_qtn = int(p1_qtn) + int(p2_qtn)
#         total_price = int(price) + int(price2)
#         for q1 in qtn_1:
#             pass
#         for q2 in qtn_2:
#             pass
#         if client_name is not None:
#             if p1_qtn > q1.product_qtn:
#                 messages.info(request, 'This product  '+str(q1.product_name)+' is too low the only quantity remaining is '+str(q1.product_qtn))
#                 return redirect('sales2')
#             elif p2_qtn > q2.product_qtn:
#                 messages.info(request, 'This product '+str(q2.product_name)+' is too low the only quantity remaining is '+str(q2.product_qtn))
#                 return redirect('sales2')
#             else:
#                 for q1 in qtn_1:
#                     new_qtn1 = int(q1.product_qtn) - int(total_qtn)
#                 for q2 in qtn_2:
#                     new_qtn2 = int(q2.product_qtn) - int(total_qtn)
#                     sales = Sales.objects.create(
#                         client_name=client_name, client_phone=client_phone, client_address=client_address,
#                         products=f"{product1}, {product2}",
#                         total_qtn=total_qtn, user=users,
#                         total_price=total_price, date=date
#                     )
#                     sales.save()
#                     new_history = History.objects.create(
#                         client_name=client_name, client_phone=client_phone, client_address=client_address,
#                         products=f"{product1}, {product2}", user=users,
#                         total_qtn=total_qtn, date=date,
#                         total_price=total_price
#                     )
#                     new_history.save()
#                     new_transaction = Transaction.objects.create(date=date, transactions=total_price)
#                     new_transaction.save()
#                     q1.product_qtn = new_qtn1
#                     q1.save()
#                     q2.product_qtn = new_qtn2
#                     q2.save()
#                     return redirect('view-sales')

#         else:
#             messages.info(request, 'There is a missing required input!!!')
#             return redirect('sales-form')
#     else:
#         context = {
#             'user':user,
#             'stock':stock,
#             'products':products,
#         }
#         return render(request, 'sales2.html', context)

# @login_required(login_url='login')
# def sales1(request):
#     user = Profile.objects.get(user=request.user)
#     stock = Stock.objects.all()
#     products = Stock.objects.values('product_name')
#     c_user = User.objects.get(username=request.user)
#     users = c_user.username

#     if request.method == 'POST':
#         client_name = request.POST['client-name']
#         client_phone = request.POST['client-phone']
#         client_address = request.POST['client-address']

#         product1 = request.POST['product1']
#         p1_price = request.POST['p1-price']
#         p1_qtn = int(request.POST['p1-qtn'])
#         date = f"{day}/{month}/{year}"

#         qtn1 = Stock.objects.get(product_name=product1)
#         qtns = Stock.objects.filter(product_name=qtn1)

#         price = int(p1_qtn) * int(p1_price)

#         total_qtn = int(p1_qtn)
#         total_price = price

#         if client_name is not None:
#             for q in qtns:
#                 if p1_qtn > q.product_qtn:
#                     messages.info(request, 'This product is low..')
#                     return redirect('sales1')
#                 else:
#                     new_qtn1 = int(q.product_qtn) - int(total_qtn)
#                     sales = Sales.objects.create(
#                         client_name=client_name, client_phone=client_phone, client_address=client_address,
#                         products=product1, user=users,
#                         total_qtn=int(p1_qtn), date=date,
#                         total_price=total_price
#                     )
#                     sales.save()
#                     new_history = History.objects.create(
#                         client_name=client_name, client_phone=client_phone, client_address=client_address,
#                         products=product1, user=users,
#                         total_qtn=int(p1_qtn), date=date,
#                         total_price=total_price
#                     )
#                     new_history.save()
#                     new_transaction = Transaction.objects.create(date=date, transactions=total_price)
#                     new_transaction.save()
#                     q.product_qtn = new_qtn1
#                     q.save()
#                     return redirect('view-sales')

#         else:
#             messages.info(request, 'There is a missing required input!!!')
#             return redirect('sales-form')
#     else:
#         return render(request, 'sales1.html', {'user':user, 'stock':stock, 'products':products})

def get_price(request, product, *args, **kwargs):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        products = Stock.objects.filter(product_name=product).values('id', 'sale_price')
        return JsonResponse({'data': list(products)})
    
    return HttpResponse('Wrong request')

@login_required(login_url='login')
def user_add(request):
    user = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password2 == password:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exist !!!')
                return redirect('add-user')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already exist !!!')
                return redirect('add-user')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # create a profile object for the user.
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                messages.info(request, 'User created successfully..')
                return redirect('add-user')
        else:
            messages.info(request, 'password and comfirm password missed match !!!!')
            return redirect('add-user')

    else:
        return render(request, 'add-user.html', {'user':user})

@login_required(login_url='login')
def view_user(request):
    profile = Profile.objects.all()
    user = Profile.objects.get(user=request.user)
    return render(request, 'view-user.html', {'profile':profile, 'user':user})

@login_required(login_url='login')
def profile(request, id):
    user = Profile.objects.get(user=request.user)
    user_profile = Profile.objects.get(id_user=id)

    if request.method == 'POST':

        if request.FILES.get('img') == None:
            image = user_profile.profileimg
            full_name = request.POST['full-name']
            user_address = request.POST['address']
            user_phone = request.POST['phone']

            user_profile.profileimg = image
            user_profile.full_name = full_name
            user_profile.user_address = user_address
            user_profile.user_phone = user_phone
            user_profile.save()

        if request.FILES.get('img') != None:
            image = request.FILES.get('img')
            full_name = request.POST['full-name']
            user_address = request.POST['address']
            user_phone = request.POST['phone']

            user_profile.profileimg = image
            user_profile.full_name = full_name
            user_profile.user_address = user_address
            user_profile.user_phone = user_phone
            user_profile.save()

        return redirect('view-user')
    return render(request, 'profile.html', {'user_profile': user_profile, 'user':user})


@login_required(login_url='login')
def edit_user(request, id):
    user = Profile.objects.get(user=request.user)
    user_detail = User.objects.get(id=id)

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        user_detail.username = username
        user_detail.email = email
        user_detail.save()

        return redirect('view-user')
    return render(request, 'edit-user.html', {'user_detail':user_detail, 'user':user})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if len(username) < 3:
            messages.info(request, 'Username is required please.')
            return redirect('login')
        elif len(password) < 3:
            messages.info(request, 'Password is required please.')
            return redirect('login')
        elif user is not None:
            auth.login(request, user)
            if user.is_staff == True:
                return redirect('/')
            else:
                return redirect('user-home')
        else:
            messages.info(request, 'invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def add_category(request):
    user = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        category = request.POST['category']
        date = f"{day}/{month}/{year}"

        if Category.objects.filter(category=category).exists():
            messages.info(request, 'This Category already exist..')
            return redirect('add-category')
        else:
            new_stock = Category.objects.create(
                category=category, date=date
            )
            new_stock.save()
            messages.info(request, 'Category is added successfully..')
            return redirect('view-category')
    return render(request, 'add-category.html', {'user':user})

@login_required(login_url='login')
def view_category(request):
    user = Profile.objects.get(user=request.user)
    category = Category.objects.all()
    return render(request, 'view-category.html', {'user':user, 'category':category})

@login_required(login_url='login')
def request_for_delete(request, id):
    c_user = Profile.objects.get(user=request.user)
    user = User.objects.get(id=id)
    context = {
    'user': user,
    'c_user':c_user,
  }
    return render(request, 'request-for-delete.html', context)

@login_required(login_url='login')
def stock_request_for_delete(request, id):
    c_user = Profile.objects.get(user=request.user)
    stock = Stock.objects.get(id=id)
    context = {
    'c_user':c_user,
    'stock':stock
  }
    return render(request, 'stock-request-for-delete.html', context)

@login_required(login_url='login')
def category_request_for_delete(request, id):
    c_user = Profile.objects.get(user=request.user)
    category = Category.objects.get(id=id)
    context = {
    'c_user':c_user,
    'category':category
  }
    return render(request, 'category-request-for-delete.html', context)

@login_required(login_url='login')
def delete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.info(request, 'User Deleted successfully...')
    return redirect('view-user')

@login_required(login_url='login')
def add_stock(request):
    user = Profile.objects.get(user=request.user)
    category_list = Category.objects.all()
    if request.method == 'POST':
        category = request.POST['category']
        product_name = request.POST['product-name']
        product_qtn = request.POST['product-qtn']
        price = request.POST['price']
        sale_price = price
        date = f"{day}/{month}/{year}"

        if Stock.objects.filter(product_name=product_name).exists():
            messages.info(request, 'This Stock already exist, you can view the Stock and Update it..')
            return redirect('add-stock')
        else:
            new_stock = Stock.objects.create(
                category=category, product_name=product_name, product_qtn=product_qtn,
                price=price, sale_price=sale_price, date=date
            )
            new_stock.save()
            return redirect('view-stock')
    else:
        return render(request, 'add-stock.html', {'user':user, 'category_list':category_list})
    
@login_required(login_url='login')
def view_stock(request):
    user = Profile.objects.get(user=request.user)
    stock = Stock.objects.all()
    context = {
        'user':user,
        'stock':stock
    }
    return render(request, 'view-stock.html', context)

@login_required(login_url='login')
def update_stock(request, id):
    user = Profile.objects.get(user=request.user)
    stock = Stock.objects.get(id=id)

    if request.method == 'POST':
        category = request.POST['category']
        product_name = request.POST['product-name']
        product_qtn = request.POST['product-qtn']
        price = request.POST['price']
        sale_price = price

        stock.category = category
        stock.product_name = product_name
        stock.product_qtn += int(product_qtn)
        stock.price = price
        stock.sale_price = sale_price
        stock.save()

        return redirect('view-stock')
    return render(request, 'update-stock.html', {'stock':stock, 'user':user})

@login_required(login_url='login')
def delete_stock(request, id):
    user = Stock.objects.get(id=id)
    user.delete()
    messages.info(request, 'Stock Deleted successfully...')
    return redirect('view-stock')

@login_required(login_url='login')
def delete_category(request, id):
    user = Category.objects.get(id=id)
    user.delete()
    messages.info(request, 'Category Deleted successfully...')
    return redirect('view-category')

@login_required(login_url='login')
def product_search(request):
    user = Profile.objects.get(user=request.user)
    product_record_list = ''
    if request.method == 'POST':
        name = request.POST['name']
        product = Stock.objects.filter(product_name__icontains=name)

        product_list = []
        product_record_list = []

        for products in product:
            product_list.append(products.id)

        for ids in product_list:
            product_list = Stock.objects.filter(id=ids)
            product_record_list.append(product_list)
        product_record_list = list(chain(*product_record_list))
    return render(request, 'product-search.html', {'product_record_list': product_record_list, 'user':user})

@login_required(login_url='login')
def history_search(request):
    user = Profile.objects.get(user=request.user)
    histories = History.objects.all()
    sum_a = ''
    history_record_list = ''
    if request.method == 'POST':
        name = request.POST['name']
        product = History.objects.filter(
            Q(date__icontains=name) | Q(user__icontains=name)
        )
        sum_a = sum([tran.total_price for tran in product])

        history_list = []
        history_record_list = []

        for products in product:
            history_list.append(products.id)

        for ids in history_list:
            history_list = History.objects.filter(id=ids)
            history_record_list.append(history_list)
        history_record_list = list(chain(*history_record_list))
    return render(request, 'history-search.html', {'history_record_list': history_record_list, 'user':user, 'histories':histories, 'sum_a':sum_a})


@login_required(login_url='login')
def sales_search(request):
    user = Profile.objects.get(user=request.user)
    sales = Sales.objects.all()
    sum_a = ''
    sales_record_list = ''
    if request.method == 'POST':
        name = request.POST['name']
        product = Sales.objects.filter(date__icontains=name)
        sum_a = sum([tran.total_price for tran in product])

        sales_list = []
        sales_record_list = []

        for products in product:
            sales_list.append(products.id)

        for ids in sales_list:
            sales_list = Sales.objects.filter(id=ids)
            sales_record_list.append(sales_list)
        sales_record_list = list(chain(*sales_record_list))
    return render(request, 'sales-search.html', {'sales_record_list': sales_record_list, 'user':user, 'sales':sales, 'sum_a':sum_a})
