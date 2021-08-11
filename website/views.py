from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import OrderForm
from .models import Order
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Item
from django.core.paginator import Paginator


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'website/signupuser.html', {'form':UserCreationForm()})
    else:

        if request.POST['password1']==request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'], first_name=request.POST['firstname'], last_name=request.POST['lastname'], email=request.POST['email'])
                user.save()
                login(request, user)
                return redirect('orderpage')
            except IntegrityError:
                return render(request, 'website/signupuser.html', {'form':UserCreationForm(), 'error': 'Username has already been taken. Please choose different username'})

        else:
            return render(request, 'website/signupuser.html', {'form':UserCreationForm(), 'error': 'Passswords did not match'})



@login_required
def orderpage(request):
    orders = Order.objects.filter(user=request.user, datereceived__isnull=True)
    return render(request, 'website/orderpage.html', {'orders': orders})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'website/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'website/loginuser.html', {'form':AuthenticationForm(), 'error': 'Username and Password did not match'})
        else:
            login(request, user)
            return redirect('orderpage')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def home(request):
    items = Item.objects.all()
    paginator = Paginator(items, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'website/home.html',{'page_obj':page_obj})


@login_required
def createorder(request):
    if request.method == 'GET':
        return render(request, 'website/createorder.html', {'form':OrderForm()})
    else:
        try:
            form = OrderForm(request.POST)
            neworder = form.save(commit=False)
            neworder.user = request.user
            neworder.save()
            return redirect('orderpage')
        except ValueError:
            return render(request, 'website/createorder.html', {'form':OrderForm(), 'error': 'Bad data entered. Try again.'})

@login_required
def vieworder(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk, user=request.user)
    if request.method == 'GET':
        form = OrderForm(instance=order)
        return render(request, 'website/vieworder.html', {'order': order, 'form': form})
    else:
        try:
            form = OrderForm(request.POST, instance=order)
            form.save()
            return redirect('orderpage')
        except ValueError:
            return render(request, 'website/vieworder.html', {'order':order, 'form':form, 'error': 'Bad info. Try again.'})

@login_required
def completeorder(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk, user=request.user)
    if request.method == 'POST':
        order.datereceived = timezone.now()
        order.save()
        return redirect('orderpage')

@login_required
def deleteorder(request, order_pk):
    todo = get_object_or_404(Order, pk=order_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('orderpage')

@login_required
def completedorders(request):
    orders = Order.objects.filter(user=request.user, datereceived__isnull=False).order_by('-datereceived')
    return render(request, 'website/completedorders.html', {'orders': orders})
