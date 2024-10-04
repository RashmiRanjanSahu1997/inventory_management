from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
import logging
from .models import Item
from .serializers import ItemSerializer
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

# Initialize logger
logger = logging.getLogger(__name__)

class ItemCreateView(APIView):
    def post(self, request):
        try:
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info("Item created successfully")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.warning(f"Validation failed for item creation: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ItemDetailView(APIView):
    def get(self, request, item_id):
        try:
            item = get_object_or_404(Item, id=item_id)
            serializer = ItemSerializer(item)
            logger.info(f"Item with id {item_id} retrieved successfully")
            return Response(serializer.data)
        except Item.DoesNotExist:
            logger.warning(f"Item with id {item_id} not found")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, item_id):
        try:
            item = get_object_or_404(Item, id=item_id)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Item with id {item_id} updated successfully")
                return Response(serializer.data)
            logger.warning(f"Validation failed for item update: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            logger.warning(f"Item with id {item_id} not found")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, item_id):
        try:
            item = get_object_or_404(Item, id=item_id)
            item.delete()
            logger.info(f"Item with id {item_id} deleted successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            logger.warning(f"Item with id {item_id} not found")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   