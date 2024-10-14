import heapq

# Constants
STATIONS = ['A', 'B', 'C', 'D']
STATION_INDICES = {station: index for index, station in enumerate(STATIONS)}

class Passenger:
    def __init__(self, start_station, destination_station, request_time):
        self.start_station = start_station
        self.destination_station = destination_station
        self.request_time = request_time
        self.priority = None  # Will be calculated
        self.arrival_time = None  # Time when the passenger reaches the destination

    def __lt__(self, other):
        return self.priority < other.priority

class Emergency(Passenger):
    pass

class EmergencyStack:
    def __init__(self):
        self.top = None

    def push(self, emergency):
        self.top = EmergencyStackNode(emergency, self.top)

    def pop(self):
        if self.top is None:
            return None
        emergency = self.top.emergency
        self.top = self.top.next_node
        return emergency

    def is_empty(self):
        return self.top is None

class EmergencyStackNode:
    def __init__(self, emergency, next_node=None):
        self.emergency = emergency
        self.next_node = next_node

def main_menu():
    passenger_requests = []
    emergency_stack = EmergencyStack()
    all_passengers = []

    while True:
        print("\nSelect an option:")
        print("1. Add Passenger Request")
        print("2. Add Emergency Request")
        print("3. Process Requests")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            passenger = add_passenger_request()
            if passenger:
                all_passengers.append(passenger)
                passenger_requests.append(passenger)
        elif choice == '2':
            emergency = add_emergency_request()
            if emergency:
                all_passengers.append(emergency)
                emergency_stack.push(emergency)
        elif choice == '3':
            process_requests(passenger_requests, emergency_stack, all_passengers)
            break
        elif choice == '4':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Try again.")

def add_passenger_request():
    request_time = int(input("Enter request time (>= 0): "))
    start_station = input("Enter start station (A-D): ").upper()
    destination_station = input("Enter destination station (A-D): ").upper()

    if start_station == destination_station:
        print("Start and destination cannot be the same.")
        return None

    return Passenger(start_station, destination_station, request_time)

def add_emergency_request():
    request_time = int(input("Enter request time (>= 0): "))
    start_station = input("Enter start station (A-D): ").upper()
    destination_station = input("Enter destination station (A-D): ").upper()

    if start_station == destination_station:
        print("Start and destination cannot be the same.")
        return None

    return Emergency(start_station, destination_station, request_time)

def process_requests(passenger_requests, emergency_stack, all_passengers):
    current_time = 0
    train_station = 'A'
    print(f"Train starts at {train_station} at time {current_time}.")

    passenger_requests.sort(key=lambda p: p.request_time)
    passenger_queue = []
    passenger_index = 0
    total_passengers = len(passenger_requests)

    while (not emergency_stack.is_empty() or passenger_queue 
           or passenger_index < total_passengers):
        
        while not emergency_stack.is_empty() and emergency_stack.top.emergency.request_time <= current_time:
            emergency = emergency_stack.pop()
            travel_and_handle(train_station, emergency, current_time, True)
            train_station = emergency.destination_station

        while (passenger_index < total_passengers and 
               passenger_requests[passenger_index].request_time <= current_time):
            passenger = passenger_requests[passenger_index]
            passenger.priority = calculate_priority(train_station, passenger.destination_station)
            heapq.heappush(passenger_queue, passenger)
            passenger_index += 1

        if passenger_queue:
            passenger = heapq.heappop(passenger_queue)
            travel_and_handle(train_station, passenger, current_time, False)
            train_station = passenger.destination_station

        else:
            next_event_time = find_next_event_time(emergency_stack, passenger_requests, passenger_index)
            if next_event_time > current_time:
                print(f"Advancing time to {next_event_time}.")
                current_time = next_event_time

    calculate_average_travel_time(all_passengers)

def travel_and_handle(train_station, passenger, current_time, is_emergency):
    travel_time = calculate_travel_time(train_station, passenger.start_station)
    current_time += travel_time
    print(f"Moved to {passenger.start_station} in {travel_time} units.")

    travel_time = calculate_travel_time(passenger.start_station, passenger.destination_station)
    current_time += travel_time
    passenger.arrival_time = current_time
    print(f"{'Emergency' if is_emergency else 'Passenger'} from {passenger.start_station} to {passenger.destination_station} handled at time {current_time}.")

def find_next_event_time(emergency_stack, passenger_requests, passenger_index):
    next_times = []
    if not emergency_stack.is_empty():
        next_times.append(emergency_stack.top.emergency.request_time)
    if passenger_index < len(passenger_requests):
        next_times.append(passenger_requests[passenger_index].request_time)
    return min(next_times) if next_times else float('inf')

def calculate_travel_time(station_a, station_b):
    return abs(STATION_INDICES[station_a] - STATION_INDICES[station_b])

def calculate_priority(current_station, destination_station):
    return calculate_travel_time(current_station, destination_station)

def calculate_average_travel_time(passengers):
    total_wait_time = sum([p.arrival_time - p.request_time for p in passengers])
    average_time = total_wait_time / len(passengers) if passengers else 0
    print(f"Average travel time: {average_time:.2f} units.")

if __name__ == "__main__":
    main_menu()
