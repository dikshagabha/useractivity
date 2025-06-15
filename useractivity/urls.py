"""
URL configuration for useractivity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# from activitylog.views import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('activitylog.urls')),
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/user-activity/', views.CreateActivityLogView.as_view(), name='create-activity'),
    # path('api/user-activity/<int:user_id>/', views.UserActivityLogListView.as_view(), name='user-activity'),
    # path('api/user-activity/all/', views.AllActivityLogView.as_view(), name='all-activity'),
    # path('api/user-activity/update/<int:pk>/', views.UpdateActivityStatusView.as_view(), name='update-activity-status'),
]
