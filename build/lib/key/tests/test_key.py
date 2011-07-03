from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.conf import settings
from key.models import ApiKey, ApiKeyProfile, generate_unique_api_key
import hashlib

class ApiKeyTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='ApiKeyTest',
                                        email='ApiKeyTest@t.com')
        self.user.save()
        generate_unique_api_key(self.user)

    def test_key_generation(self):
        k = generate_unique_api_key(self.user)
        my_kstr = hashlib.md5('%s-%s' % (self.user.email,
                                         k.created)).hexdigest()
        self.assertEquals(my_kstr, k.key)
        self.assertEquals(ApiKey.objects.filter(user=self.user).coutn(),
                          2)

    def test_authentication(self):
        client = Client()
        auth_header = getattr( settings, 'APIKEY_AUTHORIZATION_HEADER',
                               'Authorization' )
        auth_header = 'HTTP_%s' % ( auth_header.upper( ).replace( '-', '_' ) )

        rv = client.get(reverse('test_key_list'),
                        **{auth_header: self.user.api_keys.all()[0]})
        self.assertEquals(rv.status_code, 200)
        print rv

