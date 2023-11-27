from django.shortcuts import render,redirect
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.db import models
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.views.generic import View,CreateView,FormView,ListView,UpdateView,DetailView,TemplateView

from cakebox.models import User,Category,Cakes,CakeVarients,Offers
from cakebox.forms import RegistrationForm,LoginForm,CategoryCreateForm,CakeAddForm,\
    CakeVarientForm,CakeOfferForm

# Create your views here.

def signin_required(fn):

    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session...")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

def is_admin(fn):

    def wrapper(request,*args,**kwargs):
        if not request.user.is_superuser:
            messages.error(request,"permision denied for current user...")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
        
    return wrapper

decs=[signin_required,is_admin]

class IndexView(TemplateView):
    template_name="cakebox/index.html"


class SignupView(CreateView):
    template_name="cakebox/reg.html"
    model=User
    form_class=RegistrationForm
    success_url=reverse_lazy("signin")

    def form_valid(self,form):
        messages.success(self.request,"account created")
        return super().form_valid(form)
    def form_invalid(self,form):
        messages.error(self.request,"failed to create account")
        return super().form_invalid(form)
    

class SigninView(FormView):
    template_name="cakebox/login.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)

        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login successfully...")
                return redirect("index")
            else:
                messages.error(request,"login failed...try again..")
                return render(request,self.template_name,{"form":form})


@method_decorator(decs,name="dispatch")
class CategoryCreateView(CreateView,ListView):
    template_name="cakebox/cat_add.html"
    form_class=CategoryCreateForm
    model=Category
    context_object_name="categories"
    success_url=reverse_lazy("add-category")

    def form_valid(self, form):
        messages.success(self.request,"category added...")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"category adding failed...")
        return super().form_invalid(form)
    
    def get_queryset(self):
        return Category.objects.filter(is_available=True)
    
@signin_required
@is_admin
def remove_category(request,*args,**kwargs):
    id=kwargs.get("pk")
    Category.objects.filter(id=id).update(is_available=False)
    messages.success(request,"category removed...")
    return redirect("add-category")


@method_decorator(decs,name="dispatch")
class CakecreateView(CreateView):
    template_name="cakebox/cake_add.html"
    model=Cakes
    form_class=CakeAddForm
    success_url=reverse_lazy("cake-list")

    def form_valid(self, form):
        messages.success(self.request,"cake has been added...")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"cake adding failed...")
        return super().form_invalid(form)
    

@method_decorator(decs,name="dispatch")
class CakelistView(ListView):
    template_name="cakebox/cake_list.html"
    model=Cakes
    context_object_name="cakes"


@method_decorator(decs,name="dispatch")
class CakeUpdateView(UpdateView):
    template_name="cakebox/cake_edit.html"
    model=Cakes
    form_class=CakeAddForm
    success_url=reverse_lazy("cake-list")

    def form_valid(self, form):
        messages.success(self.request,"cake updated...")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"cake updating failed...")
        return super().form_invalid(form)
    
@signin_required
@is_admin
def remove_cakeview(request,*args,**kwargs):
    id=kwargs.get("pk")
    Cakes.objects.filter(id=id).delete()
    messages.success(request,"item removed...")
    return redirect("cake-list")


@method_decorator(decs,name="dispatch")
class CakeVarientCreateView(CreateView):
    template_name="cakebox/cakevar_add.html"
    model=CakeVarients
    form_class=CakeVarientForm
    success_url=reverse_lazy("cake-list")

    def form_valid(self, form):
        id=self.kwargs.get("pk")
        obj=Cakes.objects.get(id=id)
        form.instance.cake=obj
        messages.success(self.request,"varient has been added...")
        return super().form_valid(form)
    

@method_decorator(decs,name="dispatch")
class CakeDetailView(DetailView):
    template_name="cakebox/cake_detail.html"
    model=Cakes
    context_object_name="cake"


@method_decorator(decs,name="dispatch")
class CakevarientUpdateView(UpdateView):
    template_name="cakebox/cakevar_edit.html"
    model=CakeVarients
    form_class=CakeVarientForm

    def form_valid(self, form):
        messages.success(self.request,"cake varient updated...")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"cake varient updating failed...")
        return super().form_invalid(form)
    
    def get_success_url(self):
        id=self.kwargs.get("pk")
        cake_varient_object=CakeVarients.objects.get(id=id)
        cake_id=cake_varient_object.Cake.id

        return reverse("cake-detail",kwargs={"pk":cake_id})
    

@signin_required
@is_admin
def remove_varient(request,*args,**kwargs):
    id=kwargs.get("pk")
    CakeVarients.objects.filter(id=id).delete()
    messages.success(request,"item removed...")
    return redirect("cake-list")


@method_decorator(decs,name="dispatch")
class CakeofferView(CreateView):
    template_name="cakebox/ck_offer.html"
    model=Offers
    form_class=CakeOfferForm
    success_url=reverse_lazy("cake-list")

    def form_valid(self, form):
        id=self.kwargs.get("pk")
        obj=CakeVarients.objects.get(id=id)
        form.instance.cakevarient=obj

        messages.success(self.request,"offer has been added...")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request," offer close...")
        return super().form_invalid(form)
    
    def get_success_url(self):
        id=self.kwargs.get("pk")
        cake_varient_object= CakeVarients.objects.get(id=id)
        cake_id=cake_varient_object.cake.id

        return reverse("cake-detail",kwargs={"pk":cake_id})


@signin_required
@is_admin
def remove_offer(request,*args,**kwargs):
    id=kwargs.get("pk")
    offer_obj=Offers.objects.get(id=id)
    cake_id=offer_obj.cakevarient.cake.id
    offer_obj.delete()
    return redirect("cake-detail",pk=cake_id)

@signin_required
def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")



