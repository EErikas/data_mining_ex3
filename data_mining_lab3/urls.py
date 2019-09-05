"""data_mining_lab3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from algorithm_examples import views as ae_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('decision_tree/', ae_views.view_decision_tree, name='decision-tree'),
    path('id_carver/', ae_views.text_mining, name='text-mining'),
    path('corporate_id/<str:corporate_id>', ae_views.corporate_id_checker, name='corporate-id-checker'),
    path('personal_id/<str:personal_id>', ae_views.personal_id_data, name='personal-id-checker'),
    path('', ae_views.homepage, name='home')
]
