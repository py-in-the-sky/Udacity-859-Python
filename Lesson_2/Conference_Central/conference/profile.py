from protorpc import messages


class Profile(messages.Message):
    "Represents a user profile."
    userId = messages.StringField(1)
    displayName = messages.StringField(2)
    mainEmail = messages.StringField(3)
    teeShirtSize = messages.StringField(4)
