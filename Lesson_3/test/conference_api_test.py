# see the following links for information on GAE and unit testing in Python:
# https://developers.google.com/appengine/docs/python/tools/localunittesting


import sys
import os


# point to project root
# sys.path.insert(1, os.path.abspath('..'))


import unittest
import conference.conference_api as api
from conference.profile import Profile
from google.appengine.api.users import User
from google.appengine.ext import testbed
from endpoints import UnauthorizedException
from protorpc import messages


class ConferenceApiTests(unittest.TestCase):
    EMAIL = "example@gmail.com"
    USER_ID = "123456789"
    TEE_SHIRT_SIZE = 'NOT_SPECIFIED'
    DISPLAY_NAME = "Your Name Here"
    NAME = "GCP Live"
    DESCRIPTION = "New announcements for Google Cloud Platform"
    CITY = "San Francisco"
    MONTH = 3
    CAP = 500

    # These values will be constructed in the setUp method, which is called
    # before each test is run.
    user = None
    conferenceApi = api.ConferenceApi()  # None
    helper = testbed.Testbed()  # None

    def setUp(self):
        # At first, create an instance of the Testbed class.
        self.helper = testbed.Testbed()
        # Then activate the testbed which will prepare the usage of service stubs.
        self.helper.activate()
        # Next, declare which service stubs you want to use.
        self.helper.init_datastore_v3_stub()
        # The init_datastore_v3_stub() method with no argument uses an in-memory
        # datastore that is initially empty. If you want to test an existing
        # datastore entity, include its pathname as an argument to
        # init_datastore_v3_stub().

        self.user = User(email=self.EMAIL, _auth_domain='gmail.com',
                         _user_id=self.USER_ID)
        self.conferenceApi = api.ConferenceApi()

    def tearDown(self):
        # Never forget to deactivate the testbed once the tests are
        # completed. Otherwise the original stubs will not be restored.
        self.helper.deactivate()

    def testGetProfileWithoutUser(self):
        self.assertRaises(UnauthorizedException,
                          self.conferenceApi.get_profile,
                          messages.Message())

    def testGetProfileFirstTime(self):
        profile = self.conferenceApi.get_profile(self.user)
        self.assertIsNone(profile)

    def testSaveProfile(self):
        profile = Profile()
        profile.teeShirtSize = self.TEE_SHIRT_SIZE
        profile.displayName = self.DISPLAY_NAME

        self.assertIsNone(profile.userId)
        self.assertIsNone(profile.mainEmail)

        # check return value first
        profile = self.conferenceApi.save_profile(profile)
        self.assertEquals(self.USER_ID, profile.userId)
        self.assertEquals(self.EMAIL, profile.mainEmail)
        self.assertEquals(self.TEE_SHIRT_SIZE, profile.teeShirtSize)
        self.assertEquals(self.DISPLAY_NAME, profile.displayName)

        # check datastore directly
        profile = Profile.query().fetch(1)
        self.assertEquals(self.USER_ID, profile.userId)
        self.assertEquals(self.EMAIL, profile.mainEmail)
        self.assertEquals(self.TEE_SHIRT_SIZE, profile.teeShirtSize)
        self.assertEquals(self.DISPLAY_NAME, profile.displayName)

    def testSaveProfileWithNull(self):
        profile = Profile()  # all fields are None
        # save profile with no fields set
        profile = self.conferenceApi.save_profile(profile)

        displayName = self.EMAIL[:self.EMAIL.index('@')]

        # check return value
        self.assertEquals(self.USER_ID, profile.userId)
        self.assertEquals(self.EMAIL, profile.mainEmail)
        self.assertEquals(self.TEE_SHIRT_SIZE, profile.teeShirtSize)
        self.assertEquals(displayName, profile.displayName)

        # check datastore directly
        profile = Profile.query().fetch(1)
        self.assertEquals(self.USER_ID, profile.userId)
        self.assertEquals(self.EMAIL, profile.mainEmail)
        self.assertEquals(self.TEE_SHIRT_SIZE, profile.teeShirtSize)
        self.assertEquals(displayName, profile.displayName)

    def testGetProfile(self):
        profile = Profile()
        profile.teeShirtSize = self.TEE_SHIRT_SIZE
        profile.displayName = self.DISPLAY_NAME

        self.conferenceApi.save_profile(profile)

        profile = self.conferenceApi.get_profile()
        self.assertEquals(self.USER_ID, profile.userId)
        self.assertEquals(self.EMAIL, profile.mainEmail)
        self.assertEquals(self.TEE_SHIRT_SIZE, profile.teeShirtSize)
        self.assertEquals(self.DISPLAY_NAME, profile.displayName)

    def testUpdateProfile(self):
        # save for the first time
        profile = Profile()
        profile.teeShirtSize = self.TEE_SHIRT_SIZE
        profile.displayName = self.DISPLAY_NAME

        self.conferenceApi.save_profile(profile)

        profile = Profile.query().fetch(1)
        self.assertEquals(self.USER_ID, profile.userId)
        self.assertEquals(self.EMAIL, profile.mainEmail)
        self.assertEquals(self.TEE_SHIRT_SIZE, profile.teeShirtSize)
        self.assertEquals(self.DISPLAY_NAME, profile.displayName)

        # then try to update it
        new_name = 'New Name'
        new_tee_size = 'L'

        new_profile = Profile()
        new_profile.displayName = new_name
        new_profile.teeShirtSize = new_tee_size
        self.conferenceApi.save_profile(new_profile)

        profile = Profile.query().fetch(1)
        self.assertEquals(self.USER_ID, profile.userId)
        self.assertEquals(self.EMAIL, profile.mainEmail)
        self.assertEquals(new_tee_size, profile.teeShirtSize)
        self.assertEquals(new_name, profile.displayName)

    def testUpdateProfileWithNulls(self):
        # save for the first time
        profile = Profile()
        profile.teeShirtSize = self.TEE_SHIRT_SIZE
        profile.displayName = self.DISPLAY_NAME

        self.conferenceApi.save_profile(profile)

        profile.teeShirtSize = None
        profile.displayName = None

        profile = self.conferenceApi.save_profile(profile)

        # check return value
        self.assertEquals(self.USER_ID, profile.userId)
        self.assertEquals(self.EMAIL, profile.mainEmail)
        self.assertEquals(self.TEE_SHIRT_SIZE, profile.teeShirtSize)
        self.assertEquals(self.DISPLAY_NAME, profile.displayName)

        # check datastore directly
        profile = Profile.query().fetch(1)
        self.assertEquals(self.USER_ID, profile.userId)
        self.assertEquals(self.EMAIL, profile.mainEmail)
        self.assertEquals(self.TEE_SHIRT_SIZE, profile.teeShirtSize)
        self.assertEquals(self.DISPLAY_NAME, profile.displayName)





  # def testInsertEntity(self):
  #   # Because we use the datastore stub, this put() does not have
  #   # permanent side effects.
  #   TestModel().put()
  #   fetched_entities = TestModel.all().fetch(2)
  #   self.assertEqual(1, len(fetched_entities))
  #   self.assertEqual(42, fetched_entities[0].number)

if __name__ == '__main__':
    unittest.main()
