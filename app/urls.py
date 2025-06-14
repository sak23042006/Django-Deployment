from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('',views.index, name='index'),
    path('about/',views.about, name='about'),

    path('register/',views.register, name='register'),
    path('api/register/', RegisterAPIView.as_view(), name='register-view'),
    path('login/',views.login, name='login'),

    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-register/', views.admin_register, name='admin_register'),

    
    path('api/view/', UserDetailView.as_view(), name='userdetails-view'),
    path('api/view/<int:user_id>/', ParticularUserView.as_view(), name='partuserdetails-view'),
    path('api/update/<int:user_id>/', UpdateUserDetailView.as_view(), name='update-view'),
    path('api/delete/<int:user_id>/', UserDeleteView.as_view(), name='delete-view'),
    path('home/',views.home, name='home'),
    path('profile/',views.profile, name='profile'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    path('logout/', views.logout, name='logout'),
    path('addground/', views.addground, name='addground'),
    path('api/grounds/add/', AddGroundAPIView.as_view(), name='add-ground'),
    path('api/grounds/', ViewGroundsAPIView.as_view(), name='view-grounds'),
    path('viewgrounds/', views.viewgrounds, name='viewgrounds'),
    path('updategrounds/<int:id>/', views.updategrounds, name='updategrounds'),
    path('deleteground/<int:id>/', views.deleteground, name='deleteground'),
    path('addSlots/', views.addSlots, name='addSlots'),
    path('viewSlots/', views.viewSlots, name='viewSlots'),
    path('getBookedSlots/<str:groundname>/', views.getBookedSlots, name='getBookedSlots'),
    path('slotPayment/<int:slotId>/', views.slotPayment, name='slotPayment'),
    path('viewUserBookings/', views.viewUserBookings, name='viewUserBookings'),
    path('addTeam/<int:paymentID>/', views.addTeam, name='addTeam'),
    path('viewTeam/', views.viewTeam, name='viewTeam'),
    path('otherUsersBookingSlots/', views.otherUsersBookingSlots, name='otherUsersBookingSlots'),
    path('sendRequest/<int:teamID>/', views.sendRequest, name='sendRequest'),
    path('teamRequests/', views.teamRequests, name='teamRequests'),
    path('acceptUserRequest/<int:requestID>/', views.acceptUserRequest, name='acceptUserRequest'),
    path('deleteSlot/<int:slotId>/', views.deleteSlot, name='deleteSlot'),
    path('removeUserFromTeam/<int:teamID>/<str:userName>', views.removeUserFromTeam, name='removeUserFromTeam')

]
