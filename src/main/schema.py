import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required
from graphql_relay.node.node import from_global_id
from django.db.models import Q

from .models import Link, Vote
from users.schema import UserNode


class CountableConnection(graphene.relay.Connection):
    # to consider: https://github.com/graphql-python/graphene-django/issues/177
    total_count = graphene.Int()

    class Meta:
        abstract = True

    def resolve_total_count(self, info):
        # return self.length
        count = getattr(self, 'length')
        if count is None:
            count = self.iterable.count()
        return count


class LinkNode(DjangoObjectType):
    class Meta:
        model = Link
        interfaces = (graphene.relay.Node, )
        connection_class = CountableConnection


class LinkFilter(django_filters.FilterSet):
    class Meta:
        model = Link
        fields = {
            'url': ['icontains'],
            'description': ['icontains']
        }


class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (graphene.relay.Node,)


class CreateLink(graphene.relay.ClientIDMutation):
    link = graphene.Field(LinkNode)

    class Input:
        url = graphene.String()
        description = graphene.String()

    @login_required
    def mutate_and_get_payload(root, info, **input):
        user = info.context.user or None

        link = Link(
            url=input.get('url'),
            description=input.get('description'),
            posted_by=user,
        )
        link.save()

        return CreateLink(link=link)


class CreateVote(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserNode)
    link = graphene.Field(LinkNode)

    class Input:
        link_id = graphene.String()

    @login_required
    def mutate_and_get_payload(root, info, **input):
        user = info.context.user or None

        link = Link.objects.filter(id=from_global_id(input['link_id'])[1]).first()
        if not link:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)


class Query(graphene.ObjectType):
    link = graphene.relay.Node.Field(LinkNode)
    vote = graphene.relay.Node.Field(VoteNode)
    links = DjangoFilterConnectionField(
        LinkNode,
        filterset_class=LinkFilter,
        search=graphene.String(),
        orderBy=graphene.String()
    )

    def resolve_links(self, info, **kwargs):
        queryset = Link.objects.all()
        # queryset = LinkFilter(data=**kwargs, queryset=self.links).qs
        # queryset = LinkFilter(kwargs).qs

        search_term = kwargs.get('search', None)
        order_by = kwargs.get('orderBy', None)

        if search_term:
            filter = (
                Q(url__icontains=search_term) |
                Q(description__icontains=search_term)
            )
            queryset = queryset.filter(filter)

        if order_by:
            queryset = queryset.order_by(order_by)

        return queryset


class Mutation(graphene.AbstractType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()
