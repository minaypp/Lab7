import heapq
import random

class Passenger:
    def __init__(self, start_station, destination_station, request_time, priority=0, emergency=False):
        self.start_station = start_station
        self.destination_station = destination_station
        self.request_time = request_time
        self.priority = priority  # Will be updated based on distance to destination
        self.emergency = emergency
        self.boarded = False
        self.pickup_time = None
        self.dropoff_time = None
        self.assigned_priority = None

    def __lt__(self, other):
        # For priority queue, higher priority passengers come first
        return self.priority > other.priority  # Since we use heapq which is a min-heap

    def __repr__(self):
        return f"Passenger({self.start_station}->{self.destination_station}, priority={self.assigned_priority}, emergency={self.emergency})"

class TrainSystem:
    def __init__(self, stations):
        self.stations = stations
        self.passengers = []  # priority queue for regular passengers
        self.emergencies = []  # stack for emergency passengers
        self.onboard_passengers = []
        self.current_time = 0  # in cycles
        self.train_location = stations[0]
        self.total_travel_time = 0
        self.total_passengers = 0

    def calculate_distance(self, start, end):
        return abs(self.stations.index(start) - self.stations.index(end))

    def generate_new_passengers(self):
        # Random chance for emergency passenger
        if random.random() < 0.1:  # 10% chance
            start_station = random.choice(self.stations)
            destination_station = random.choice(self.stations)
            while destination_station == start_station:
                destination_station = random.choice(self.stations)
            new_emergency = Passenger(start_station, destination_station, self.current_time, emergency=True)
            self.emergencies.append(new_emergency)
            print(f"Emergency added: {new_emergency}")
        # Random number of regular passengers
        num_passengers = random.randint(0, 5)
        for _ in range(num_passengers):
            start_station = random.choice(self.stations)
            destination_station = random.choice(self.stations)
            while destination_station == start_station:
                destination_station = random.choice(self.stations)
            new_passenger = Passenger(start_station, destination_station, self.current_time)
            self.passengers.append(new_passenger)
            print(f"New passenger added: {new_passenger}")
        # We need to heapify the priority queue
        heapq.heapify(self.passengers)

    def update_priorities(self):
        # Update priority of each passenger based on distance from train's location to their destination
        for passenger in self.passengers:
            distance = self.calculate_distance(self.train_location, passenger.destination_station)
            # Priority is higher when distance is longer
            passenger.priority = -distance  # negative distance so that heapq pops passengers with higher distance first
            passenger.assigned_priority = -passenger.priority
            print(f"Assigned priority {passenger.assigned_priority} to passenger {passenger}")
        # Need to heapify again after updating priorities
        heapq.heapify(self.passengers)

    def board_passengers(self):
        # Passengers at current station can board
        boarding_passengers = []
        for passenger in self.passengers:
            if passenger.start_station == self.train_location and not passenger.boarded:
                passenger.boarded = True
                passenger.pickup_time = self.current_time
                boarding_passengers.append(passenger)
        # Remove boarded passengers from the priority queue
        for passenger in boarding_passengers:
            self.passengers.remove(passenger)
        heapq.heapify(self.passengers)
        # Add to onboard passengers
        self.onboard_passengers.extend(boarding_passengers)
        if boarding_passengers:
            print(f"Passengers boarded at {self.train_location}: {boarding_passengers}")

    def alight_passengers(self):
        # Passengers whose destination is current station alight
        alighting_passengers = []
        for passenger in self.onboard_passengers:
            if passenger.destination_station == self.train_location:
                passenger.dropoff_time = self.current_time
                travel_time = passenger.dropoff_time - passenger.pickup_time
                self.total_travel_time += travel_time
                self.total_passengers += 1
                alighting_passengers.append(passenger)
        # Remove alighting passengers from onboard_passengers
        for passenger in alighting_passengers:
            self.onboard_passengers.remove(passenger)
        if alighting_passengers:
            print(f"Passengers alighted at {self.train_location}: {alighting_passengers}")

    def move_train(self, next_station):
        # Move train to next station
        print(f"Train moving from {self.train_location} to {next_station}")
        self.train_location = next_station
        self.current_time += 1  # Moving consumes one cycle

    def handle_emergencies(self):
        while self.emergencies:
            emergency_passenger = self.emergencies.pop()
            print(f"Handling emergency: {emergency_passenger}")
            # Move train to emergency passenger's start station if not already there
            if self.train_location != emergency_passenger.start_station:
                self.move_train_to_station(emergency_passenger.start_station)
            # Board the emergency passenger
            emergency_passenger.boarded = True
            emergency_passenger.pickup_time = self.current_time
            self.onboard_passengers.append(emergency_passenger)
            print(f"Emergency passenger boarded at {self.train_location}: {emergency_passenger}")
            # Move train to emergency passenger's destination
            self.move_train_to_station(emergency_passenger.destination_station)
            # Passenger alights
            emergency_passenger.dropoff_time = self.current_time
            travel_time = emergency_passenger.dropoff_time - emergency_passenger.pickup_time
            self.total_travel_time += travel_time
            self.total_passengers += 1
            self.onboard_passengers.remove(emergency_passenger)
            print(f"Emergency passenger alighted at {self.train_location}: {emergency_passenger}")
            # Check if new emergencies arrived during handling
            self.generate_new_passengers()
            if self.emergencies:
                continue
            else:
                break

    def move_train_to_station(self, destination):
        # Move train step by step towards destination
        while self.train_location != destination:
            # Decide direction
            current_index = self.stations.index(self.train_location)
            destination_index = self.stations.index(destination)
            if destination_index > current_index:
                next_station = self.stations[current_index + 1]
            elif destination_index < current_index:
                next_station = self.stations[current_index - 1]
            else:
                break
            self.move_train(next_station)
            # After moving, check for new emergencies or passengers (simplification)
            self.alight_passengers()
            self.board_passengers()
            self.generate_new_passengers()

    def simulate_cycle(self):
        print(f"\nCycle {self.current_time}: Train at {self.train_location}")
        self.generate_new_passengers()
        self.board_passengers()
        self.alight_passengers()
        # Update priorities after boarding and alighting
        self.update_priorities()
        if self.emergencies:
            self.handle_emergencies()
        elif self.passengers:
            # Get the highest priority passenger
            highest_priority_passenger = heapq.heappop(self.passengers)
            # Determine next station based on their destination
            next_station = highest_priority_passenger.destination_station
            # Move to passenger's start station if not already there
            if self.train_location != highest_priority_passenger.start_station:
                self.move_train_to_station(highest_priority_passenger.start_station)
            # Board the passenger if not already boarded
            if not highest_priority_passenger.boarded:
                highest_priority_passenger.boarded = True
                highest_priority_passenger.pickup_time = self.current_time
                self.onboard_passengers.append(highest_priority_passenger)
                print(f"Passenger boarded at {self.train_location}: {highest_priority_passenger}")
            # Move towards their destination
            self.move_train_to_station(next_station)
            # Passenger alights
            highest_priority_passenger.dropoff_time = self.current_time
            travel_time = highest_priority_passenger.dropoff_time - highest_priority_passenger.pickup_time
            self.total_travel_time += travel_time
            self.total_passengers += 1
            self.onboard_passengers.remove(highest_priority_passenger)
            print(f"Passenger alighted at {self.train_location}: {highest_priority_passenger}")
        else:
            # No passengers to handle this cycle.
            print("No passengers to handle this cycle.")
            self.current_time += 1

    def calculate_average_travel_time(self):
        if self.total_passengers == 0:
            return 0
        return self.total_travel_time / self.total_passengers

def main():
    stations = ['A', 'B', 'C', 'D']
    train_system = TrainSystem(stations)
    num_cycles = 10  # Run simulation for 10 cycles
    for _ in range(num_cycles):
        train_system.simulate_cycle()
    average_travel_time = train_system.calculate_average_travel_time()
    print(f"\nAverage travel time: {average_travel_time} cycles")

if __name__ == "__main__":
    main()
