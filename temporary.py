import heapq

# Constants
STATIONS = ['A', 'B', 'C', 'D']

# Mapping station names to indices for easy distance calculation
STATION_INDICES = {station: index for index, station in enumerate(STATIONS)}

class Passenger:
    def __init__(self, start_station, destination_station, request_time):
        self.start_station = start_station
        self.destination_station = destination_station
        self.request_time = request_time
        self.priority = None  # Will be calculated based on current train station
        self.arrival_time = None  # Time when the passenger reaches the destination

    def __lt__(self, other):
        return self.priority < other.priority

class Emergency(Passenger):
    pass  # Inherits all attributes; can add more if needed

class EmergencyStackNode:
    def __init__(self, emergency, next_node=None):
        self.emergency = emergency
        self.next_node = next_node

class EmergencyStack:
    def __init__(self):
        self.top = None

    def push(self, emergency):
        new_node = EmergencyStackNode(emergency, self.top)
        self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        emergency = self.top.emergency
        self.top = self.top.next_node
        return emergency

    def is_empty(self):
        return self.top is None

def main_menu():
    passenger_requests = []
    emergency_stack = EmergencyStack()
    all_passengers = []  # Keep track of all passengers for wait time calculation

    while True:
        print("\nPlease select an option:")
        print("1. Add Passenger Request")
        print("2. Add Emergency Request")
        print("3. Process All Requests")
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
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

def add_passenger_request():
    print("\n--- Add Passenger Request ---")
    try:
        request_time = int(input("Enter request time (integer >= 0): "))
        if request_time < 0:
            print("Request time cannot be negative.")
            return None
    except ValueError:
        print("Invalid input. Please enter a valid integer for time.")
        return None

    start_station = input("Enter start station (A, B, C, D): ").upper()
    if start_station not in STATIONS:
        print("Invalid start station.")
        return None

    destination_station = input("Enter destination station (A, B, C, D): ").upper()
    if destination_station not in STATIONS:
        print("Invalid destination station.")
        return None

    if start_station == destination_station:
        print("Start station and destination station cannot be the same.")
        return None

    passenger = Passenger(start_station, destination_station, request_time)
    print("Passenger request added successfully!")
    return passenger

def add_emergency_request():
    print("\n--- Add Emergency Request ---")
    try:
        request_time = int(input("Enter request time (integer >= 0): "))
        if request_time < 0:
            print("Request time cannot be negative.")
            return None
    except ValueError:
        print("Invalid input. Please enter a valid integer for time.")
        return None

    start_station = input("Enter start station (A, B, C, D): ").upper()
    if start_station not in STATIONS:
        print("Invalid start station.")
        return None

    destination_station = input("Enter destination station (A, B, C, D): ").upper()
    if destination_station not in STATIONS:
        print("Invalid destination station.")
        return None

    if start_station == destination_station:
        print("Start station and destination station cannot be the same.")
        return None

    emergency = Emergency(start_station, destination_station, request_time)
    print("Emergency request added successfully!")
    return emergency

def process_requests(passenger_requests, emergency_stack, all_passengers):
    print("\nProcessing all requests...")
    current_time = 0
    train_station = 'A'  # Train starts at Station A

    # Sort passenger requests based on request time
    passenger_requests.sort(key=lambda p: p.request_time)

    # Initialize the priority queue
    passenger_queue = []

    # Index to keep track of which passengers have been added to the queue
    passenger_index = 0
    total_passengers = len(passenger_requests)

    while not emergency_stack.is_empty() or passenger_queue or passenger_index < total_passengers:
        # Handle emergencies first
        while not emergency_stack.is_empty():
            emergency = emergency_stack.pop()
            # Move train to emergency's start station
            travel_time = calculate_travel_time(train_station, emergency.start_station)
            current_time += travel_time
            train_station = emergency.start_station
            print(f"\nHandling emergency from {emergency.start_station} to {emergency.destination_station}.")
            print(f"Train moved to {train_station} in {travel_time} time units.")
            # Move train to emergency's destination station
            travel_time = calculate_travel_time(train_station, emergency.destination_station)
            current_time += travel_time
            train_station = emergency.destination_station
            emergency.arrival_time = current_time
            print(f"Emergency passenger dropped off at {train_station} at time {current_time}.")
            # Update wait time for this emergency
            emergency.wait_time = emergency.arrival_time - emergency.request_time

        # Add passengers whose request time has arrived to the priority queue
        while (passenger_index < total_passengers and
               passenger_requests[passenger_index].request_time <= current_time):
            passenger = passenger_requests[passenger_index]
            # Calculate initial priority
            passenger.priority = calculate_priority(train_station, passenger.destination_station)
            heapq.heappush(passenger_queue, passenger)
            passenger_index += 1

        if passenger_queue:
            # Recalculate priorities based on current train station
            temp_passengers = []
            while passenger_queue:
                passenger = heapq.heappop(passenger_queue)
                passenger.priority = calculate_priority(train_station, passenger.destination_station)
                temp_passengers.append(passenger)
            for passenger in temp_passengers:
                heapq.heappush(passenger_queue, passenger)

            # Process the passenger with the highest priority (lowest priority number)
            passenger = heapq.heappop(passenger_queue)
            # Move train to passenger's start station
            travel_time = calculate_travel_time(train_station, passenger.start_station)
            current_time += travel_time
            train_station = passenger.start_station
            print(f"\nPicking up passenger from {passenger.start_station} to {passenger.destination_station}.")
            print(f"Train moved to {train_station} in {travel_time} time units.")
            # Move train to passenger's destination station
            travel_time = calculate_travel_time(train_station, passenger.destination_station)
            current_time += travel_time
            train_station = passenger.destination_station
            passenger.arrival_time = current_time
            print(f"Passenger dropped off at {train_station} at time {current_time}.")
            # Update wait time for this passenger
            passenger.wait_time = passenger.arrival_time - passenger.request_time
        else:
            # If no passengers are ready, advance time to the next request time
            if passenger_index < total_passengers:
                next_request_time = passenger_requests[passenger_index].request_time
                print(f"\nNo requests to process. Advancing time from {current_time} to {next_request_time}.")
                current_time = next_request_time
            else:
                # All passengers have been processed
                break

    # Calculate average wait time
    total_wait_time = sum([p.arrival_time - p.request_time for p in all_passengers])
    average_wait_time = total_wait_time / len(all_passengers) if all_passengers else 0
    print("\nAll requests have been processed.")
    print(f"Average wait time: {average_wait_time:.2f} time units.")

def calculate_travel_time(station_a, station_b):
    index_a = STATION_INDICES[station_a]
    index_b = STATION_INDICES[station_b]
    return abs(index_a - index_b)

def calculate_priority(current_station, destination_station):
    index_current = STATION_INDICES[current_station]
    index_destination = STATION_INDICES[destination_station]
    return abs(index_current - index_destination)

if __name__ == "__main__":
    main_menu()
