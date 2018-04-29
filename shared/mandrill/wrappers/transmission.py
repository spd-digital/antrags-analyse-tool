import json

from shared.mandrill.wrappers.event import MandrillEventWrapper


class NoMandrillEventsKeyError(AssertionError):
    pass


class NotADictionaryError(AssertionError):
    pass


class MandrillTransmissionWrapper(object):
    def __init__(self, json_source):
        self.json_source = json_source

        self.events = extract_events(self.json_source)


def extract_events(json_source):
    if not isinstance(json_source, dict):
        raise NotADictionaryError(u'data must be a dictionary')
    if not 'mandrill_events' in json_source:
        raise NoMandrillEventsKeyError(u'data should contain a mandrill_events key')

    events_json = json.loads(json_source.get('mandrill_events'))
    
    events = []
    for event_json in events_json:
        mandrill_event = MandrillEventWrapper(event_json)
        events.append(mandrill_event)

    return events
