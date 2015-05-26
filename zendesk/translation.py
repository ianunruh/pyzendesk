from zendesk import resources

SINGULAR_NOUN_MAP = {
    'group': resources.Group,
    'organization': resources.Organization,
    'ticket': resources.Ticket,
    'user': resources.User,
}

def map_result_type(client, data):
    return SINGULAR_NOUN_MAP[data['result_type']](client, data)

PLURAL_NOUN_MAP = {
    'audits': resources.TicketAudit,
    'comments': resources.TicketComment,
    'groups': resources.Group,
    'organizations': resources.Organization,
    'results': map_result_type,
    'tickets': resources.Ticket,
    'users': resources.User,
}

def map_single(noun):
    def outer(func):
        def inner(client, *args, **kwargs):
            data = func(client, *args, **kwargs)
            return SINGULAR_NOUN_MAP[noun](client, data[noun])

        return inner

    return outer

def map_paged(noun):
    def outer(func):
        def inner(client, *args, **kwargs):
            for page in func(client, *args, **kwargs):
                for data in page[noun]:
                    yield PLURAL_NOUN_MAP[noun](client, data)

        return inner

    return outer

__ALL__ = ['map_single', 'map_paged']
