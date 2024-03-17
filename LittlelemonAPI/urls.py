from django.urls import path,include
from . import views

urlpatterns = [
#    path('ratings', views.RatingsView.as_view()),
    path('djoser-token/',include('djoser.urls.authtoken')),
    path('', include('rest_framework.urls')),
    path('menu-items/', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemsView.as_view()),
    path('categories/', views.CategoryView.as_view()),
    path('categories/<int:pk>', views.SingleCategoryView.as_view()),
    path('groups/manager/users', views.ManagerManagerView.as_view()),
    path('groups/manager/users/<int:pk>', views.ManagerSingleManagerView.as_view()),
    path('groups/delivery-crew/users', views.ManagerDeliveryCrewView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.ManagerSingleDeliveryCrewView.as_view()),
    path('cart/menu-items', views.CartView.as_view()),
    path('orders', views.OrderView.as_view()),
    path('orders/<int:pk>', views.OrderUpdateView.as_view()),
]