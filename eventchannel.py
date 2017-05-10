
##################################################
## listens for events
##################################################
class EventChannelSub:
	def __init__(self, name):
		self.name = name
		
	def update(self, message):
		print('{} got message "{}"'.format(self.name, message))


##################################################
## publishes events to registered subs
##################################################
class EventChannelPub:
	def __init__(self, events):
		# maps event names to subscribers
		# str -> dict
		self.events = {event: dict() for event in events}

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
			callback(message)

##################################################
## pytest tests
##################################################
class SimpleSubscriber():
	def __init__(self, name):
		self.name = name

	def event_handler(self, message):
		self.last_message = message


class TestEventChannel():
	def test_create(self):
		ecp = EventChannelPub(['channel_one', 'channel_two'])
		ecs = EventChannelSub('sub_one')
		ecp.register('channel_one', ecs)

	def test_custom_subscriber(self):
		ecp = EventChannelPub(['channel_one', 'channel_two'])
		ecs = SimpleSubscriber('simple_sub')
		ecp.register('channel_one', ecs, ecs.event_handler)
		test_message = 'a test message'
		ecp.dispatch('channel_one', test_message)
		assert test_message == ecs.last_message
	
	def test_multi_sub(self):
		ecp = EventChannelPub(['foo'])
		ecs1 = SimpleSubscriber('ecs1')
		ecp.register('foo', ecs1, ecs1.event_handler)
		ecs2 = SimpleSubscriber('ecs2')
		ecp.register('foo', ecs2, ecs2.event_handler)
		test_message = 'a test message'
		ecp.dispatch('foo', test_message)
		assert test_message == ecs1.last_message
		assert test_message == ecs2.last_message


##################################################
## standalone
##################################################
def main():
	t = TestEventChannel()
	t.test_custom_subscriber()
	

if __name__ == '__main__':
	main()
