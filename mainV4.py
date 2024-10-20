import heapq  # Import heapq for priority queue implementation
import random  # Import random for generating random destinations

# Node class for the linked list implementation
class Node:
    def __init__(self, data, next=None):
        self.data = data  # Store data (Passenger object)
        self.next = next  # Pointer to the next node

# LinkedList class to implement stack functionality for emergencies
class LinkedList:
    def __init__(self):
        self.head = None  # Initialize the head of the list
        self.size = 0     # Keep track of the size of the list

    def add(self, data):
        # Add a new node with the given data to the end of the list
        new_node = Node(data)
        if self.head is None:
            self.head = new_node  # If list is empty, new node is the head
        else:
            current = self.head
            while current.next is not None:
                current = current.next  # Traverse to the end of the list
            current.next = new_node  # Append the new node
        self.size += 1  # Increment the size of the list

    def remove(self, node):
        # Remove the given node from the list
        if node is None:
            return
        if node == self.head:
            self.head = node.next  # If node is head, update head
        else:
            current = self.head
            while current.next != node:
                current = current.next  # Find the node before the one to remove
            current.next = node.next  # Bypass the node to remove
        self.size -= 1  # Decrement the size of the list

    def remove_head(self):
        # Remove and return the data from the head node
        if self.head is None:
            return None
        node = self.head
        self.head = self.head.next  # Update head to the next node
        self.size -= 1  # Decrement the size of the list
        return node.data  # Return the data from the removed node

# Priority Queue class for storing passengers based on priority
class PriorityQueue:
    def __init__(self):
        self.queue = []  # Initialize an empty list to store the heap

    def peek(self):
        # Return the passenger with the highest priority without removing it
        if self.empty():
            return None
        return self.queue[0]  # The root of the heap has the highest priority

    def push(self, passenger):
        # Add a passenger to the priority queue
        heapq.heappush(self.queue, passenger)  # Use heapq to maintain heap property

    def pop(self):
        # Remove and return the passenger with the highest priority
        return heapq.heappop(self.queue)

    def heapify(self):
        # Rebuild the heap (useful after updating priorities)
        heapq.heapify(self.queue)

    def empty(self):
        # Check if the priority queue is empty
        return len(self.queue) == 0

    def remove(self, passenger):
        # Remove a specific passenger from the queue
        self.queue.remove(passenger)  # Remove passenger
        heapq.heapify(self.queue)     # Rebuild the heap to maintain heap property

# Stack class for storing emergency passengers
class Stack:
    def __init__(self):
        self.stack = LinkedList()  # Use LinkedList to implement the stack

    def peek(self):
        # Return the passenger on top of the stack without removing it
        if self.is_empty():
            return None
        return self.stack.head.data  # The head of the linked list is the top of the stack

    def push(self, item):
        # Push a new passenger onto the stack
        self.stack.add(item)

    def pop(self):
        # Pop the top passenger from the stack and return it
        return self.stack.remove_head()

    def is_empty(self):
        # Check if the stack is empty
        return self.stack.size == 0

# Passenger class representing a passenger in the train system
class Passenger:
    def __init__(self, start_station, destination_station, request_time, priority):
        self.start_station = start_station
        self.destination_station = destination_station
        self.request_time = request_time  # The time when the passenger requested the ride
        self.priority = priority          # The priority of the passenger (lower value means higher priority)

    def __lt__(self, other):
        # Less than operator for comparing passengers based on priority
        return self.priority < other.priority

# TrainSystem class to simulate the train operations
class TrainSystem:
    def __init__(self, stations):
        self.stations = stations                    # List of stations in the train system
        self.passengers = PriorityQueue()           # Priority queue for regular passengers
        self.emergencies = Stack()                  # Stack for emergency passengers
        self.current_time = 0                       # Simulation current time
        self.train_location = self.stations[0]      # Train starts at the first station
        self.train_direction = 1                    # Direction the train is moving (1 for forward, -1 for reverse)
        self.carry_count = 0                        # Total number of passengers carried
        self.total_travel = 0                       # Total travel time of all passengers

    def generate_new_passengers(self):
        # Generate a new passenger at the current station with a random destination
        destination_station = random.choice(self.stations)
        while destination_station == self.train_location:
            # Ensure the destination is not the current station
            destination_station = random.choice(self.stations)

        # Priority is determined by the distance between stations
        priority = abs(self.stations.index(self.train_location) - self.stations.index(destination_station))

        # Create a new passenger
        new_passenger = Passenger(self.train_location, destination_station, self.current_time, priority)
        self.passengers.push(new_passenger)  # Add the passenger to the priority queue
        self.carry_count += 1  # Increment the carry count
        print(f"New passenger from {self.train_location} to {destination_station} at time {self.current_time}")

    def generate_new_emergencies(self):
        # Generate a new emergency passenger at the current station
        destination_station = random.choice(self.stations)
        while destination_station == self.train_location:
            # Ensure the destination is not the current station
            destination_station = random.choice(self.stations)

        # Emergency passengers have the highest priority (priority=0)
        new_emergency = Passenger(self.train_location, destination_station, self.current_time, priority=0)
        self.emergencies.push(new_emergency)  # Add the emergency passenger to the stack
        self.carry_count += 1  # Increment the carry count
        print(f"Emergency added for passenger from {self.train_location} to {destination_station} at time {self.current_time}")

    def drop_off_passenger(self, passenger):
        # Drop off a regular passenger at the current station
        travel_time = self.current_time - passenger.request_time  # Calculate travel time
        self.total_travel += travel_time  # Add to total travel time
        print(f"Passenger dropped off at {self.train_location}, travel time: {travel_time}")
        self.passengers.remove(passenger)  # Remove passenger from the priority queue

    def drop_off_emergency(self, passenger_node):
        # Drop off an emergency passenger at the current station
        travel_time = self.current_time - passenger_node.data.request_time  # Calculate travel time
        self.total_travel += travel_time  # Add to total travel time
        print(f"Emergency dropped off at {self.train_location}, travel time: {travel_time}")
        self.emergencies.stack.remove(passenger_node)  # Remove passenger node from the linked list stack

    def determine_next_station(self):
        # Determine the next station the train should go to
        current_index = self.stations.index(self.train_location)  # Get current station index

        # Prioritize emergencies first
        if not self.emergencies.is_empty():
            emergency_passenger = self.emergencies.peek()
            destination_index = self.stations.index(emergency_passenger.destination_station)
            # Determine direction towards the emergency passenger's destination
            self.train_direction = destination_index - current_index
            self.train_direction /= abs(self.train_direction)  # Normalize to -1 or 1
            return self.stations[int(current_index + self.train_direction)]

        # Next, consider regular passengers
        if not self.passengers.empty():
            next_passenger = self.passengers.peek()
            destination_index = self.stations.index(next_passenger.destination_station)
            # Determine direction towards the passenger's destination
            self.train_direction = destination_index - current_index
            self.train_direction /= abs(self.train_direction)  # Normalize to -1 or 1
            return self.stations[int(current_index + self.train_direction)]

        # If no passengers, move to the next station in current direction
        if current_index == 0:
            self.train_direction = 1  # Move forward if at the first station
        elif current_index == len(self.stations) - 1:
            self.train_direction = -1  # Reverse direction if at the last station
        return self.stations[int(current_index + self.train_direction)]

    def cycle_at_station(self):
        # Simulate the train's actions at the current station
        print(f"Time: {self.current_time}, Current Station: {self.train_location}")

        # Generate new passengers and emergencies at the current station
        self.generate_new_passengers()
        self.generate_new_emergencies()

        # Drop off emergency passengers at the current station
        emergency_node = self.emergencies.stack.head
        while emergency_node:
            next_node = emergency_node.next  # Keep track of next node before potentially removing current
            if emergency_node.data.destination_station == self.train_location:
                self.drop_off_emergency(emergency_node)
            emergency_node = next_node  # Move to the next node

        # Drop off regular passengers at the current station
        while not self.passengers.empty() and self.passengers.peek().destination_station == self.train_location:
            self.drop_off_passenger(self.passengers.peek())

        # Recalculate priorities for onboard passengers based on the new train location
        for passenger in self.passengers.queue:
            passenger.priority = abs(self.stations.index(self.train_location) - self.stations.index(passenger.destination_station))
        self.passengers.heapify()  # Rebuild the heap after updating priorities

        # Determine the next station to move to
        next_station = self.determine_next_station()
        self.train_location = next_station  # Update train location

        self.current_time += 1  # Increment simulation time

    def calculate_average(self):
        # Calculate average travel time of all passengers
        return self.total_travel / self.carry_count if self.carry_count > 0 else 0

def main():
    stations = ['A', 'B', 'C', 'D']  # Define the list of stations
    train_system = TrainSystem(stations)  # Initialize the train system

    for _ in range(10):  # Simulate 10 time cycles
        train_system.cycle_at_station()

    avg_travel_time = train_system.calculate_average()
    print(f"Average travel time: {avg_travel_time:.2f} minutes")

if __name__ == "__main__":
    main()
