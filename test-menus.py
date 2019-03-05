import unittest
from mock import patch
from decorators import get_menu_entries

class MenuTestCase(unittest.TestCase):

    @patch('mod_auth.models.User')
    def test_simple_menu(self,mock_user):
        """
        Passing a menu entry to get_menu_entries() when all the routes are accessible (simulating admin)
        and verifying against correct menu structure.
        """
        mu=mock_user.return_value
        mu.can_access_route.return_value=True

        entries = get_menu_entries(
            mu, 'Configuration', 'cog', '', [
                {'title': 'Notif. services', 'icon': 'bell-o', 'route':
                    'config.notifications', 'entries': [{'title': 'Notif. services', 'icon': 'bell-o', 'route':
                    'config.notifications', 'entries': [{'title': 'Honeypot services', 'icon': 'sliders', 'route':
                    'config.services', 'entries': [{'title': 'Profile mgmt', 'icon': 'bookmark', 'route':
                    'honeypot.profiles'}]}]}]},
                {'title': 'Data processing', 'icon': 'exchange', 'route':
                    'config.data_processing'},
                {'title': 'Honeypot services', 'icon': 'sliders', 'route':
                    'config.services'}
            ]
        )

        correct_entries={'entries': [{'title': 'Notif. services', 'route': 'config.notifications', 'entries': [{'title': 'Notif. services', 'route': 'config.notifications', 'entries': [{'title': 'Honeypot services', 'route': 'config.services', 'entries': [{'title': 'Profile mgmt', 'route': 'honeypot.profiles', 'icon': 'bookmark'}], 'icon': 'sliders'}], 'icon': 'bell-o'}], 'icon': 'bell-o'}, {'route': 'config.data_processing', 'title': 'Data processing', 'icon': 'exchange'}, {'route': 'config.services', 'title': 'Honeypot services', 'icon': 'sliders'}], 'icon': 'cog', 'title': 'Configuration'}

        self.assertDictEqual(entries,correct_entries)


    @patch('mod_auth.models.User')
    def test_menu_with_no_permissions(self, mock_user):
        """
        Passing a menu entry to the function under test when the user is not
        allowed to access any route. This should return an empty dictionary.
        """
        mu = mock_user.return_value
        mu.can_access_route.return_value=False
        entries = get_menu_entries(
            mu, 'Configuration', 'cog', '', [
                {'title': 'Notif. services', 'icon': 'bell-o', 'route':
                    'config.notifications', 'entries': [{'title': 'Notif. services', 'icon': 'bell-o', 'route':
                    'config.notifications', 'entries': [{'title': 'Honeypot services', 'icon': 'sliders', 'route':
                    'config.services', 'entries': [{'title': 'Profile mgmt', 'icon': 'bookmark', 'route':
                    'honeypot.profiles'}]}]}]},
                {'title': 'Data processing', 'icon': 'exchange', 'route':
                    'config.data_processing'},
                {'title': 'Honeypot services', 'icon': 'sliders', 'route':
                    'config.services'}
            ]
        )
        correct_entries={}

        self.assertDictEqual(entries,correct_entries)


    @patch('mod_auth.models.User')
    def test_menu_with_partial_permissions(self, mock_user):
        """
        Passing a menu entry to the function get_menu_entries() when the user is not
        allowed to access the route of one of the sub-entries with 'route' = 'honeypot.profiles'
        This should return a dictionary without this entry.
        """
        mu = mock_user.return_value

        def side_effect(*args):
            if args[0] == 'honeypot.profiles':
                return False
            return True

        mu.can_access_route.side_effect = side_effect
        entries = get_menu_entries(
            mu, 'Configuration', 'cog', '', [
                {'title': 'Notif. services', 'icon': 'bell-o', 'route':
                    'config.notifications', 'entries': [{'title': 'Notif. services', 'icon': 'bell-o', 'route':
                    'config.notifications', 'entries': [{'title': 'Honeypot services', 'icon': 'sliders', 'route':
                    'config.services', 'entries': [{'title': 'Profile mgmt', 'icon': 'bookmark', 'route':
                    'honeypot.profiles'}]}]}]},
                {'title': 'Data processing', 'icon': 'exchange', 'route':
                    'config.data_processing'},
                {'title': 'Honeypot services', 'icon': 'sliders', 'route':
                    'config.services'}
            ]
        )
        correct_entries = {'entries': [{'title': 'Notif. services', 'route': 'config.notifications', 'entries': [{'title': 'Notif. services', 'route': 'config.notifications', 'entries': [{'title': 'Honeypot services', 'route': 'config.services', 'icon': 'sliders'}], 'icon': 'bell-o'}], 'icon': 'bell-o'}, {'route': 'config.data_processing', 'title': 'Data processing', 'icon': 'exchange'}, {'route': 'config.services', 'title': 'Honeypot services', 'icon': 'sliders'}], 'icon': 'cog', 'title': 'Configuration'}
        self.assertDictEqual(entries, correct_entries)


if __name__=='__main__':
    unittest.main()