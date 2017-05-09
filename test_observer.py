import pytest


class EventSubscriber:
    def __init__(self, name):
        self.name = name

    def update(self, event, message):
        print('sub=[{}] event=[{}] message=[{}]'.format(self.name, event, message))


class EventPublisher:
    def __init__(self, events):
        # maps event names to subscribers
        # str -> dict
        self.events = {event: dict()
                       for event in events}

    def get_subscribers(self, event):
        return self.events[event]

    def register(self, event, who, callback=None):
        if callback is None:
            callback = getattr(who, 'update')
        self.get_subscribers(event)[who] = callback

    def unregister(self, event, who):
        del self.get_subscribers(event)[who]

    def dispatch(self, event, message):
        for subscriber, callback in self.get_subscribers(event).items():
            callback(event, message)

    def broadcast(self, message):
        for event in self.events:
            self.dispatch(event, message)


def test_broadcast(capsys):
    ep = EventPublisher(["One", "Two", "Three"])
    s1 = EventSubscriber("s1")
    ep.register("One", s1)
    ep.register("Two", s1)
    ep.register("Three", s1)
    ep.broadcast("Hello")
    out, err = capsys.readouterr()
    assert out == "sub=[s1] event=[One] message=[Hello]\n"\
                  "sub=[s1] event=[Two] message=[Hello]\n"\
                  "sub=[s1] event=[Three] message=[Hello]\n"


def test_single_pub_single_sub_subscriber(capsys):
    ep = EventPublisher(["EventOne"])
    s1 = EventSubscriber("s1")
    ep.register("EventOne", s1)
    ep.dispatch("EventOne", "Hello")
    out, err = capsys.readouterr()
    assert out == "sub=[s1] event=[EventOne] message=[Hello]\n"


def test_single_pub_multi_sub_subscriber(capsys):
    ep = EventPublisher(["EventOne"])
    s1 = EventSubscriber("s1")
    s2 = EventSubscriber("s2")
    ep.register("EventOne", s1)
    ep.register("EventOne", s2)
    ep.dispatch("EventOne", "Hello")
    out, err = capsys.readouterr()
    assert out == "sub=[s2] event=[EventOne] message=[Hello]\nsub=[s1] event=[EventOne] message=[Hello]\n"


def test_multi_pub_single_sub(capsys):
    ep1 = EventPublisher(["EventOne"])
    ep2 = EventPublisher(["EventTwo"])
    sp1 = EventSubscriber("s1")
    ep1.register("EventOne", sp1)
    ep2.register("EventTwo", sp1)
    ep1.dispatch("EventOne", "Hello")
    ep2.dispatch("EventTwo", "Hello")
    out, err = capsys.readouterr()
    assert out == "sub=[s1] event=[EventOne] message=[Hello]\nsub=[s1] event=[EventTwo] message=[Hello]\n"
