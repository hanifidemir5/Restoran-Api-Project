from rest_framework import serializers
from .models import Category,MenuItem,Cart,Order,OrderItem
from django.contrib.auth.models import Group,User

class CategorySeralizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']
    
class MenuItemSerializer(serializers.ModelSerializer):
    queryset = Category.objects.all()
    category_list = []
    for item in queryset:
        category_list.append(item.title)
        
    category = serializers.ChoiceField(choices=category_list)
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category']
        
    def get_category_name(self,menuitem:MenuItem):
        category_name = Category.objects.get(title=menuitem.category)
        return category_name.title
    def update(self,menuitem:MenuItem,validated_data):
        new_category_title = validated_data['category']
        new_category = Category.objects.get(title=new_category_title)
        menuitem.category = new_category
        menuitem.save()
        return menuitem
    def create(self,validated_data):
        title = validated_data['title']
        price = validated_data['price']
        featured = validated_data['featured']
        category = Category.objects.get(title=validated_data['category'])
        instance = MenuItem.objects.create(title=title,
                                           price=price,
                                           featured=featured,
                                           category=category)
        return instance
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name',]

class UserSerializer(serializers.ModelSerializer):    
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('id','username', 'email', 'is_staff', 'groups',)
    
class SimpleCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['menuitem']
            
class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    unit_price = serializers.SerializerMethodField(method_name="calculate_unitprice")
    item = serializers.SerializerMethodField(method_name="get_title")
    price = serializers.SerializerMethodField(method_name="calculate_price")
    class Meta:
        model = Cart
        fields = ('user','menuitem','item','quantity','unit_price','price')
    
    def create(self, validated_data):
        request = self.context.get('request')
        item = validated_data['menuitem']
        unit = MenuItem.objects.get(title=item)
        serializer_unit_price = unit.price
        quantity = validated_data['quantity']
        serializer_price = serializer_unit_price * quantity
        obj = Cart.objects.create(user=request.user,
                                  menuitem=validated_data['menuitem'],
                                  quantity=validated_data['quantity'],
                                  unit_price=serializer_unit_price,
                                  price=serializer_price)
        return obj
        
    def get_title(self,cartitem:Cart):
        return cartitem.menuitem.title

    def calculate_price(self,cartitem:Cart):
        return cartitem.price
    
    def calculate_unitprice(self,cartitem:Cart):
        return cartitem.unit_price
    
class OrderManagerUpdateSerializer(serializers.ModelSerializer):
    queryset = User.objects.filter(groups__name="Delivery-Crew")
    crew_list = []
    for item in queryset:
        crew_list.append(item.username)
        
    delivery_crew = serializers.ChoiceField(choices=crew_list)
    
    class Meta:
        model = Order
        fields = ['id','status','delivery_crew']       
    
    def update(self,instance,validated_data):
        crew = validated_data['delivery_crew']
        status = validated_data['status']
        instance.status = status
        dcrew=User.objects.get(username=crew)
        instance.delivery_crew = dcrew
        instance.save()
        return instance

class OrderCustomerUpdateSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField(source='total')
    order_items = serializers.SerializerMethodField(method_name="order_items_all")
    class Meta:
        model = Order
        fields = ['date','total_price','order_items']
        
    def order_items_all(self,order:Order):
        queryset = OrderItem.objects.filter(order=order.pk)
        serializers = OrderItemSerializer(queryset,many=True)
        return serializers.data
    
class OrderItemSerializer(serializers.ModelSerializer):
    unit_price = serializers.SerializerMethodField(method_name="calculate_unitprice")
    item = serializers.SerializerMethodField(method_name="get_title")
    price = serializers.SerializerMethodField(method_name="calculate_price")
    class Meta:
        model = OrderItem
        fields = ('order','menuitem','item','quantity','unit_price','price')
    
    def create(self, validated_data):
        order = validated_data['order']
        item = validated_data['menuitem']
        quantity = validated_data['quantity']
        unit = MenuItem.objects.get(title=item)
        serializer_unit_price = unit.price
        serializer_price = serializer_unit_price * quantity
        obj = OrderItem.objects.create(order=order,
                                  menuitem=validated_data['menuitem'],
                                  quantity=validated_data['quantity'],
                                  unit_price=serializer_unit_price,
                                  price=serializer_price)
        return obj
    
    def get_title(self,cartitem:Cart):
        return cartitem.menuitem.title

    def calculate_price(self,cartitem:Cart):
        return cartitem.price
    
    def calculate_unitprice(self,cartitem:Cart):
        return cartitem.unit_price
    
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_owner = serializers.SerializerMethodField(method_name="get_user")
    total_price = serializers.ReadOnlyField(source='total')
    status = serializers.ReadOnlyField()
    delivery_crew = serializers.HiddenField(default=None)
    order_items = serializers.SerializerMethodField(method_name="order_items_all")
    crew = serializers.SerializerMethodField(method_name="get_crew")
    
    class Meta:
        model = Order
        fields = ('id','user','order_owner','crew','status','total_price','delivery_crew','date','order_items')
        order_by = ['date']
    
    def order_total(self,order:Order):
        return order.total
        
    def order_items_all(self,order:Order):
        queryset = OrderItem.objects.filter(order=order.pk)
        serializers = OrderItemSerializer(queryset,many=True)
        return serializers.data
    
    def get_crew(self,order:Order):
        check = order.delivery_crew
        if check == None:
            return None
        else:
            return order.delivery_crew.username
    
    def get_user(self,order:Order):
        return order.user.username