from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.decorators import action
from rest_framework import authentication
from rest_framework import permissions


from api.serializers import UserSerializer,CakesSerializer,CartSerializer,OrderSerializer,ReviewSerializer

from cakebox.models import Cakes,CakeVarients,Carts,Orders

# Create your views here.





class UserCreationView(APIView):

    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class CakesView(ModelViewSet):
    
    serializer_class=CakesSerializer
    model=Cakes
    queryset=Cakes.objects.all()
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    # custom method

    # http://127.0.0.1:8000/api/cakes/{varient_id}/cart_add/


    @action(methods=["post"],detail=True)
    def cart_add(self,request,*args,**kwargs):
        vid=kwargs.get("pk")
        varient_obj=CakeVarients.objects.get(id=vid)
        user=request.user
        serializer=CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cakevarient=varient_obj,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    #url:http://127.0.0.1:8000/api/cakes/{varient_id}/place_order/    

    @action(methods=["post"],detail=True)
    def place_order(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        varient_object=CakeVarients.objects.get(id=id)
        user=request.user

        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cakevarient=varient_object,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    @action(methods=["post"],detail=True)
    def add_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        cake_obj=Cakes.objects.get(id=id)
        user=request.user

        serializer=ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cake=cake_obj,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)



class OrdersView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    # authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]
    def list(self,request,*args,**kwargs):
        qs=Orders.objects.filter(user=request.user)
        serializer=OrderSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        instance=Orders.objects.get(id=id)
        if instance.user==request.user:
            instance.delete()
            return Response(data={"msg":"deleted"})
        else:
            return Response(data={"message":"permission denied"})


        
    



# create new view for add to cart

# post,create => id


class CartsView(ViewSet):

    authentication_classes=[authentication.TokenAuthentication]
    # authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]
    serializer_class=CartSerializer

    def list(self,request,*args,**kwargs):
        qs=Carts.objects.filter(user=request.user)
        serializer=CartSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")

        Carts.objects.get(id=id).delete()
        return Response(data={"message":"delete"})

