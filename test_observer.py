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
		
	def register(self, event: str, who: object, callback=None) -> None:
		""" subscribe to events here
		
		:param event: the name of the even caller is interested in
		:param who: instance of a class that will be called when the event fires
		:param callback: method called defaults to update()
		:return: None
		"""
		if callback is None:
			callback = getattr(who, 'update')
		self.get_subscribers(event)[who] = callback
		
	def unregister(self, event: str, who: object) -> None:
		""" removes a subscriber
		
		:param event: the event subscribed to
		:param who: the subscriber
		:return: None
		"""
		del self.get_subscribers(event)[who]
		
	def dispatch(self, event: str, message: str) -> None:
		""" send message to all subscribers of event
		
		:param event: the event
		:param message: the message to send
		:return: None
		"""
		for subscriber, callback in self.get_subscribers(event).items():
			callback(event, message)
			
	def broadcast(self, message: str) -> int:
		""" send specified message to all subscribers
		
		:param message: the message to send
		:return: the number of distinct subscribers that got a messsage
		"""
		subs_notified_so_far = []
		receiver_count = 0
		for event in self.events:
			for subscriber, callback in self.get_subscribers(event).items():
				if subscriber not in subs_notified_so_far:
					callback("broadcast", message)
					subs_notified_so_far.append(subscriber)
					receiver_count += 1
		return receiver_count


class TestObserver():
	def __init__(self, name):
		self.name = name
		self.message_history = []

	def update(self, event: str, message: str) -> None:
		self.message_history.append(message)


def test_broadcast(capsys):
	ep = EventPublisher(["One", "Two", "Three"])
	s1 = TestObserver("s1")
	s2 = TestObserver("s2")
	ep.register("One", s1)
	ep.register("Two", s1)
	ep.register("Three", s1)
	ep.register("Three", s2)
	receiver_count = ep.broadcast("Hello")
	assert receiver_count == 2
	assert len(s1.message_history) == 1
	assert len(s2.message_history) == 1
	assert "Hello" in s1.message_history
	assert len(s2.message_history) == 1
	assert "Hello" in s2.message_history

	
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

