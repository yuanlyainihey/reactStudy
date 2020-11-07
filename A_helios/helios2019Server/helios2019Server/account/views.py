from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from account.serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework import generics
from rest_framework_jwt.settings import api_settings


class UserRegisterList(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = ()
    authentication_classes = ()

    def create(self, request):
        """
          创建新用户，注册，不应该进行身份认证
        """
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()

    def retrieve(self, request, pk=None):
        """
        经过身份验证的用户自动登录
        """
        # try:
        #     user = User.objects.get(pk=pk)
        # except User.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserLoginSerializer(request.user)
        return Response(serializer.data)


class UserLoginList(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = ()
    authentication_classes = ()

    def create(self, request):
        """
          用户登录，需要签发token
        """
        try:
            user_obj = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response("不存在该用户", status=status.HTTP_401_UNAUTHORIZED)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # 生成载荷信息(payload),根据user的信息生成一个payload
        payload = jwt_payload_handler(user_obj)
        # 根据payload和secret_key，采用HS256，生成token.
        token = jwt_encode_handler(payload)
        serializer = UserLoginSerializer(user_obj)
        response_data = serializer.data
        response_data['token'] = token
        return Response(response_data)
