from django.urls import path

from livero.api.views import ListSymptoms, RegisterView, Login, ListTests, CreateReadingForUser, ListDoctors, \
    ListHospitals, ListLaps, UpdateReadings, ListHome
from livero.models import Symptoms

urlpatterns = [
    path("list_symptoms", ListSymptoms.as_view(), name="list_symptoms"),
    path('signup', RegisterView.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path("list_test", ListTests.as_view(), name="list_test"),
    path("create_reading", CreateReadingForUser.as_view(), name="create_reading"),
    path("list_doctors", ListDoctors.as_view(), name="list_doctors"),
    path("list_hospitals", ListHospitals.as_view(), name="list_hospitals"),
    path("list_laps", ListLaps.as_view(), name="list_laps"),
    path("update_reading", UpdateReadings.as_view(), name="update_reading"),
    path("list_home", ListHome.as_view(), name="list_home"),


]
