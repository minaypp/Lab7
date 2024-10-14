import heapq

class Passenger:
    def __init__(self, start_station, destination_station, request_time):
        self.start_station = start_station
        self.destination_station = destination_station
        self.request_time = request_time
        self.priority = None  # Will be calculated dynamically
        self.arrival_time = None  # Time when the passenger reaches their destination
        self.boarding_time = None  # Time when the passenger boards the train

    def __lt__(self, other):
        return self.priority < other.priority

class Emergency:
    def __init__(self, start_station, destination_station, request_time):
        self.start_station = start_station
        self.destination_station = destination_station
        self.request_time = request_time
        self.arrival_time = None  # Time when the emergency reaches their destination
        self.boarding_time = None  # Time when the emergency boards the train

class TrainSystem:
    def __init__(self):
        self.stations = ['A', 'B', 'C', 'D']
        self.passenger_requests = []
        self.emergency_requests = []
        self.current_time = 0
        self.train_location = 'A'
        self.train_direction = 1  # 1 for forward, -1 for backward
        self.passenger_queue = []
        self.emergency_stack = []
        self.onboard_passengers = []
        self.onboard_emergencies = []
        self.total_travel_time = 0
        self.total_passengers = 0

    def station_distance(self, start, end):
        return abs(self.stations.index(start) - self.stations.index(end))

    def calculate_priority(self, passenger):
        passenger.priority = self.station_distance(self.train_location, passenger.destination_station)

    def add_passenger_request(self, passenger):
        heapq.heappush(self.passenger_requests, (passenger.request_time, passenger))

    def add_emergency_request(self, emergency):
        self.emergency_requests.append((emergency.request_time, emergency))
        self.emergency_requests.sort(key=lambda x: x[0])  # Keep sorted by request time

    def get_next_station(self, destination):
        current_index = self.stations.index(self.train_location)
        dest_index = self.stations.index(destination)
        if current_index < dest_index:
            return self.stations[current_index + 1]
        elif current_index > dest_index:
            return self.stations[current_index - 1]
        else:
            return self.train_location

    def move_train(self, destination):
        next_station = self.get_next_station(destination)
        if self.train_location != next_station:
            self.train_location = next_station
            print(f"Time {self.current_time}: Train moved to station {self.train_location}")

    def process_boarding(self):
        # Board emergencies first
        emergencies_to_board = [e for rt, e in self.emergency_requests
                                if e.start_station == self.train_location and e.request_time <= self.current_time]
        for emergency in emergencies_to_board:
            self.emergency_stack.append(emergency)
            emergency.boarding_time = self.current_time
            self.emergency_requests.remove((emergency.request_time, emergency))
            print(f"Time {self.current_time}: Emergency boarded at station {self.train_location} going to {emergency.destination_station}")

        # Board passengers
        passengers_to_board = [p for rt, p in self.passenger_requests
                               if p.start_station == self.train_location and p.request_time <= self.current_time]
        for passenger in passengers_to_board:
            self.calculate_priority(passenger)
            passenger.boarding_time = self.current_time
            heapq.heappush(self.passenger_queue, passenger)
            self.passenger_requests.remove((passenger.request_time, passenger))
            print(f"Time {self.current_time}: Passenger boarded at station {self.train_location} going to {passenger.destination_station}")

    def process_alighting(self):
        # Alight emergencies first
        for emergency in self.onboard_emergencies[:]:
            if emergency.destination_station == self.train_location:
                emergency.arrival_time = self.current_time
                self.onboard_emergencies.remove(emergency)
                travel_time = emergency.arrival_time - emergency.boarding_time
                self.total_travel_time += travel_time
                self.total_passengers += 1
                print(f"Time {self.current_time}: Emergency alighted at station {self.train_location}, travel time {travel_time}")

        # Alight passengers
        for passenger in self.onboard_passengers[:]:
            if passenger.destination_station == self.train_location:
                passenger.arrival_time = self.current_time
                self.onboard_passengers.remove(passenger)
                travel_time = passenger.arrival_time - passenger.boarding_time
                self.total_travel_time += travel_time
                self.total_passengers += 1
                print(f"Time {self.current_time}: Passenger alighted at station {self.train_location}, travel time {travel_time}")

    def handle_emergencies(self):
        while self.emergency_stack or self.onboard_emergencies:
            # If there are emergencies already onboard, handle them first
            if self.onboard_emergencies:
                emergency = self.onboard_emergencies[0]
            else:
                emergency = self.emergency_stack.pop()
                self.onboard_emergencies.append(emergency)
                print(f"Time {self.current_time}: Handling emergency from {emergency.start_station} to {emergency.destination_station}")

            # Move train to emergency's destination
            while self.train_location != emergency.destination_station:
                self.current_time += 1
                self.move_train(emergency.destination_station)
                self.process_alighting()
                self.process_boarding()

            # Emergency alights
            self.process_alighting()

    def handle_passengers(self):
        while self.passenger_queue or self.onboard_passengers:
            if self.onboard_passengers:
                passenger = self.onboard_passengers[0]
            else:
                passenger = heapq.heappop(self.passenger_queue)
                self.onboard_passengers.append(passenger)
                print(f"Time {self.current_time}: Handling passenger from {passenger.start_station} to {passenger.destination_station}")

            # Move train to passenger's destination
            while self.train_location != passenger.destination_station:
                self.current_time += 1
                # Check for emergencies before moving
                self.process_boarding()
                if self.emergency_stack or self.onboard_emergencies:
                    self.handle_emergencies()
                    # Recalculate priorities after handling emergencies
                    for p in self.passenger_queue:
                        self.calculate_priority(p)
                    heapq.heapify(self.passenger_queue)
                    break  # Break to reprocess the passenger queue

                self.move_train(passenger.destination_station)
                self.process_alighting()
                self.process_boarding()
                if self.emergency_stack or self.onboard_emergencies:
                    break  # Break to handle emergencies

            # Check if passenger has alighted
            if passenger not in self.onboard_passengers:
                continue  # Passenger has already alighted

            # Passenger alights
            self.process_alighting()

    def run(self):
        # Start simulation
        while (self.passenger_requests or self.emergency_requests or self.onboard_passengers or
               self.onboard_emergencies or self.passenger_queue or self.emergency_stack):

            self.process_alighting()
            self.process_boarding()

            # Handle emergencies first
            if self.emergency_stack or self.onboard_emergencies:
                self.handle_emergencies()
                # Recalculate priorities after emergencies
                for passenger in self.passenger_queue:
                    self.calculate_priority(passenger)
                heapq.heapify(self.passenger_queue)
            elif self.passenger_queue or self.onboard_passengers:
                self.handle_passengers()
            else:
                # No one to handle, move train to next station
                self.current_time += 1
                self.move_train(self.get_next_station(self.stations[-1]))  # Move towards the end station

        if self.total_passengers > 0:
            average_travel_time = self.total_travel_time / self.total_passengers
            print(f"\nAverage travel time: {average_travel_time}")
        else:
            print("No passengers or emergencies were processed.")

def main():
    train_system = TrainSystem()
    print("Welcome to the Train Simulation System")
    while True:
        print("\nMenu:")
        print("1. Add Passenger Request")
        print("2. Add Emergency Request")
        print("3. Start Simulation")
        choice = input("Please select an option (1-3): ")
        if choice == '1':
            try:
                request_time = int(input("Enter request time: "))
                start_station = input("Enter start station (A-D): ").upper()
                destination_station = input("Enter destination station (A-D): ").upper()
                if start_station not in train_system.stations or destination_station not in train_system.stations:
                    print("Invalid station. Please try again.")
                    continue
                if start_station == destination_station:
                    print("Start and destination stations cannot be the same. Please try again.")
                    continue
                passenger = Passenger(start_station, destination_station, request_time)
                train_system.add_passenger_request(passenger)
            except ValueError:
                print("Invalid input. Please enter numeric values for time.")
        elif choice == '2':
            try:
                request_time = int(input("Enter request time: "))
                start_station = input("Enter start station (A-D): ").upper()
                destination_station = input("Enter destination station (A-D): ").upper()
                if start_station not in train_system.stations or destination_station not in train_system.stations:
                    print("Invalid station. Please try again.")
                    continue
                if start_station == destination_station:
                    print("Start and destination stations cannot be the same. Please try again.")
                    continue
                emergency = Emergency(start_station, destination_station, request_time)
                train_system.add_emergency_request(emergency)
            except ValueError:
                print("Invalid input. Please enter numeric values for time.")
        elif choice == '3':
            print("Starting simulation...")
            train_system.run()
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
