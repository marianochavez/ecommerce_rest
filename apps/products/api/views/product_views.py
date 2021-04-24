from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from apps.base.api import GeneralListAPIView
from apps.products.api.serializers.product_serializers import ProductSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    """ Concrete view for listing a queryset or creating a model instance of Product

    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)

    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Producto creado correctamente'},status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class ProductRetrieveAPIView(generics.RetrieveAPIView):
    """Its like list api view but only gets one product with his pk

    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)

class ProductRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    """Delete Product, I change generics.DestroyAPIView to generics.RetrieveDestroyAPIView
        to see the attributes of the product I want to delete

    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        """Get the model name with self.get_serializer().Meta.model
            and filter state true
        """
        return self.get_serializer().Meta.model.objects.filter(state=True)

    def delete(self,request,pk=None):
        """Modified to soft delete, only change the state of a product

        """
        product = self.get_queryset().filter(id=pk).first()
        if product:
            product.state = False
            product.save()
            return Response({'message':'Producto eliminado correctamente!'},status = status.HTTP_200_OK)
        return Response({'error':'No existe un producto con estos datos!'},status = status.HTTP_400_BAD_REQUEST)

class ProductRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Update product and see his attributes with retrieve

    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        """Get the model name with self.get_serializer().Meta.model
            and filter state true
        """
        return self.get_serializer().Meta.model.objects.filter(state=True)

    """
    Example of method path and put, unused

    def get_queryset(self,pk):
        return self.get_serializer().Meta.model.objects.filter(state = True).filter(id = pk).first()

    def patch(self,request,pk=None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk)) # serialize instance
            return Response(product_serializer.data,status = status.HTTP_200_OK)
        return Response({'error':'No existe un Producto con estos datos!'},status = status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk=None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk),data = request.data) # send information to serializer referencing the instance
            
            if product_serializer.is_valid(): # serializer validations
                product_serializer.save()
                return Response(product_serializer.data,status = status.HTTP_200_OK)
            return Response(product_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    """