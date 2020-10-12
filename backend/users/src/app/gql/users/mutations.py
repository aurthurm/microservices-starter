from datetime import timedelta
from fastapi.encoders import jsonable_encoder
import graphene
from graphql import GraphQLError
from sqlalchemy.orm import Session
from app.core.config import settings # noqa
from app.core import security # noqa
from app.utils import ( # noqa
    generate_password_reset_token,
    verify_password_reset_token,
)
from app.gql import deps # noqa
from app.apps.user import crud, schemas # noqa
from app.gql.users.types import UserType # noqa


from app.database.session import SessionScoped # noqa
from app.database.session import database as async_db # noqa

sync_db = SessionScoped.session_factory()


class CreateUser(graphene.Mutation):
    class Arguments:
        firstname = graphene.String(required=True)
        lastname = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        passwordc = graphene.String(required=True)
        is_superuser = graphene.Boolean(required=False)
        open_reg = graphene.Boolean(required=True)
        token = graphene.String(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserType)

    @staticmethod
    def mutate(root, info, token, open_reg, firstname, lastname, username, email, password, passwordc, is_superuser, db: Session = sync_db, ):
        if open_reg and not settings.USERS_OPEN_REGISTRATION:
            GraphQLError("Open user registration is forbidden on this server")
        active_super_user = deps.get_current_active_superuser(token=token)
        user_e = crud.user.get_by_email(db, email=email)
        if user_e:
            raise GraphQLError("A user with this email already exists in the system")
        
        user_u = crud.user.get_by_username(db, username=username)
        if user_u:
            raise GraphQLError("A user with that username already exists in the system")
        if password != passwordc:
            raise GraphQLError("Password do not match, try again")
        user_in = {
            "first_name": firstname,
            "last_name": lastname,
            "user_name": username,
            "email": email,
            "password": password,
            "is_superuser": is_superuser,
        }
        user_in = schemas.UserCreate(**user_in)
        user = crud.user.create(db, obj_in=user_in)
        if settings.EMAILS_ENABLED and user_in.email:
            # send httprequest to email service
            # email_to=user_in.email
            # username=user_in.user_name
            # password=user_in.password
            pass
        ok = True
        return CreateUser(user=user, ok=ok)


class AuthenticateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    token = graphene.String()
    token_type = graphene.String()
    user = graphene.Field(lambda: UserType)

    @staticmethod
    def mutate(root, info, username, password, db: Session = sync_db, ):            
        user = crud.user.authenticate_by_username(
            db, username=username, password=password
        )
        if not user:
            raise GraphQLError("Incorrect username or password")
        elif not crud.user.is_active(user):
            raise GraphQLError("Inactive user")
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(user.id, expires_delta=access_token_expires ),
        token_type = "bearer"
        ok = True
        return AuthenticateUser(ok=ok, token=access_token, token_type=token_type, user=user)
        
                      
class UpdateUser(graphene.Mutation):
    class Arguments:
        update_self = graphene.Boolean(required=False)
        username = graphene.String(required=False)
        firstname = graphene.String(required=False)
        lastname = graphene.String(required=False)
        email = graphene.String(required=False)
        password = graphene.String(required=False)
        passwordc = graphene.String(required=False)
        token = graphene.String(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserType)

    @staticmethod
    def mutate(root, info, token, update_self, firstname, lastname, username, email, password, passwordc, db: Session = sync_db, ):   
        """
        only a superuser can update
        get user from token if updating self
        get user from username if updating another
        """
        current_super_user = deps.get_current_active_superuser(token=token)
        if update_self:
            # user = jsonable_encoder(current_super_user)
            user = current_super_user
        else:
            if not username:
                raise GraphQLError("No username to identify user for updating")
            _user = crud.user.get_by_username(db, username=username)
            if not _user:
                raise GraphQLError("A user with that username does not exist in the system")
            # user = jsonable_encoder(_user)
            user = _user
        
        user_in = schemas.UserUpdate(**user)
        if password is not None:
            if password != passwordc:
                raise GraphQLError("New Passwords dont match")
            user_in.password = password
            
        if firstname is not None:
            user_in.first_name = firstname
            
        if lastname is not None:
            user_in.last_name = lastname
            
        if email is not None:
            user_in.email = email
            
        user = crud.user.update(db, db_obj=_user, obj_in=user_in)
        ok = True
        return AuthenticateUser(ok=ok, user=user)
    
    
class RecoverPassword(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    ok = graphene.Boolean()
    msg = graphene.String()

    @staticmethod
    def mutate(root, info, username, db: Session = sync_db, ):  
        user = crud.user.get_by_username(db, username=username)
        if not user:
            raise GraphQLError("A user with that username does not exist ")
        
        password_reset_token = generate_password_reset_token(email=user.email)
        # send httprequest to email service
        # email_to=user.email
        # email=user.email
        # token=password_reset_token
        msg = "Password recovery email sent"
        ok = True
        return RecoverPassword(ok=ok, msg=msg)
    
    
# Reset password is an api_endpoint since it will be a link