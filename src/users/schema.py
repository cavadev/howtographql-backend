from django.contrib.auth import get_user_model
import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphql_jwt.shortcuts import get_token
from graphene_django.filter import DjangoFilterConnectionField


class UserNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
        interfaces = (graphene.relay.Node, )


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']


class CreateUser(graphene.relay.ClientIDMutation):
    token = graphene.String()
    user = graphene.Field(UserNode)

    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        firstName = graphene.String(required=True)
        lastName = graphene.String(required=True)

    def mutate_and_get_payload(root, info, **input):
        UserModel = get_user_model()
        user = UserModel.objects.filter(email__iexact=input.get('email')).first()

        if user:
            raise Exception('User email exist!')

        user = get_user_model()(
            email= input.get('email'),
            first_name= input.get('firstName'),
            last_name= input.get('lastName'),
        )

        user.set_password(input.get('password'))
        user.save()
        user.username = 'usr' + str(user.id)
        user.save()

        return CreateUser(user=user, token=get_token(user))


class Query(graphene.ObjectType):
    me = graphene.Field(UserNode) # no relay format
    # me = graphene.relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode, filterset_class=UserFilter)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user


class Mutation(graphene.AbstractType):
    signup = CreateUser.Field()
