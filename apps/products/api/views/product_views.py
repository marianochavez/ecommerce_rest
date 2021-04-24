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
        """Create product method

        """
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Producto creado correctamente'},status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ Concrete view for retrieving, updating or deleting a model instance of Product

    """
    serializer_class = ProductSerializer

    def get_queryset(self,pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk,state = True).first()

    def patch(self,request,pk=None):
        """Gets an instance of product, refill instance attributes in raw data (json)

        """
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk)) # serialize instance
            return Response(product_serializer.data,status = status.HTTP_200_OK)
        return Response({'error':'No existe un Producto con estos datos!'},status = status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk=None):
        """Update product method

        """
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk),data = request.data) # send information to serializer referencing the instance
            
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data,status = status.HTTP_200_OK)
            return Response(product_serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk=None):
        """Modified to soft delete, only change the state of a product

        """
        product = self.get_queryset().filter(id = pk).first() # get instance
        
        if product:
            product.state = False
            product.save()
            return Response({'message':'Producto eliminado correctamente!'},status = status.HTTP_200_OK)
        return Response({'error':'No existe un Producto con estos datos!'},status = status.HTTP_400_BAD_REQUEST)