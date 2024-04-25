from math import sqrt

from django.db.models import Q
from rest_framework import generics, status
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from livero.api.seriaizer import *
from livero.models import *


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class Login(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class ListTests(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TestsSerializer

    def list(self, request, *args, **kwargs):
        tests = Tests.objects.all()
        tests_serializer = self.serializer_class(tests, many=True).data
        return Response(tests_serializer)


class ListSymptoms(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Symptoms.objects.all()

    def list(self, request, *args, **kwargs):
        symptoms = Symptoms.objects.all()
        symptoms_serializer = SymptomsSerializer(symptoms, many=True)
        chronic_diseases = ChronicDiseases.objects.all()
        chronic_diseases_serializer = ChronicDiseasesSerializer(chronic_diseases, many=True)
        allergy = MedicineAllergy.objects.all()
        allergy_serializer = MedicineAllergySerializer(allergy, many=True)
        data = {
            "symptoms": symptoms_serializer.data,
            "chronic_diseases": chronic_diseases_serializer.data,
            "allergy": allergy_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class CreateReadingForUser(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        symptoms = Symptoms.objects.filter(id__in=request.data.get("symptoms"))
        chronic_diseases = ChronicDiseases.objects.filter(id__in=request.data.get("chronic_diseases"))
        user = Users.objects.filter(id=request.user.id).first()

        serializer = ReadingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(users=user)
        user_reading = Readings.objects.filter(id=serializer.data.get('id')).first()
        print(user_reading)
        for sym in symptoms:
            user_reading.symptoms.add(sym)
        for cd in chronic_diseases:
            user_reading.chironic_dieases.add(cd)
        user_reading.save()
        tests = Tests.objects.all()
        tests_serializer = TestsSerializer(tests, many=True).data
        return Response(tests_serializer)


class ListDoctors(generics.ListAPIView):
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        doctors = Doctors.objects.all()
        serializer = DoctorSerializer(doctors, many=True)

        return Response(serializer.data)


class ListHospitals(generics.ListAPIView):
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        hospitals = Hospitals.objects.all().order_by('rating')
        full_url = request.build_absolute_uri().split('/api')[0]

        serializer = HospitalSerializer(hospitals, many=True)
        hospitals_data = serializer.data
        final_data = []
        for data in hospitals_data:
            if data.get('image'):
                data['image'] = full_url + data['image']
            final_data.append(data)
        return Response(final_data)


class ListLaps(generics.ListAPIView):
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        laps = Laps.objects.all().order_by('rating')
        full_url = request.build_absolute_uri().split('/api')[0]

        serializer = LapsSerializer(laps, many=True)
        labs_data = serializer.data
        final_data = []
        for data in labs_data:
            if data.get('image'):
                data['image'] = full_url + data['image']
            final_data.append(data)
        return Response(final_data)


class UpdateReadings(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        reading = Readings.objects.filter(id=request.data.get("reading_id")).first()
        user = Users.objects.filter(id=request.user.id).first()
        alt = request.data.get("alt")
        ast = request.data.get("ast")
        plt = request.data.get("plt")
        fbi = (user.age * ast) / (plt * sqrt(alt))

        fbi = round(fbi, 2)
        print(fbi)
        user_status = None
        for status in UserStatus.objects.all():
            if status.min <= fbi < status.max:
                user_status = status
                break  # Exit the loop after finding a match

        if user_status:
            # Proceed with the user_status as planned
            reading.user_status = user_status
            # ... rest of your code
        else:
            # Handle the case where no matching user status is found
            print("No matching user status found for fbi")

        print(user_status)
        reading.blood = request.data.get("blood")
        reading.urine = request.data.get("urine")
        reading.kidney = request.data.get("kidney")
        reading.fbi_result = fbi
        reading.save()
        data = {
            "status": user_status.status,
            'fbi_result': fbi
        }
        return Response(data)


class ListHome(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        readings = Readings.objects.filter(users_id=request.user.id)
        serializer = ReadingsSerializer(readings, many=True)
        completed = []
        uncompleted = []
        for reading in serializer.data:
            if float(reading.get("fbi_result")) > 0.00:
                completed.append(reading)
            else:
                uncompleted.append(reading)

        data = {
            "completed": completed,
            "uncompleted": uncompleted
        }
        return Response(data)
