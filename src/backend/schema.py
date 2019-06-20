import graphene
import graphql_jwt
import main.schema
import users.schema
from django.contrib.auth.models import User as UserModel


class Query(users.schema.Query, main.schema.Query, graphene.ObjectType):
    pass


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(users.schema.UserNode)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class Mutation(users.schema.Mutation, main.schema.Mutation, graphene.ObjectType):
    login = ObtainJSONWebToken.Field() # no relay format
    verify_token = graphql_jwt.Verify.Field() # no relay format
    refresh_token = graphql_jwt.Refresh.Field() # no relay format



schema = graphene.Schema(query=Query, mutation=Mutation)
