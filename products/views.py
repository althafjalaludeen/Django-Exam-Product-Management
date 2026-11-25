# Product Management System

from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status
from products.models import Product
from products.serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import serializers


class ProductListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Product created successfully"})
        return Response(serializer.errors);

class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(data=serializer.data)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Product updated successfully", 'data': serializer.data})
        return Response(serializer.errors)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({'message': "Product deleted successfully"})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists.'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        token, created = Token.objects.get_or_create(user=user)
        data = {
            'message': 'User registered successfully',
            'username': user.username,
            'token': token.key
        }
        return Response(data, status=201)