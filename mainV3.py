import heapq
import random

class Node:
    def __init__(self, data, next):
        self.data = data
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = None

    def add(self, data, next):
        new_node = Node(data, next)
        if self.head is None:
            self.head = new_node
            self.size = 1
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
            while current.next is not node:
                current = current.next
            current.next = node.next
        self.size -= 1

    def remove_head(self):
        if self.head is None:
            return None
        return self.remove(self.head)

#Requirement 1 - Priority Queue class for storing passengers based on priority
class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, passenger):
        heapq.heappush(self.queue, passenger)

    def pop(self):
        return heapq.heappop(self.queue)

    def remove(self, passenger):
        if passenger in self.queue:
            self.queue.remove(passenger)
            self.queue.heapify()

    def heapify(self):
        heapq.heapify(self.queue)

    def empty(self):
        return len(self.queue) == 0

#Requirement 2 - Linked List stack
class Stack:
    def __init__(self):
        self.stack = LinkedList()

    def push(self, item):
        self.stack.add(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.stack.remove_head()

    def peek(self):
        if self.is_empty():
            return None
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0

#Requirement 4 - Passenger Class
class Passenger:
    def __init__(self, start_station, destination_station, request_time, priority):
        self.start_station =  start_station
        self.destination_station = destination_station
        self.request_time = request_time
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

#System to simulate a train
class TrainSystem():
    def __init__(self, stations):
        self.stations = stations
        self.passengers = PriorityQueue()
        self.emergencies = Stack()
        self.current_time = 0
        self.train_location = self.stations[0]
        self.CarryCount = 0
        self.totalTravel = 0

    #Generate new passengers and emergencies
    def generate_new_passengers(self):
        start_station = random.choice(self.stations)
        destination_station = random.choice(self.stations)
        priority = random.randint(1, 10)

        new_passenger = Passenger(start_station, destination_station, self.current_time, priority)
        self.passengers.push(new_passenger)
        self.CarryCount += 1
        print(f"New passenger from {start_station} to {destination_station} at time {self.current_time}")

    def generate_new_emergencies(self):
        start_station = random.choice(self.stations)
        destination_station = random.choice(self.stations)

        new_emergency = Passenger(start_station, destination_station, self.current_time, priority=0)
        self.emergencies.push(new_emergency)
        print(f"Emergency added for passenger from {start_station} to {destination_station} at time {self.current_time}")

    #Cycle for train at station
    def cycle_at_station(self):
        # Display the current time and placement
        print(f"Time: {self.current_time}, Current Station: {self.train_location}")

        # Generate new passengers and emergencies
        self.generate_new_passengers()
        self.generate_new_emergencies()

        # Process emergencies
        self.emergencies.heapify()
        while not self.emergencies.empty() and self.emergencies.peek().request_time <= self.current_time:
            self.process_emergency(self.emergencies.pop())

        # Process passengers
        self.passengers.heapify()
        while not self.passengers.empty() and self.passengers.peek().request_time <= self.current_time:
            self.process_passenger(self.passengers.pop())

        # Move to next station
        self.train_location = self.stations[(self.stations.index(self.train_location) + 1) % len(self.stations)]
        # Take off passengers
        # Calculate Priority and move to next station

    #Drop off a passenger
    def drop_off_passenger(self, passenger):
        self.totalTravel += self.calculate_traveltime(passenger)
        self.passengers.remove(passenger)

    def calculate_traveltime(self, p):
        return abs(self.current_time - self.p.request_time)

    def calculate_average(self):
        return self.totalTravel / self.CarryCount

def main():
    stations = ['A', 'B', 'C', 'D']
    train_system = TrainSystem(stations)

    for x in range(100):



main()


