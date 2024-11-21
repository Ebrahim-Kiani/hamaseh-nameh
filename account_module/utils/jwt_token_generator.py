from rest_framework_simplejwt.tokens import AccessToken, RefreshToken



def get_token_for_user(user):
    access = str(AccessToken.for_user(user))
    refresh = str(RefreshToken.for_user(user))
    json_tokens = {
        'refresh': refresh,
        'access': access

    }
    return json_tokens
