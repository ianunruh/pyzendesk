import six

class Resource(object):
    def __init__(self, client, data):
        self._client = client
        self._data = data

        for k, v in six.iteritems(data):
            setattr(self, k, v)

    def to_dict(self):
        return self._data

class Group(Resource):
    @property
    def users(self):
        return self._client.group_users(self.id)

class Organization(Resource):
    @property
    def users(self):
        return self._client.organization_users(self.id)

class Ticket(Resource):
    @property
    def requester(self):
        return self._client.user(self.requester_id)

    @property
    def submitter(self):
        if self.submitter_id:
            return self._client.user(self.submitter_id)

    @property
    def assignee(self):
        if self.assignee_id:
            return self._client.user(self.assignee_id)

    @property
    def group(self):
        if self.group_id:
            return self._client.group(self.group_id)

    @property
    def organization(self):
        if self.organization_id:
            return self._client.organization(self.organization_id)

    @property
    def comments(self):
        return self._client.ticket_comments(self.id)

    @property
    def collaborators(self):
        return [self._client.user(collaborator_id) for collaborator_id in self.collaborator_ids]

    @property
    def problem(self):
        if self.problem_id:
            return self._client.ticket(self.problem_id)

    def add_tags(self, *tags):
        self._client.add_tags_to_ticket(self.id, *tags)

    def remove_tags(self, *tags):
        self._client.remove_tags_from_ticket(self.id, *tags)

    def update(self, **kwargs):
        self._client.update_ticket(self.id, **kwargs)

    def delete(self):
        self._client.delete_ticket(self.id)

class TicketComment(Resource):
    @property
    def author(self):
        return self._client.user(self.author_id)

class Upload(Resource):
    pass

class User(Resource):
    @property
    def organization(self):
        if self.organization_id:
            return self._client.organization(self.organization_id)
