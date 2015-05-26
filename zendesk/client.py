import logging
import time

import requests

from zendesk import exceptions
from zendesk.translation import *

LOG = logging.getLogger('zendesk')

class Client(object):
    def __init__(self, url, username, password, session=None):
        if not session:
            session = requests.Session()

        self.session = session
        self.session.auth = (username, password)

        self.url = url

    @map_paged('results')
    def search(self, query, sort_by=None, sort_order=None):
        params = {
            'query': query,
            'sort_by': sort_by,
            'sort_order': sort_order,
        }

        return self.fetch_paged('/api/v2/search.json', params=params)

    def find(self, *args, **kwargs):
        last_result = None
        for result in self.search(*args, **kwargs):
            if last_result:
                raise exceptions.MultipleResulsts()

            last_result = result

        return last_result

    @map_single('organization')
    def organization(self, id):
        return self.get('/api/v2/organizations/{}.json'.format(id)).json()

    @property
    @map_paged('organizations')
    def organizations(self):
        return self.fetch_paged('/api/v2/organizations.json')

    def add_tags_to_ticket(self, id, *tags):
        params = {
            'tags': tags,
        }

        self.put('/api/v2/tickets/{}/tags.json'.format(id), json=params)
        
    def set_tags_on_ticket(self, id, *tags):
        params = {
            'tags': tags,
        }

        self.post('/api/v2/tickets/{}/tags.json'.format(id), json=params)
        
    def remove_tags_from_ticket(self, id, *tags):
        params = {
            'tags': tags,
        }

        self.delete('/api/v2/tickets/{}/tags.json'.format(id), json=params)

    @map_single('ticket')
    def ticket(self, id):
        return self.get('/api/v2/tickets/{}.json'.format(id)).json()

    @property
    @map_paged('tickets')
    def tickets(self):
        return self.fetch_paged('/api/v2/tickets.json')

    @property
    @map_paged('tickets')
    def recent_tickets(self):
        return self.fetch_paged('/api/v2/tickets/recent.json')

    @map_paged('tickets')
    def organization_tickets(self, id):
        return self.fetch_paged('/api/v2/organizations/{}/tickets.json'.format(id))

    @map_single('ticket')
    def create_ticket(self, **kwargs):
        params = {
            'ticket': kwargs,
        }

        return self.post('/api/v2/tickets.json', json=params).json()

    @map_single('ticket')
    def update_ticket(self, id, **kwargs):
        params = {
            'ticket': kwargs,
        }

        return self.put('/api/v2/tickets/{}.json'.format(id), json=params).json()

    def delete_ticket(self, id):
        return self.delete('/api/v2/tickets/{}.json'.format(id))

    @map_paged('comments')
    def ticket_comments(self, id):
        return self.fetch_paged('/api/v2/tickets/{}/comments.json'.format(id))

    @map_single('upload')
    def upload_attachment(self, filename, stream, token=None):
        params = {
            'filename': filename,
            'token': token,
        }

        return self.post('/api/v2/uploads.json', params=params, data=stream).json()

    @property
    @map_single('user')
    def current_user(self):
        return self.get('/api/v2/users/me.json').json()

    @map_single('user')
    def user(self, id):
        return self.get('/api/v2/users/{}.json'.format(id)).json()

    @property
    @map_paged('users')
    def users(self):
        return self.fetch_paged('/api/v2/users.json')

    @map_paged('users')
    def group_users(self, id):
        return self.fetch_paged('/api/v2/groups/{}/users.json'.format(id))

    @map_paged('users')
    def organization_users(self, id):
        return self.fetch_paged('/api/v2/organizations/{}/users.json'.format(id))

    def fetch_paged(self, url, params=None, **kwargs):
        if not params:
            params = {}

        params['page'] = 1
        params['per_page'] = 100

        while True:
            data = self.get(url, params=params, **kwargs).json()
            yield data

            if not data['next_page']:
                return

            params['page'] += 1

    def get(self, url, **kwargs):
        return self.__request('get', url, **kwargs)

    def post(self, url, **kwargs):
        return self.__request('post', url, **kwargs)

    def put(self, url, **kwargs):
        return self.__request('put', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.__request('delete', url, **kwargs)

    def __request(self, method, url, **kwargs):
        while True:
            response = self.session.request(method, self.url + url, **kwargs)
            if response.status_code == 429:
                retry_after = int(response.headers['Retry-After'])

                LOG.debug('Rate limit exceeded, retrying after %s seconds', retry_after)
                time.sleep(retry_after)

                continue

            response.raise_for_status()

            return response
