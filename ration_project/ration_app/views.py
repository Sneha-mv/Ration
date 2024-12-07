from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .models import ShopOwnerDetails, Product,UserProfile

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


# Shop Owner Section
# @login_required
# def shop_dashboard(request):
#     shop_owner_details = ShopOwnerDetails.objects.get(user=request.user)
#     products = Product.objects.all() 
#     return render(request, 'shop_dashboard.html', {'user': request.user, 'shop_owner_details': shop_owner_details, 'products': products,})
@login_required
def shop_dashboard(request):
    shop_owner_details = ShopOwnerDetails.objects.get(user=request.user)
    products = Product.objects.all()  # Get all products, you can filter based on other conditions if needed.
    return render(request, 'shop_dashboard.html', {
        'user': request.user, 
        'shop_owner_details': shop_owner_details, 
        'products': products
    })

@login_required
def shop_details(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        aadhar_image = request.FILES['aadhar_image']
        shop_name = request.POST['shop_name']
        shop_address = request.POST['shop_address']
        shop_license_number = request.POST['shop_license_number']
        license_image = request.FILES['license_image']

        # Save the details
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
        return redirect('shop_dashboard')  
    

    return render(request, 'shop_details.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .models import CATEGORY_CHOICES

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
            availability=availability
        )
        return redirect('shop_dashboard')
     # Pass CATEGORY_CHOICES to the template
    context = {
        'CATEGORY_CHOICES': Product._meta.get_field('category').choices,
    }
    return render(request, 'add_product.html',context)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':  # Update product when the user submits the data
        # Directly update the product fields
        product.name = request.POST.get('name', product.name)
        product.category = request.POST.get('category', product.category)
        product.quantity = request.POST.get('quantity', product.quantity)
        product.price = request.POST.get('price', product.price)
        product.availability = request.POST.get('availability', product.availability)
        product.save()
        
        return redirect('shop_dashboard')  # Redirect to the product list page after update
    
    return render(request, 'edit_product.html', {'product': product})

from django.shortcuts import get_object_or_404, redirect
from .models import Product

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':  # Confirm deletion via POST
        product.delete()
        return redirect('shop_dashboard')  # Redirect to the product list page after deletion
    
    return render(request, 'confirm_delete.html', {'product': product})






# User Section
from django.shortcuts import redirect
@login_required
def user_dashboard(request):
    # Check if the user is a regular user, if not, redirect them
    if request.user.role != "user":
        return redirect('some_other_page')  # Redirect to another page (like shop owner's dashboard)

    # Initialize profile variable
    profile = None
    # Get or create the profile for the user
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Handle form submission for profile update
    if request.method == "POST":
        # Update profile for user
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.email = request.POST.get('email')
        profile.phone_number = request.POST.get('phone_number')
        profile.address = request.POST.get('address')
        profile.save()

        # Redirect after saving the profile
        return redirect('user_dashboard')
      # Check if the profile is filled (i.e., if any required fields are missing)
    profile_filled = all([profile.first_name, profile.last_name, profile.phone_number, profile.address])

    # Render the user dashboard with the profile
    return render(request, 'user_dashboard.html', {'user': request.user, 'profile': profile, 'profile_filled': profile_filled})


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Product, Booking
from django.contrib.auth.decorators import login_required
from datetime import date

@login_required
def booking(request):
    if request.method == "POST":
        # Process the booking form
        address = request.POST.get("address")
        phone_number = request.POST.get("phone_number")
        ration_card_number = request.POST.get("ration_card_number")
        ration_card_image = request.FILES.get("ration_card_image")
        product_ids = request.POST.getlist("products")
        
        if not product_ids:
            return render(request, "booking_form.html", {
                "error": "Please select at least one product.",
                "categories": dict(CATEGORY_CHOICES),
                "products": Product.objects.none()
            })
        
        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            address=address,
            ration_card_number=ration_card_number,
            ration_card_image=ration_card_image,
            phone_number=phone_number,
            booking_date=date.today()
        )
        booking.products.set(product_ids)
        return redirect("user_dashboard")  # Replace 'success_page' with the name of your success URL
    
    # For GET request, show the form
    categories = dict(CATEGORY_CHOICES)
    return render(request, "booking_form.html", {
        "categories": categories,
        "products": Product.objects.none()  # Initially no products
    })


def filter_products_by_category(request):
    category = request.GET.get("category")
    if category:
        products = Product.objects.filter(category=category, availability=True)
        data = [{"id": product.id, "name": product.name, "price": str(product.price)} for product in products]
        return JsonResponse({"products": data})
    return JsonResponse({"products": []})


def booking_details(request):
    # Fetch all bookings with related product details
    bookings = Booking.objects.select_related('user').prefetch_related('products').all()
    return render(request, 'booking_details.html', {'bookings': bookings})
