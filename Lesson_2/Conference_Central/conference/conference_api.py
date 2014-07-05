from endpoints import UnauthorizedException, get_current_user
from protorpc import remote
from constants import *
from profile import Profile
from profile_form import ProfileForm


package = 'conference'


def _extractDefaultDisplayNameFromEmail(email):
    """Get the display name from the user's email. For example, if the
    email is lemoncake@example.com, then the display name becomes
    "lemoncake."
    """
    return None if email is None else email[:email.index('@')]


@endpoints.api(name='conference', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE],
               scopes=[EMAIL_SCOPE],
               description='API for Conference Central backend app.')
class ConferenceApi(remote.Service):
    "Defines full Conference Central API."

    @endpoints.method(ProfileForm, Profile, name='saveProfile', path='profile')
    def save_profile(self, request):
        # user = users.get_current_user()
        user = get_current_user()

        if user is None:
            raise UnauthorizedException("Authorization required.")

        user_id = user.user_id()
        main_email = user.email()
        display_name = (request.displayName or
                        _extractDefaultDisplayNameFromEmail(main_email))
        teeshirt_size = request.teeShirtSize or 'NOT_SPECIFIED'

        return Profile(userId=user_id, displayName=display_name,
                       mainEmail=main_email, teeShirtSize=teeshirt_size)


app = endpoints.api_server([ConferenceApi])
