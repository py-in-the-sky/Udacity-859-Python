from protorpc import messages


class ProfileForm(messages.Message):
    "Represents a profile form on the client side."
    displayName = messages.StringField(1)
    teeShirtSize = messages.StringField(2)
