import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
import graphene
from graphene_django import DjangoObjectType
from .models import Product


# Define ProductType for GraphQL
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "image")


# Define Query Class
class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)
    product = graphene.Field(ProductType, id=graphene.Int())

    def resolve_all_products(self, info):
        return Product.objects.all()

    def resolve_product(self, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None


# Define CreateProduct Mutation
class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        image = graphene.String()  # Base64 image string

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, image=None):
        if image:
            # Ensure base64 string is in the correct format
            if image.startswith('data:image'):
                image = image.split('base64,')[1]  # Remove 'data:image/jpeg;base64,' part

            # Decode the base64 string
            try:
                image_data = base64.b64decode(image)
                image_file = ContentFile(image_data, name="product_image.jpg")  # Assign name
                product = Product(name=name, price=price, image=image_file)  # Store image file
                product.save()
            except Exception as e:
                raise Exception(f"Error decoding image: {str(e)}")
        else:
            product = Product(name=name, price=price)
            product.save()

        return CreateProduct(product=product)


# Define UpdateProduct Mutation
class UpdateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        price = graphene.Float()
        image = graphene.String()

    def mutate(self, info, id, name, price, image):
        try:
            product = Product.objects.get(id=id)
            product.name = name
            product.price = price
            product.image = image  # Assuming the image is base64 encoded
            product.save()
            return UpdateProduct(product=product)
        except Product.DoesNotExist:
            return UpdateProduct(product=None)


# Define DeleteProduct Mutation
class DeleteProduct(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.ID()

    def mutate(self, info, id):
        try:
            product = Product.objects.get(id=id)
            product.delete()
            return DeleteProduct(success=True, message="Product deleted successfully")
        except Product.DoesNotExist:
            return DeleteProduct(success=False, message="Product not found")


# Define Mutation Class
class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()


# Define the Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
