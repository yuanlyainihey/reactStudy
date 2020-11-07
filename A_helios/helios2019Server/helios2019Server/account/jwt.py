def jwt_response_payload_handler(token, user=None, request=None):
    """自定义登录成功后的返回信息，是给前端的"""
    return {
        'username': user.username,
        'id': user.id,
        'groups': [i.name for i in user.groups.all()],
        'token': token
    }
