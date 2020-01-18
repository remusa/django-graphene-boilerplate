from django.contrib.auth import get_user_model
import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
import graphql_jwt


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        # fields = ("id", "email", "username")
        exclude = ("password", "is_admin", "is_staff", "is_superuser")


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.List(UserType, id=graphene.Int(required=True))
    me = graphene.Field(UserType)

    def resolve_users(self, info):
        # return get_user_model().objects.all()
        user = info.context.user

        if user.is_superuser or user.is_staff:
            return get_user_model().objects.all()

        raise GraphQLError("Not authorized.")

    def resolve_user(self, info, id):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("Not logged in.")

        if user.is_superuser or user.is_staff:
            return get_user_model().objects.all().filter(id=id)
        return GraphQLError("Not authorized.")

    def resolve_me(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("Not logged in.")

        return user


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(username=username, email=email)

        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
