from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced,Contact
# from .models import Customer,Product,Cart,OrderPlaced,Wishlist,Contact

from .forms import CustomerRegistrationForm, CustomerProfileForm,ContactForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

class ProductView(View):
    def get(self, request):
        totalitem=0 
        # wishitem=0
        electronics=Product.objects.filter(category='E')
        clothing=Product.objects.filter(category='C')
        grocery=Product.objects.filter(category='G')
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            # wishitem=len(Wishlist.objects.filter(user=request.user))
        # return render(request,'app/home.html', {'one_piece':one_piece,'top_wears':top_wears,'bags':bags,'totalitem':totalitem,'wishitem':wishitem})
        return render(request,'app/home.html', {'electronics':electronics,'clothing':clothing,'grocery':grocery,'totalitem':totalitem})


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})

@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add, 'active':'btn-primary'})

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request,'app/updateaddress.html',locals())
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")

@login_required
def add_to_cart(request):
    user=request.user 
    product_id=request.GET.get('prod_id')
    print("this is prod id", product_id)
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    totalitem=0
    # wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        # wishitem=len(Wishlist.objects.filter(user=request.user))
        user=request.user
        cart=Cart.objects.filter(user=user) 
        amount=0.0
        shipping_amount=70.0
        totalamount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        
        if cart_product:
            for p in cart_product:
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
                totalamount=amount+shipping_amount

            # return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem,'wishitem':wishitem})
            return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})

        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1 
        c.save()

        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data) 

def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()

        amount=0.0
        shipping_amount=70.0
        
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()

        amount=0.0
        shipping_amount=70.0

        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount

        data={
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data) 

# def plus_wishlist(request):
#     if request.method=='GET':
#         prod_id=request.GET['prod_id']
#         product=Product.objects.get(id=prod_id)
#         user=request.user
#         Wishlist(user=user,product=product).save()
#         data={
#             'message':'Wishlist Added Successfully!!',
#             'url': ""
#         }
#         return JsonResponse(data)
    
# def minus_wishlist(request):
#     if request.method=='GET':
#         prod_id=request.GET['prod_id']
#         product=Product.objects.get(id=prod_id)
#         user=request.user
#         Wishlist.objects.filter(user=user,product=product).delete()
#         data={
#             'message':'Wishlist Removed Successfully!!',
#             'url': ""
#         }
#         return JsonResponse(data)

# @login_required
# def show_wishlist(request):
#     user=request.user
#     totalitem=0
#     wishitem=0
#     if request.user.is_authenticated:
#         totalitem=len(Cart.objects.filter(user=request.user))
#         wishitem=len(Wishlist.objects.filter(user=request.user))
#     product=Wishlist.objects.filter(user=user)
#     return render(request, 'app/wishlist.html',{'totalitem':totalitem,'wishitem':wishitem,'product':product})

def search(request):
    query=request.GET['search']
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        # wishitem=len(Wishlist.objects.filter(user=request.user))
    product=Product.objects.filter(Q(title__icontains=query))
    # return render(request,'app/search.html',{'totalitem':totalitem,'wishitem':wishitem,'product':product})
    return render(request,'app/search.html',{'totalitem':totalitem,'product':product})


# @login_required
# def checkout(request):
#     user=request.user
#     add=Customer.objects.filter(user=user)
#     cart_items=Cart.objects.filter(user=user)

#     amount=0.0
#     shipping_amount=70.0
#     totalamount=0.0

#     cart_product=[p for p in Cart.objects.all() if p.user==user]
#     if cart_product:
#         for p in cart_product:
#             tempamount=(p.quantity*p.product.discounted_price)
#             amount+=tempamount
#             totalamount=tempamount+shipping_amount
#     return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

@login_required
def payment_done(request):
    user=request.user
    print("this is user",user)
    # custid=request.GET.get('custid')
    # custid = request.session.get('custid')
    # print("This is cust id",custid)
    customer=Customer.objects.get(id=13)
  
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
        # return redirect("orders")
        return render(request, 'app/success.html')


@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

def about(request):
    return render(request, 'app/about.html')

class ProductDetailView(View):
    def get(self, request, id):
        totalitem=0
        # wishitem=0
        product=Product.objects.get(id=id)
        # wishlist=Wishlist.objects.filter(Q(product=product)&Q(user=request.user.id))

        item_already_in_cart=False 
  
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            # wishitem=len(Wishlist.objects.filter(user=request.user))
            item_already_in_cart=Cart.objects.filter(Q(product=product.id)&Q(user=request.user)).exists()
        # return render(request, 'app/productdetail.html', {'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem,'wishlist':wishlist,'wishitem':wishitem})
        return render(request, 'app/productdetail.html', {'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})


# def one_piece(request, data=None):
#     if data==None:
#         onepiece=Product.objects.filter(category='OP')
#     elif data=='kee' or data=='Aajio':
#         onepiece=Product.objects.filter(category='OP').filter(brand=data)
#     elif data=='below':
#         onepiece=Product.objects.filter(category='OP').filter(discounted_price__lt=1000)
#     elif data=='above':
#         onepiece=Product.objects.filter(category='OP').filter(discounted_price__gt=1000)
#     return render(request, 'app/one_piece.html',{'onepiece':onepiece})

# def bags(request, data=None):
#     if data==None:
#         bags=Product.objects.filter(category='B')
#     elif data=='TWEE' or data=='WEE':
#         bags=Product.objects.filter(category='B').filter(brand=data)
#     elif data=='below':
#         bags=Product.objects.filter(category='B').filter(discounted_price__lt=700)
#     elif data=='above':
#         bags=Product.objects.filter(category='B').filter(discounted_price__gt=700)
#     return render(request, 'app/bags.html',{'bags':bags})
    
# def top_wears(request, data=None):
#     if data==None:
#         topwears=Product.objects.filter(category='TP')
#     elif data=='Nike' or data=='Lee':
#         topwears=Product.objects.filter(category='TP').filter(brand=data)
#     elif data=='below':
#         topwears=Product.objects.filter(category='TP').filter(discounted_price__lt=800)
#     elif data=='above':
#         topwears=Product.objects.filter(category='TP').filter(discounted_price__gt=800)
#     return render(request, 'app/top_wears.html',{'topwears':topwears})

@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})

    def post(self, request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully')
            form.save()
            return render(request, 'app/customerregistration.html',{'form':form})

        else:
            return render(request, 'app/customerregistration.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid(): 
            form.save()
            subject = "Welcome to ShopHere"
            message = "Our team will contact you within 24hrs."
            email_from = settings.EMAIL_HOST_USER
            email = form.cleaned_data['email']
            recipient_list =email
            send_mail(subject, message, email_from, [recipient_list])
            return render(request, 'app/success.html') 
    form = ContactForm()
    context = {'form': form}
    return render(request, 'app/contact.html', context)

# def chatbot_view(request):
#     return render(request, 'app/chatbot.html')


# @login_required
# def payment(request):
#     return render(request, 'app/try.html')



def calculate_checkout_data(user):
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)

    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0

    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount += tempamount + shipping_amount

    return {'add': add, 'totalamount': totalamount, 'cart_items': cart_items}

@login_required
def checkout(request):
    user = request.user
    checkout_data = calculate_checkout_data(user)
    return render(request, 'app/checkout.html', checkout_data)

@login_required
def payment(request):
    user = request.user
    checkout_data = calculate_checkout_data(user)
    total_amount = checkout_data['totalamount']
    return render(request, 'app/try.html', {'total_amount' : total_amount})


@login_required
def success(request):
    return render(request, 'app/success.html')