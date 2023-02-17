
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# Create your views here.


class UserView(APIView):
    """ User can access self detail"""
    def get(self, request):
        if request.user:
            print("user: ", request.user)
            user_email = request.user
            try:
                user = User.objects.get(email=user_email)
            except Exception as e:
                return Response({'error': e}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"status": "user not found please Signup first"},
                        status=status.HTTP_400_BAD_REQUEST)


class UserRegistration(APIView):
    """ user registration """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserDetail(APIView):
    """ Update User Details"""
    permission_classes = (IsAuthenticated,)
    # parser_classes = (FormParser, MultiPartParser)

    def patch(self, request):
        try:
            serializer_data = UserSerializer(User.objects.get(email=request.user), data=request.data, partial=True)
        except Exception as e:
            return HttpResponse(e)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response({"status": "success", "data": serializer_data.data})
        return Response({"status": "error", "data": serializer_data.errors})


class AdminView(APIView):
    """ Admin can get details, add new user, update detail, and delete
    users """
    permission_classes = (IsAdminUser,)

    def get(self, request, pk=None):
        if pk:
            user = User.objects.filter(pk=pk)
            if not user:
                return Response({"status": "invalid user or id"})
            serializer = UserSerializer(User.objects.get(pk=pk))
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        user = User.objects.all().order_by('id')
        serializer = UserSerializer(user, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        if pk:
            try:
                serializer_data = UserSerializer(User.objects.get(id=pk), data=request.data, partial=True)
            except Exception as e:
                return HttpResponse(e)
            print(serializer_data)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response({"status": "success", "data": serializer_data.data})
            else:
                return Response({"status": "error", "data": serializer_data.errors})
        else:
            return Response({"status": "invalid detail or attribute"})

    def delete(self, request, pk=None):
        if pk:
            user = User.objects.filter(pk=pk)
            if not user:
                return Response({'status': 'page not found'})
            user.delete()
            return Response({"status": "success", "data": "Item Deleted"})
        else:
            return Response({'error': 'user id not found'})


class UploadProfile(APIView):
    """ user profile upload """
    def patch(self, request, pk=None):
        if pk:
            try:
                file = request.data['profile_picture']
                serializer_data = UserSerializer(User.objects.get(id=pk), data=file, partial=True)
            except Exception as e:
                return HttpResponse(e)
            print(serializer_data)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response({"status": "success", "data": serializer_data.data})
            else:
                return Response({"status": "error", "data": serializer_data.errors})
        else:
            return Response({"status": "invalid detail or attribute"})
    # # print(request.user.profile_picture)
    # file = request.data['profile_picture']
    # image = User.objects.create(profile_picture=file)
    # print(image)
    # return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)
