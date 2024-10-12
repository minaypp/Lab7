import heapq

# Passenger class with comparison methods
class Passenger:
    def __init__(self, start_station, destination_station, request_time):
        self.start_station = start_station
        self.destination_station = destination_station
        self.request_time = request_time
        self.priority = self.calculate_initial_priority()
    
    def calculate_initial_priority(self):
        station_positions = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        # Initial priority based on distance from start to destination
        distance = abs(station_positions[self.start_station] - station_positions[self.destination_station])
        return distance  # Smaller distance, higher priority (lower numerical value)
    
    def __lt__(self, other):
        # First compare priorities
        if self.priority != other.priority:
            return self.priority < other.priority
        # If priorities are equal, compare request times
        return self.request_time < other.request_time
    
    def __eq__(self, other):
        return (self.priority, self.request_time) == (other.priority, other.request_time)

# Emergency stack implemented using a linked list
class EmergencyNode:
    def __init__(self, passenger, next_node=None):
        self.passenger = passenger
        self.next_node = next_node

class EmergencyStack:
    def __init__(self):
        self.top = None
    
    def push(self, passenger):
        new_node = EmergencyNode(passenger, self.top)
        self.top = new_node
    
    def pop(self):
        if self.top is None:
            return None
        passenger = self.top.passenger
        self.top = self.top.next_node
        return passenger
    
    def is_empty(self):
        return self.top is None

# Priority queue for passengers
passenger_queue = []

def add_passenger(passenger):
    heapq.heappush(passenger_queue, passenger)

def calculate_priority(current_station, destination_station):
    station_positions = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    distance = abs(station_positions[current_station] - station_positions[destination_station])
    return distance  # Smaller distance means higher priority

def recalculate_priorities(current_station):
    global passenger_queue
    temp_passengers = []
    
    # Remove all passengers from the heap
    while passenger_queue:
        passenger = heapq.heappop(passenger_queue)
        # Recalculate priority based on current station
        passenger.priority = calculate_priority(current_station, passenger.destination_station)
        temp_passengers.append(passenger)
    
    # Rebuild the heap with updated priorities
    for passenger in temp_passengers:
        heapq.heappush(passenger_queue, passenger)

def calculate_travel_time(start_station, destination_station):
    station_positions = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    return abs(station_positions[start_station] - station_positions[destination_station])

def train_system():
    current_station = 'A'  # Starting station
    total_time = 0
    passenger_count = 0
    
    while passenger_queue or not emergency_stack.is_empty():
        # Handle emergencies first
        if not emergency_stack.is_empty():
            passenger = emergency_stack.pop()
            print(f"Handling emergency for passenger from {passenger.start_station} to {passenger.destination_station}")
            # Assume immediate processing
            travel_time = calculate_travel_time(current_station, passenger.destination_station)
            total_time += travel_time
            passenger_count += 1
            current_station = passenger.destination_station
        else:
            passenger = heapq.heappop(passenger_queue)
            print(f"Processing passenger from {passenger.start_station} to {passenger.destination_station} at station {current_station}")
            travel_time = calculate_travel_time(current_station, passenger.destination_station)
            total_time += travel_time
            passenger_count += 1
            current_station = passenger.destination_station
            # Recalculate priorities after each trip
            recalculate_priorities(current_station)
    
    average_time = total_time / passenger_count if passenger_count else 0
    print(f"Average travel time per passenger: {average_time}")

# Initialize the emergency stack
emergency_stack = EmergencyStack()

# Adding passengers
add_passenger(Passenger('A', 'C', request_time=1))
add_passenger(Passenger('B', 'D', request_time=2))
add_passenger(Passenger('C', 'A', request_time=3))

# Simulating an emergency
emergency_stack.push(Passenger('D', 'A', request_time=4))

# Running the train system
train_system()
