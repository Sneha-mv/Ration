from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .models import ShopOwnerDetails, Product,UserProfile, Booking
from django.http import JsonResponse
from datetime import date
from django.db.models import Sum
from .models import CATEGORY_CHOICES

# For All
def index(request):
    return render(request,"index.html")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role']

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})

        user = CustomUser.objects.create_user(username=username, email=email, password=password, role=role)
        user.save()
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif user.role == 'shop_owner':
                return redirect('shop_details')
            else:
                return redirect('user_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)  
    return redirect('index')


# Admin Section
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def shop_owner_list(request):
    shop_owners = ShopOwnerDetails.objects.all()  
    return render(request, 'shop_owners.html', {'shop_owners': shop_owners})


def user_list(request):
    users = UserProfile.objects.all()  
    return render(request, 'user_list.html', {'users': users})


def product_list(request):
    products = Product.objects.all()  
    return render(request, 'product_list.html', {'products': products})


def order_list(request):
    bookings = Booking.objects.all().select_related('user').prefetch_related('products')
    return render(request, 'order_list.html', {'bookings': bookings})


def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()  
    return redirect('order_list')


def delete_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)  
    user.user.is_active = False
    user.user.save()
    # Optionally, delete the user profile (you can skip this if you want to keep the profile data)
    user.delete()
    return redirect('user_list') 


def approve_owner(request, owner_id):
    owner = ShopOwnerDetails.objects.get(id=owner_id)
    owner.status = 'approved'
    owner.save()
    return redirect('shop_owner_list') 


def reject_owner(request, owner_id):
    owner = ShopOwnerDetails.objects.get(id=owner_id)
    owner.status = 'rejected'
    owner.save()
    return redirect('shop_owner_list')  


# Shop Owner Section
@login_required
def shop_dashboard(request):
    shop_owner_details = ShopOwnerDetails.objects.get(user=request.user)
    products = Product.objects.all()  
    
    return render(request, 'shop_dashboard.html', {
        'user': request.user, 
        'shop_owner_details': shop_owner_details, 
        'products': products })


@login_required
def shop_details(request):
    try:
        owner_details = ShopOwnerDetails.objects.get(user=request.user)
    except ShopOwnerDetails.DoesNotExist:
        owner_details = None  # User hasn't filled details yet

    if request.method == 'POST':
        if owner_details:
            if owner_details.status == 'approved':
                return redirect('shop_dashboard')
            elif owner_details.status == 'rejected':
                return render(request, 'shop_details.html', {
                    'owner_details': owner_details,
                    'message': 'Your details have been rejected. Please contact support for more information.'
                })
            else:
                return render(request, 'shop_details.html', {
                    'owner_details': owner_details,
                    'message': 'Your status is pending. Please wait until your details are approved.'
                })

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        aadhar_image = request.FILES['aadhar_image']
        shop_name = request.POST['shop_name']
        shop_address = request.POST['shop_address']
        shop_license_number = request.POST['shop_license_number']
        license_image = request.FILES['license_image']

        ShopOwnerDetails.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            aadhar_image=aadhar_image,
            shop_name=shop_name,
            shop_address=shop_address,
            shop_license_number=shop_license_number,
            license_image=license_image
        )
        return render(request, 'shop_details.html', {
            'message': 'Your details are submitted and pending approval.'
        })
    return render(request, 'shop_details.html', {'owner_details': owner_details})


def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        quantity = request.POST['quantity']
        price = request.POST['price']
        availability = 'availability' in request.POST
        
        Product.objects.create(
            name=name,
            category=category,
            quantity=quantity,
            price=price,
            availability=availability )
        return redirect('shop_dashboard')
    
    context = {
        'CATEGORY_CHOICES': Product._meta.get_field('category').choices,
    }
    return render(request, 'add_product.html',context)


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':  
        product.name = request.POST.get('name', product.name)
        product.category = request.POST.get('category', product.category)
        product.quantity = request.POST.get('quantity', product.quantity)
        product.price = request.POST.get('price', product.price)
        product.availability = request.POST.get('availability', product.availability)
        product.save()
        
        return redirect('shop_dashboard')  
    return render(request, 'edit_product.html', {'product': product})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST': 
        product.delete()
        return redirect('shop_dashboard')  
    return render(request, 'confirm_delete.html', {'product': product})


def orders_in_shop(request):
    shop_owner = ShopOwnerDetails.objects.get(user=request.user)
    bookings = Booking.objects.filter(ration_shop=shop_owner)
    for booking in bookings:
        booking.total_price = booking.products.aggregate(Sum('price'))['price__sum'] or 0
    return render(request, "orders_in_shop.html", {"bookings": bookings})


# User Section
@login_required
def user_dashboard(request):
    if request.user.role != "user":
        return redirect('index') 

    profile = None
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.email = request.POST.get('email')
        profile.phone_number = request.POST.get('phone_number')
        profile.address = request.POST.get('address')
        profile.save()
        return redirect('user_dashboard')
    profile_filled = all([profile.first_name, profile.last_name, profile.phone_number, profile.address])
    return render(request, 'user_dashboard.html', {'user': request.user, 'profile': profile, 'profile_filled': profile_filled})


@login_required
def booking(request):
    if request.method == "POST":
        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")
        ration_card_number = request.POST.get("ration_card_number")
        ration_card_image = request.FILES.get("ration_card_image")
        product_ids = request.POST.getlist("products")
        shop_id = request.POST.get("ration_shop")

        # Validate the selected shop
        if not shop_id:
            return render(request, "booking_form.html", {
                "error": "Please select a ration shop.",
                "shops": ShopOwnerDetails.objects.all(),
                "products": Product.objects.none()
            })
        
        if not product_ids:
            return render(request, "booking_form.html", {
                "error": "Please select at least one product.",
                "categories": dict(CATEGORY_CHOICES),
                "products": Product.objects.none()
            })
        
        # Retrieve the selected ration shop
        ration_shop = get_object_or_404(ShopOwnerDetails, id=shop_id)
        booking = Booking.objects.create(
            user=request.user,
            address=address,
            ration_card_number=ration_card_number,
            ration_card_image=ration_card_image,
            phone_number=phone_number,
            booking_date=date.today(),
            ration_shop=ration_shop )
        
        booking.products.set(product_ids)
        return redirect("user_dashboard")  
    
    categories = dict(CATEGORY_CHOICES)
    shops = ShopOwnerDetails.objects.all()
    return render(request, "booking_form.html", {
        "categories": categories,
        'shops':shops,
        "products": Product.objects.none()  })


def filter_products_by_category(request):
    category = request.GET.get("category")
    if category:
        products = Product.objects.filter(category=category, availability=True)
        data = [{"id": product.id, "name": product.name, "price": str(product.price)} for product in products]
        return JsonResponse({"products": data})
    return JsonResponse({"products": []})


@login_required
def booking_details(request):
    bookings = Booking.objects.filter(user=request.user).select_related('user').prefetch_related('products')
    return render(request, 'booking_details.html', {'bookings': bookings})


