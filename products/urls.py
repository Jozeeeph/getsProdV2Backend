from django.urls import path
from graphene_django.views import GraphQLView
from products.schema import schema
from django.views.decorators.csrf import csrf_exempt





urlpatterns = [
    # Only a single URL to access GraphQL
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
