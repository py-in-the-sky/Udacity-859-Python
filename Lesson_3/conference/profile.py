from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsModel


class Profile(EndpointsModel):
    "Represents a user profile."

    _message_fields_schema = ('userId', 'displayName',
                              'mainEmail', 'teeShirtSize')

    userId = ndb.StringProperty()  # messages.StringField(1)
    displayName =  ndb.StringProperty()  # messages.StringField(2)
    mainEmail = ndb.StringProperty()  # messages.StringField(3)
    teeShirtSize = ndb.StringProperty()  # messages.StringField(4)

    def update(self, displayName, teeShirtSize):
        "update values of displayName and teeShirtSize if changed"
        if displayName:
            self.displayName = displayName

        if teeShirtSize:
            self.teeShirtSize = teeShirtSize
