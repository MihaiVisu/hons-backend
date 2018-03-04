"""hons_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from api_vlad import views as vlad_views
from api_mihai import views as mihai_views


urlpatterns = [
	path('admin/', admin.site.urls),
	path('api_vlad/test', vlad_views.test, name='test'),
	path('api_vlad/predict', vlad_views.predict, name='predict'),
	path('api_vlad/predict_pollution', vlad_views.predict_pollution, name='predict_pollution'),
	path('api_mihai/labelled_clustered_data/<int:dataset_id>/<int:number_location_clusters>/<int:number_environment_clusters>/', 
		mihai_views.labelled_unsupervised_data),
	path('api_mihai/labelled_classified_data/<int:dataset_id>/<slug:classifier>/<slug:validation_criterion>/<int:folds_number>/',
		mihai_views.labelled_classified_data),
	path('api_mihai/attributes/', mihai_views.get_attributes),
]
