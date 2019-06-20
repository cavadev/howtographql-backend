from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.shortcuts import get_token


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    token = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        firstName = graphene.String(required=True)
        lastName = graphene.String(required=True)

    def mutate(self, info, email, password, firstName, lastName):

        UserModel = get_user_model()
        user = UserModel.objects.filter(email__iexact=email).first()
        if user:
            raise Exception('User email exist!')

        user = get_user_model()(
            email=email,
            first_name= firstName,
            last_name= lastName,
        )
        user.set_password(password)
        user.save()
        user.username = 'usr' + str(user.id)
        user.save()

        return CreateUser(user=user, token=get_token(user))


class Query(graphene.AbstractType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user


class Mutation(graphene.ObjectType):
    signup = CreateUser.Field()
