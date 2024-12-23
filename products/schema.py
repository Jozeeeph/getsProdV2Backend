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
        image = graphene.String()

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, image=None):
        product = Product.objects.create(name=name, price=price, image=image)
        return CreateProduct(product=product)


# Define UpdateProduct Mutation
class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        price = graphene.Float()
        image = graphene.String()

    product = graphene.Field(ProductType)

    def mutate(self, info, id, name=None, price=None, image=None):
        product = Product.objects.get(pk=id)
        if name:
            product.name = name
        if price:
            product.price = price
        if image:
            product.image = image
        product.save()
        return UpdateProduct(product=product)


# Define DeleteProduct Mutation
class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            product = Product.objects.get(pk=id)
            product.delete()
            return DeleteProduct(success=True)
        except Product.DoesNotExist:
            return DeleteProduct(success=False)


# Define Mutation Class
class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()


# Define the Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
