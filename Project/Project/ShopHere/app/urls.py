from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm

urlpatterns=[
    path('', views.ProductView.as_view(), name='home'),
    path('contact/',views.contact,name='contact'),

    path('product_detail/<int:id>/',views.ProductDetailView.as_view(), name='product_detail'),
    path('customerregistration/',views.CustomerRegistrationView.as_view(),name='customerregistration'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm,next_page='profile'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',
    form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='password_change'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),
    name='password_change_done'),

    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='app/passwordreset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/passwordresetdone.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/passwordresetconfirm.html',
    form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/passwordresetcomplete.html'),name='password_reset_complete'),

    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('address/',views.address,name='address'),
    path('updateAddress/<int:pk>',views.updateAddress.as_view(),name='updateaddress'),
    path('add-to-cart/',views.add_to_cart,name='add_to_cart'),
    path('cart/',views.show_cart,name='show_cart'),

    path('pluscart/',views.plus_cart,name='plus-cart'),
    path('minuscart/',views.minus_cart,name='minus-cart'),
    path('removecart/',views.remove_cart,name='remove-cart'),

    # path('pluswishlist/',views.plus_wishlist),
    # path('minuswishlist/',views.minus_wishlist, name="wishlist"),
    
    path('search/',views.search,name='search'),
    # path('wishlist/',views.show_wishlist,name='showwishlist'),

    path('checkout/',views.checkout,name='checkout'),
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path('orders/',views.orders,name='orders'),
    path('payment/',views.payment, name = 'payment'),
    path('success/',views.success, name = 'success'),



    # path('one_piece/',views.one_piece,name='onepiece'),
 
    # path('one_piece/<slug:data>/',views.one_piece,name='onepiecedata'),
    # path('bags/',views.bags,name='bags'),
    # path('bags/<slug:data>/',views.bags,name='bagsdata'),
    # path('top_wears/',views.top_wears,name='topwears'),
    # path('top_wears/<slug:data>/',views.top_wears,name='topwearsdata'),

    path('buy/',views.buy_now,name='buy_now'),
    
    # path('chatbot/', views.chatbot_view, name='chatbot'),
        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header="Hamro Mart"
admin.site.site_title="Hamro Mart"

