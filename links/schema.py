# from django.contrib.auth import get_user_model
from datetime import datetime

from django.db.models import Q
import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError

from .models import Link


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.ObjectType):
    links = graphene.List(
        LinkType, search=graphene.String(), first=graphene.Int(), skip=graphene.Int()
    )

    def resolve_links(self, info, search=None, first=None, skip=None, orderBy=None, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not authenticated.")

        query_results = Link.objects.filter(posted_by=user)

        if search:
            filter = (
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(url__icontains=search)
            )
            query_results = query_results.filter(filter)

        if skip:
            query_results = query_results[skip:]

        if first:
            query_results = query_results[:first]

        if orderBy:
            query_results = query_results.order_by("-updated_at")

        return query_results


class CreateLink(graphene.Mutation):
    link = graphene.Field(LinkType)
    # posted_by = graphene.Field(UserType)

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        url = graphene.String(required=True)

    def mutate(self, info, title, description, url):
        user = info.context.user or None

        if user.is_anonymous:
            raise GraphQLError("Not authenticated.")

        link = Link(title=title, description=description, url=url, posted_by=user)
        link.save()

        return CreateLink(link=link)


class UpdateLink(graphene.Mutation):
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, link_id, title, description, url):
        user = info.context.user or None

        if user.is_anonymous:
            raise GraphQLError("Not authenticated.")

        link = Link.objects.get(id=link_id)

        if link.posted_by != user:
            raise GraphQLError("Not authorized to update that link.")

        link.title = title
        link.description = description
        link.url = url

        link.save()

        return UpdateLink(link=link)


class DeleteLink(graphene.Mutation):
    link_id = graphene.Int()

    class Arguments:
        link_id = graphene.Int(required=True)

    def mutate(self, info, link_id):
        user = info.context.user or None

        if user.is_anonymous:
            raise GraphQLError("Not authenticated.")

        link = Link.objects.get(id=link_id)

        if link.posted_by != user:
            raise GraphQLError("Not authorized to delete that link.")

        link.delete()

        return DeleteLink(link_id=link_id)


class Mutation(graphene.ObjectType):
    create_link = CreateLink().Field()
    update_link = UpdateLink().Field()
    delete_link = DeleteLink().Field()
