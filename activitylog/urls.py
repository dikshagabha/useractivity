from django.urls import path
from . import views

urlpatterns = [
    path('user-activity/', views.CreateActivityLogView.as_view(), name='create-activity'),
    path('user-activity/<int:user_id>/', views.UserActivityLogListView.as_view(), name='user-activity'),
    path('user-activity/all/', views.AllActivityLogView.as_view(), name='all-activity'),
    path('user-activity/update/<int:pk>/', views.UpdateActivityStatusView.as_view(), name='update-activity-status'),
]
