from .models import MenuItem,Category,Cart,Order,OrderItem
from .serializers import MenuItemSerializer,CategorySeralizer,UserSerializer,CartSerializer,OrderSerializer,OrderItemSerializer,OrderManagerUpdateSerializer,OrderCustomerUpdateSerializer
from django.http import JsonResponse,HttpResponse
from django.http import QueryDict
from django.shortcuts import render,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.db import IntegrityError
from django.contrib.auth.models import User,Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions,viewsets
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status,generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.viewsets import GenericViewSet,ModelViewSet

# Create your views here.
class MenuItemsView(generics.ListCreateAPIView,generics.DestroyAPIView):
    permission_classes = [permissions.DjangoModelPermissions]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get(self,request):
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price=to_price)
        if search:
            items = items.filter(title__contains=search)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
        
        serialized_item = MenuItemSerializer(items,many=True)
        return Response(serialized_item.data)
    
    def get_permissions(self):
        permission_classes = [permissions.DjangoModelPermissions]
        if self.request.method != 'GET':
            permission_classes = [permissions.DjangoModelPermissions]
        return [permission() for permission in permission_classes]
    
class SingleMenuItemsView(generics.RetrieveUpdateAPIView,generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def get_permissions(self):
        permission_classes = [permissions.DjangoModelPermissions]
        if self.request.method != 'GET':
            permission_classes = [permissions.DjangoModelPermissions]
        return [permission() for permission in permission_classes]
    
class CategoryView(generics.ListCreateAPIView,generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySeralizer
    
class SingleCategoryView(generics.RetrieveAPIView,generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySeralizer
    
class ManagerManagerView(generics.ListCreateAPIView):
    queryset = User.objects.all() 
    serializer_class = UserSerializer
    
    def get(self,request): 
        users = User.objects.filter(groups__name='Manager')
        serializer = UserSerializer(users, many=True)
        return Response({'data': serializer.data})
        
    def post(self,request):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name='Manager')
            managers.user_set.add(user)
            users = User.objects.filter(groups__name='Manager')
            serializer = UserSerializer(users, many=True)
            return Response({'data': serializer.data})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
class ManagerSingleManagerView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    
    def get(self,request,pk):
        user = User.objects.get(id=pk)
        if user.groups.filter(name='Manager'):
            instance = User.objects.get(id=pk)
            serializer_class = UserSerializer(instance)
            return Response(serializer_class.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,pk):
        username = User.objects.get(pk=pk)
        if username and username.groups.filter(name="Manager"):
            user = get_object_or_404(User,username=username)
            manager = Group.objects.get(name='Manager')
            manager.user_set.remove(user)
            users = User.objects.filter(groups__name='Manager')
            serializer = UserSerializer(users, many=True)
            return Response({'data': serializer.data})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
                 
class ManagerDeliveryCrewView(generics.ListCreateAPIView):
    queryset = User.objects.all() 
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    
    def get(self,request):
        users = User.objects.filter(groups__name='Delivery-Crew')
        serializer = UserSerializer(users, many=True)
        return Response({'data': serializer.data})
        
        
    def post(self,request):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name='Delivery-Crew')
            managers.user_set.add(user)
            users = User.objects.filter(groups__name='Delivery-Crew')
            serializer = UserSerializer(users, many=True)
            return Response({'data': serializer.data})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
          
class ManagerSingleDeliveryCrewView(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    
    def get(self,request,pk):
        user = User.objects.get(id=pk)
        if user.groups.filter(name='Delivery-Crew'):
            instance = User.objects.get(id=pk)
            serializer_class = UserSerializer(instance)
            return Response(serializer_class.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,pk):
        username = User.objects.get(pk=pk)
        if username and username.groups.filter(name="Delivery-Crew"):
            user = get_object_or_404(User,username=username)
            manager = Group.objects.get(name='Delivery-Crew')
            manager.user_set.remove(user)
            users = User.objects.filter(groups__name='Delivery-Crew')
            serializer = UserSerializer(users, many=True)
            return Response({'data': serializer.data})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
class CartView(generics.ListCreateAPIView):
    permission_classes = ([IsAuthenticated])
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    def get(self, request, format=None):
        if request.user.groups.filter(name='Manager').exists() or request.user.groups.filter(name='Delivery-Crew').exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = Cart.objects.filter(user=request.user.pk)
            serializer = CartSerializer(queryset,many=True)
            return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists() or request.user.groups.filter(name='Delivery-Crew').exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return self.create(request, *args, **kwargs)
    
    def delete(self,request):
        if request.user.groups.filter(name='Manager').exists() or request.user.groups.filter(name='Delivery-Crew').exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = Cart.objects.filter(user=request.user.pk)
            serializer = CartSerializer(queryset,many=True)
            queryset.delete()
            return Response(serializer.data)
        
class OrderView(generics.ListCreateAPIView,generics.DestroyAPIView):
    permission_classes = ([IsAuthenticated])
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get(self,request):
        if request.user.groups.filter(name='Manager').exists():
            queryset = Order.objects.all()
            serializer = OrderSerializer(queryset,many=True)
            return Response(serializer.data)
        elif request.user.groups.filter(name='Delivery-Crew').exists():
            queryset = Order.objects.filter(delivery_crew=request.user.pk)
            serializer = OrderSerializer(queryset,many=True)
            return Response(serializer.data)
        else:
            queryset = Order.objects.filter(user=request.user.pk)
            serializer = OrderSerializer(queryset,many=True)
            return Response(serializer.data)
    
    def post(self,request,*args, **kwargs):
        if request.user.groups.filter(name='Manager').exists() or request.user.groups.filter(name='Delivery-Crew').exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            cart_queryset = Cart.objects.all()
            if cart_queryset.exists():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                order_id = serializer.instance.id
                queryset = Cart.objects.filter(user=request.user.pk)
                order = Order.objects.get(id=order_id)
                for item in queryset:
                    OrderItem.objects.create(order=order,
                                            menuitem=item.menuitem,
                                            quantity=item.quantity,
                                            unit_price=item.unit_price,
                                            price=item.price)
                returndata = OrderItem.objects.filter(order=order_id)
                order_item_serializer = OrderItemSerializer(returndata,many=True)
                child_viewset = CartView()
                child_viewset.delete(request, *args, **kwargs)
                calculate_total = 0
                for item in returndata:
                    calculate_total += item.price
                order.total = calculate_total
                order.save()
                return Response(order_item_serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
                     
class OrderUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = ([IsAuthenticated])
    queryset = Order.objects.all()
    serializer_class = OrderCustomerUpdateSerializer
    
    def delete(self,request,pk):
            queryset = Order.objects.get(id=pk)
            queryset.delete()
            viewset = Order.objects.all()
            serializer = OrderSerializer(viewset,many=True)
            return Response(serializer.data)
        
    def put(self, request,pk, *args, **kwargs):
        if self.request.user.groups.filter(name='Manager').exists():
            instance = Order.objects.get(id=pk)
            crew = request.data['username']
            order_status = request.data['status']
            instance.status = order_status
            dcrew=User.objects.get(username=crew)
            instance.delivery_crew = dcrew
            instance.save()
            serializer_class = OrderManagerUpdateSerializer(instance)
            return Response(serializer_class.data)
        elif self.request.user.groups.filter(name='Delivery-Crew').exists():
            instance = Order.objects.get(id=pk)
            order_status = request.data['status']
            instance.status = order_status
            instance.save()
            return Response(status=status.HTTP_200_OK)
        elif Order.objects.get(id=pk).user == self.request.user:
            queryset = Order.objects.get(id=pk)
            serializer_class = OrderCustomerUpdateSerializer(queryset)
            return super().put(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    
    def get(self,request,pk,*args,**kwargs):
        if self.request.user.groups.filter(name='Manager').exists():
            queryset = Order.objects.get(id=pk)
            serializer_class = OrderManagerUpdateSerializer(queryset)
            return Response(serializer_class.data)
        elif Order.objects.get(id=pk).user == self.request.user:
            queryset = Order.objects.get(id=pk)
            serializer_class = OrderCustomerUpdateSerializer(queryset)
            return Response(serializer_class.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
    
    def delete(self,request,*args,**kwargs):
        if self.request.user.groups.filter(name='Manager').exists():
            return self.destroy(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    