from django.urls import path
from cakebox.views import SignupView,SigninView,CategoryCreateView,remove_category,\
CakecreateView,CakelistView,CakeUpdateView,remove_cakeview,CakeVarientCreateView,\
CakeDetailView,CakevarientUpdateView,remove_varient,CakeofferView,remove_offer,signout_view,IndexView


urlpatterns=[
    path("register/",SignupView.as_view(),name="signup"),
    path("",SigninView.as_view(),name="signin"),
    path("categories/add",CategoryCreateView.as_view(),name="add-category"),
    path("categories/<int:pk>/remove",remove_category,name="remove-category"),
    path("cakes/add",CakecreateView.as_view(),name="cake-add"),
    path("cakes/all",CakelistView.as_view(),name="cake-list"),
    path("cakes/<int:pk>/change",CakeUpdateView.as_view(),name="cake-change"),
    path("cakes/<int:pk>/remove",remove_cakeview,name="cake-remove"),
    path("cakes/<int:pk>/varients/add",CakeVarientCreateView.as_view(),name="add-varient"),
    path("cakes/<int:pk>/",CakeDetailView.as_view(),name="cake-detail"),
    path("cakes/<int:pk>/varients/change",CakevarientUpdateView.as_view(),name="update-varient"),
    path("cakes/<int:pk>,varients/remove",remove_varient,name="remove-varient"),
    path("cakes/<int:pk>/varients/offers/add",CakeofferView.as_view(),name="offer-varient"),
    path("offers/<int:pk>/remove",remove_offer,name="remove-offer"),
    path("logout/",signout_view,name="signout"),
    path("index",IndexView.as_view(),name='index'),




]