import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote


# this section corresponds to Constants.java
WEB_CLIENT_ID = 'replace this with your web client ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID


# this line is unique to Python -- no counterpart in the Java version
package = 'Hello'


# this section corresponds to HelloClass.java
class HelloClass(messages.Message):
    """Greeting that stores a message"""
    message = messages.StringField(1)


# this section corresponds to HelloWorldEndpoints.java
@endpoints.api(name='helloworldendpoints', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE],
               scopes=[endpoints.EMAIL_SCOPE],
               description='API for hello world endpoints.')
class HelloWorldEndpoints(remote.Service):
    """Helloworld API v1."""

    @endpoints.method(message_types.VoidMessage, HelloClass,
                      name='sayHello',
                      path='sayHello',
                      http_method='GET')
    def say_hello(self, request):
        return HelloClass(message='Hello World')

    NAME_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        name=messages.StringField(1, required=True)
    )

    @endpoints.method(NAME_RESOURCE, HelloClass,
                      name='sayHelloByName',
                      path='sayHelloByName/{name}',
                      http_method='GET')
    def say_hello_by_name(self, request):
        message = 'Hello ' + (request.name if request.name else 'you') + '!'
        return HelloClass(message=message)

    PERIOD_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        name=messages.StringField(1, required=True),
        period=messages.StringField(2, required=True)
    )

    @endpoints.method(PERIOD_RESOURCE, HelloClass,
               name='greetByPeriod',
               path='greetByPeriod/{name}/{period}',
               http_method='GET')
    def greet_by_period(self, request):
        name = request.name
        period = request.period
        message = ('Good ' + (period if period else 'day')
                   + ' ' + (name if name else 'you') + '!')
        return HelloClass(message=message)


# this line is unique to Python -- no counterpart in the Java version
app = endpoints.api_server([HelloWorldEndpoints])
