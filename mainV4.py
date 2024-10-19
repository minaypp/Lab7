import heapq
import random

class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.size += 1

    def remove(self, node):
        if node is None:
            return
        if node == self.head:
            self.head = node.next
        else:
            current = self.head
            while current.next != node:
                current = current.next
            current.next = node.next
        self.size -= 1

    def remove_head(self):
        if self.head is None:
            return None
        node = self.head
        self.head = self.head.next
        self.size -= 1
        return node.data

# Priority Queue class for storing passengers based on priority
class PriorityQueue:
    def __init__(self):
        self.queue = []

    def peek(self):
        if self.empty():
            return None
        return self.queue[0]

    def push(self, passenger):
        heapq.heappush(self.queue, passenger)

    def pop(self):
        return heapq.heappop(self.queue)

    def heapify(self):
        heapq.heapify(self.queue)

    def empty(self):
        return len(self.queue) == 0

    def remove(self, passenger):
        self.queue.remove(passenger)
        heapq.heapify(self.queue)

# Stack for emergency passengers
class Stack:
    def __init__(self):
        self.stack = LinkedList()

    def peek(self):
        if self.is_empty():
            return None
        return self.stack.head.data

    def push(self, item):
        self.stack.add(item)

    def pop(self):
        return self.stack.remove_head()

    def is_empty(self):
        return self.stack.size == 0

# Passenger Class
class Passenger:
    def __init__(self, start_station, destination_station, request_time, priority):
        self.start_station = start_station
        self.destination_station = destination_station
        self.request_time = request_time
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

# Train system simulation
class TrainSystem:
    def __init__(self, stations):
        self.stations = stations
        self.passengers = PriorityQueue()
        self.emergencies = Stack()
        self.current_time = 0
        self.train_location = self.stations[0]
        self.train_direction = 1  # 1 for forward, -1 for reverse
        self.carry_count = 0
        self.total_travel = 0

    def generate_new_passengers(self):
        # Generate passengers only at the current station
        destination_station = random.choice(self.stations)
        while destination_station == self.train_location:
            destination_station = random.choice(self.stations)

        priority = abs(self.stations.index(self.train_location) - self.stations.index(destination_station))

        new_passenger = Passenger(self.train_location, destination_station, self.current_time, priority)
        self.passengers.push(new_passenger)
        self.carry_count += 1
        print(f"New passenger from {self.train_location} to {destination_station} at time {self.current_time}")

    def generate_new_emergencies(self):
        destination_station = random.choice(self.stations)
        while destination_station == self.train_location:
            destination_station = random.choice(self.stations)

        new_emergency = Passenger(self.train_location, destination_station, self.current_time, priority=0)
        self.emergencies.push(new_emergency)
        self.carry_count += 1
        print(f"Emergency added for passenger from {self.train_location} to {destination_station} at time {self.current_time}")

    def drop_off_passenger(self, passenger):
        travel_time = self.current_time - passenger.request_time
        self.total_travel += travel_time
        print(f"Passenger dropped off at {self.train_location}, travel time: {travel_time}")
        self.passengers.remove(passenger)

    def drop_off_emergency(self, passengerNode):
        travel_time = self.current_time - passengerNode.data.request_time
        self.total_travel += travel_time
        print(f"Emergency dropped off at {self.train_location}, travel time: {travel_time}")
        self.emergencies.stack.remove(passengerNode)

    def determine_next_station(self):
        current_index = self.stations.index(self.train_location)

        # Prioritize emergencies first and determine destination
        if not self.emergencies.is_empty():
            emergency_passenger = self.emergencies.peek()
            self.train_direction = self.stations.index(emergency_passenger.destination_station) - current_index
            self.train_direction /= abs(self.train_direction)
            return self.stations[int(current_index + self.train_direction)]

        # Determine direction for queue next
        if not self.passengers.empty():
            next_passenger = self.passengers.peek()
            self.train_direction = self.stations.index(next_passenger.destination_station) - current_index
            self.train_direction /= abs(self.train_direction)
            return self.stations[int(current_index + self.train_direction)]

        # Default behavior if no passengers or emergencies: move to next adjacent station
        if current_index == 0:
            self.train_direction = 1  # Move forward
        elif current_index == len(self.stations) - 1:
            self.train_direction = -1  # Reverse direction
        return self.stations[current_index + self.train_direction]

    def cycle_at_station(self):
        print(f"Time: {self.current_time}, Current Station: {self.train_location}")

        # Pick up passengers from the current station
        self.generate_new_passengers()

        # Pick up emergencies
        self.generate_new_emergencies()

        # Drop off emergencies at the current station
        emergency = self.emergencies.stack.head
        while emergency:
            if emergency.data.destination_station == self.train_location:
                self.drop_off_emergency(emergency)
            if emergency:
                emergency = emergency.next


        while self.emergencies.peek().destination_station == self.train_location:
            self.drop_off_passenger(self.emergencies.peek())

        # Drop off passengers in the queue at the current station
        while self.passengers.peek().destination_station == self.train_location:
            self.drop_off_passenger(self.passengers.peek())

        # Recalculate priorities for onboard passengers
        for passenger in self.passengers.queue:
            passenger.priority = abs(self.stations.index(self.train_location) - self.stations.index(passenger.destination_station))

        self.passengers.heapify()

        # Determine the next station based on emergencies and priority
        next_station = self.determine_next_station()
        self.train_location = next_station

        self.current_time += 1  # Time increments after completing the cycle at the current station

    def calculate_average(self):
        return self.total_travel / self.carry_count if self.carry_count > 0 else 0

def main():
    stations = ['A', 'B', 'C', 'D']
    train_system = TrainSystem(stations)

    for _ in range(10):  # Simulate 10 cycles
        train_system.cycle_at_station()

    avg_travel_time = train_system.calculate_average()
    print(f"Average travel time: {avg_travel_time:.2f} minutes")

if __name__ == "__main__":
    main()
