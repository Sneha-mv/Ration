from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .models import ShopOwnerDetails, Product,UserProfile, Booking, RationCardApplications, IDProofs
from django.http import JsonResponse
from datetime import date
from django.db.models import Sum
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import razorpay
from .models import CATEGORY_CHOICES

# For All
def index(request):
    return render(request,"index.html")


def about(request):
    return render(request,"about_us.html")


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


def contact(request):
    return render(request,'contact.html')


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


@login_required
def payment_list(request):
    payments = Booking.objects.select_related('user').values(
        'user__username', 
        'payment_status' )
    return render(request, "admin_payments.html", {"payments": payments})


def view_ration_cards(request):
    applications = RationCardApplications.objects.all()
    return render(request, 'view_ration_cards.html', {'applications': applications})


def manage_ration_card(request, id):
    application = get_object_or_404(RationCardApplications, id=id)
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'approve':
            application.status = 'Approved'  
        elif action == 'reject':
            application.status = 'Rejected'
        application.save()
        return redirect('view_ration_cards')
    return render(request, 'manage_ration_card.html', {'application': application})


def delete_ration_card(request, id):
    application = get_object_or_404(RationCardApplications, id=id)
    application.delete()
    return redirect('view_ration_cards')


# Shop Owner Section
@login_required
def shop_dashboard(request):
    shop_owner_details = ShopOwnerDetails.objects.get(user=request.user)
    products = Product.objects.filter(shop_owner=shop_owner_details)  
    
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


@login_required
def add_product(request):
    try:
        shop_owner = ShopOwnerDetails.objects.get(user=request.user)
    except ShopOwnerDetails.DoesNotExist:
        return redirect('index')  
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        availability = request.POST.get('availability') == 'on' 

        product = Product(
            shop_owner=shop_owner,
            name=name,
            category=category,
            quantity=quantity,
            price=price,
            availability=availability
        )
        product.save()
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

        if not shop_id:
            return render(request, "booking_form.html", {
                "error": "Please select a ration shop.",
                "shops": ShopOwnerDetails.objects.filter(status="approved"), 
                "products": Product.objects.none()
            })
        
        if not product_ids:
            return render(request, "booking_form.html", {
                "error": "Please select at least one product.",
                "categories": dict(CATEGORY_CHOICES),
                "products": Product.objects.none()
            })

        current_month = now().month
        current_year = now().year

        previous_bookings = Booking.objects.filter(
            user=request.user,
            booking_date__month=current_month,
            booking_date__year=current_year,
            products__id__in=product_ids
        ).distinct()

        if previous_bookings.exists():
            return render(request, "booking_form.html", {
                "error": "You have already booked some of these products this month. Please try again next month.",
                "categories": dict(CATEGORY_CHOICES),
                "shops": ShopOwnerDetails.objects.filter(status="approved"),
                "products": Product.objects.filter(shop_owner_id=shop_id, availability=True),
            })
        
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
    shops = ShopOwnerDetails.objects.filter(status="approved")
    return render(request, "booking_form.html", {
        "categories": categories,
        'shops':shops,
        "products": Product.objects.none()
    })


def filter_products_by_category(request):
    category = request.GET.get("category")
    shop_id = request.GET.get("shop_id")  
    if category and shop_id:
        products = Product.objects.filter(category=category, availability=True, shop_owner_id=shop_id)
        data = [{"id": product.id, "name": product.name, "price": str(product.price)} for product in products]
        return JsonResponse({"products": data})
    return JsonResponse({"products": []})


@login_required
def booking_details(request):
    bookings = Booking.objects.filter(user=request.user).select_related('user').prefetch_related('products')
    return render(request, 'booking_details.html', {'bookings': bookings})


@login_required
def payment_details(request):
    bookings = Booking.objects.filter(user=request.user, payment_status=False).select_related('user').prefetch_related('products')
    
    if not bookings.exists():
        return render(request, "payment_details.html", {"message": "You don't have any orders or bookings to proceed payment."})
    total_amount = sum(
        (booking.products.aggregate(Sum('price'))['price__sum'] or 0) + 100  # Add service charge of 100
        for booking in bookings
    )
    amount_in_paise = int(total_amount * 100)

    # Create Razorpay order with the calculated amount
    client = razorpay.Client(auth=("rzp_test_JAeLcxoJpwFjEq", "PvjOeaEQA5b2gH4XHxEGEhMB"))
    payment = client.order.create({
        'amount': amount_in_paise, 
        'currency': 'INR',
        'payment_capture': '1'
    })

    if request.method == 'POST':
        bookings.update(payment_status=True)
        return redirect('payment_success')
    
    return render(request, "payment_details.html", {
        "bookings": bookings,
        "payment": payment,
        "total_amount": total_amount })


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        booking = get_object_or_404(Booking, id=booking_id)
        booking.payment_status = True
        booking.save()
        return render(request, "payment_success.html", {"message": "Payment completed successfully!"})
    return redirect("user_dashboard")


def apply_ration_card(request):
    if request.method == "POST":
        master_of_the_house = request.POST.get("master_of_the_house")
        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")
        punchayath_or_corporation = request.POST.get("punchayath_or_corporation")
        ward_number = request.POST.get("ward_number")
        house_number = request.POST.get("house_number")
        monthly_income = request.POST.get("monthly_income")
        total_family_members = request.POST.get("total_family_members")
        family_details = request.POST.get("family_details")
        date = request.POST.get("date")

        application = RationCardApplications.objects.create(
            master_of_the_house=master_of_the_house,
            address=address,
            phone_number=phone_number,
            punchayath_or_corporation=punchayath_or_corporation,
            ward_number=ward_number,
            house_number=house_number,
            monthly_income=monthly_income,
            total_family_members=total_family_members,
            family_details=family_details,
            date=date,
        )

        for file in request.FILES.getlist("id_proofs"):
            IDProofs.objects.create(application=application, file=file)
        return render(request, "success_message_rationcard.html")
    return render(request, "apply_ration_card.html")


