from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from . models import*
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from .forms import*
from django.contrib import messages
from django.urls import reverse
from .models import Notification
from django.conf import settings
from django.core.mail import send_mail




# Create your views here.
from django.http import HttpResponse
def home(request):
    print("User authenticated?", request.user.is_authenticated)
    return render(request, 'home.html') 

def register_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 

    context = {'form': form}
    return render(request, 'register.html', context) 

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')  # وجهه إلى لوحة الإدارة
            else:
                return redirect('service_list')
        else:
            print('Invalid credentials')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)  # Log out the user
    return redirect('home')  # Redirect to the login page after logout
def service_list(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})
def service_detail(request, pk):
    service = Service.objects.get(id=pk)
    return render(request, 'service_detail.html', {'service': service})
from django.contrib.auth.decorators import login_required
from .forms import OrderForm

@login_required
def create_order(request, service_id):
    service = Service.objects.get(id=service_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.service = service
            order.save()
            return redirect('my_orders')  # صفحة الطلبات الخاصة بالمستخدم
    else:
        form = OrderForm()

    return render(request, 'create_order.html', {'form': form, 'service': service})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'my_orders.html', {'orders': orders})

@login_required
def update_order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('my_orders')  # بعد التعديل، العودة لصفحة الطلبات
    else:
        form = OrderForm(instance=order)

    return render(request, 'update_order.html', {'form': form, 'order': order})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'تم حذف الطلب بنجاح.')
        return redirect('my_orders')
    return render(request, 'remove_order.html', {'order': order})


@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    orders = Order.objects.all().order_by('-date_created')

    username = request.GET.get('username')
    status = request.GET.get('status')

    if username:
        orders = orders.filter(user__username__icontains=username)

    if status in dict(Order.STATUS_CHOICES):  # تأكد أن الحالة صحيحة
        orders = orders.filter(status=status)

    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'current_username': username,
        'current_status': status,
    }
    return render(request, 'admin-dashboard.html', context)


def admin_update_order(request, order_id):
    if not request.user.is_superuser:
        return HttpResponse("غير مصرح لك بالدخول")

    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = AdminOrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f"تم تحديث حالة الطلب رقم {order.id} إلى {order.get_status_display()}")

            # إنشاء إشعار للمستخدم داخل التطبيق
            Notification.objects.create(
                user=order.user,
                message=f"تم تحديث حالة طلبك إلى: {order.status}"
            )

            # إرسال إشعار عبر البريد الإلكتروني
            # send_mail(
            #     'تحديث حالة طلبك',
            #     f"تم تحديث حالة طلبك رقم {order.id} إلى: {order.get_status_display()}",
            #     settings.EMAIL_HOST_USER,
            #     [order.user.email],  # إرسال البريد للمستخدم
            #     fail_silently=False,
            # )

            return redirect('admin_dashboard')
    else:
        form = AdminOrderStatusForm(instance=order)

    return render(request, 'admin_update_order_status.html', {'form': form, 'order': order})


def add_rating(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.order = order
            rating.user = request.user
            rating.save()
            messages.success(request, "تم تقييم الطلب بنجاح.")
            return redirect('orders_to_user')
    else:
        form = RatingForm()

    return render(request, 'add_rating.html', {'form': form, 'order': order})

def check_rating_permission(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # messages.info(request, "🚀 دخلنا على view check_rating_permission")
    if order.status != 'completed':
        messages.error(request, "لا يمكنك تقييم هذا الطلب لأنه غير مكتمل.")
        return redirect('orders_to_user')

    existing_rating = Rating.objects.filter(order=order, user=request.user).exists()
    if existing_rating:
        messages.info(request, "لقد قمت بتقييم هذا الطلب بالفعل.")
        
        return redirect('orders_to_user')

    # كل شيء تمام → توجّه المستخدم لصفحة التقييم
    return redirect(reverse('add_rating', args=[order_id]))


def orders_to_user(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'my_orders.html', {'orders': orders})

def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_notifications.html', {'notifications': notifications}) 

def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    if request.method == 'POST':
        notification.is_read = True
        notification.save()
    return redirect('user_notifications')

def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    if request.method == 'POST':
        notification.delete()
    return redirect('user_notifications')




  











    
