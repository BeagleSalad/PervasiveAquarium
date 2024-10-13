import paho.mqtt.client as mqtt

class Node:
    def __init__(self, node_id, broker_address='localhost', broker_port=1883):
        self.node_id = node_id
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client = mqtt.Client(client_id=self.node_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.callbacks = {}

    def on_connect(self, client, userdata, flags, rc):
        print(f"[{self.node_id}] Connected to broker with result code {rc}")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode('utf-8')
        print(f"[{self.node_id}] Received message on topic '{topic}': {payload}")

        # Call registered callback if available
        if topic in self.callbacks:
            self.callbacks[topic](payload)

    def connect(self):
        self.client.connect(self.broker_address, self.broker_port)
        self.client.loop_start()  # Start the loop in a background thread

    def send_unicast(self, target_node_id, message):
        topic = f'unicast/{target_node_id}'
        self.client.publish(topic, message)
        print(f"[{self.node_id}] Sent unicast message to '{target_node_id}': {message}")

    def send_multicast(self, topic, message):
        multicast_topic = f'multicast/{topic}'
        self.client.publish(multicast_topic, message)
        print(f"[{self.node_id}] Sent multicast message on '{multicast_topic}': {message}")

    def subscribe(self, topic, callback=None):
        self.client.subscribe(topic)
        print(f"[{self.node_id}] Subscribed to topic '{topic}'")

        if callback:
            self.callbacks[topic] = callback

    def receive(self, topic, callback):
        self.subscribe(topic, callback)

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        print(f"[{self.node_id}] Disconnected from broker.")

# Example usage:
if __name__ == "__main__":
    # Create two nodes
    node1 = Node("node1")
    node2 = Node("node2")

    # Connect nodes to the broker
    node1.connect()
    node2.connect()

    # Set up receive callbacks
    node1.receive("unicast/node1", lambda msg: print(f"Node1 received unicast: {msg}"))
    node2.receive("unicast/node2", lambda msg: print(f"Node2 received unicast: {msg}"))

    node1.receive("multicast/general", lambda msg: print(f"Node1 received multicast: {msg}"))
    node2.receive("multicast/general", lambda msg: print(f"Node2 received multicast: {msg}"))

    # Send messages
    node1.send_unicast("node2", "Hello from Node 1!")
    node2.send_unicast("node1", "Hello from Node 2!")

    node1.send_multicast("general", "This is a multicast message!")

    # Allow time for messages to be sent and received
    import time
    time.sleep(2)

    # Stop nodes
    node1.stop()
    node2.stop()