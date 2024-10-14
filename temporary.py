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
        self.onboard_passengers = []
        self.onboard_emergencies = []
        self.total_travel_time = 0
        self.total_passengers = 0

    def station_distance(self, start, end):
        return abs(self.stations.index(start) - self.stations.index(end))

    def calculate_priority(self, passenger):
        passenger.priority = self.station_distance(self.train_location, passenger.destination_station)

    def add_passenger_request(self, passenger):
        self.passenger_requests.append(passenger)
        self.passenger_requests.sort(key=lambda x: x.request_time)

    def add_emergency_request(self, emergency):
        self.emergency_requests.append(emergency)
        self.emergency_requests.sort(key=lambda x: x.request_time)  # Keep sorted by request time

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
        # Board passengers
        passengers_to_board = [p for p in self.passenger_requests
                               if p.start_station == self.train_location and p.request_time <= self.current_time]
        for passenger in passengers_to_board:
            self.calculate_priority(passenger)
            passenger.boarding_time = self.current_time
            heapq.heappush(self.passenger_queue, passenger)
            self.passenger_requests.remove(passenger)
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
        # Collect emergencies whose request_time <= current_time and have not yet been handled
        pending_emergencies = [e for e in self.emergency_requests if e.request_time <= self.current_time]
        # Remove them from emergency_requests
        for emergency in pending_emergencies:
            self.emergency_requests.remove(emergency)

        while pending_emergencies or self.onboard_emergencies:
            # Handle pending emergencies
            if pending_emergencies:
                # Pick the emergency with the earliest request time
                emergency = min(pending_emergencies, key=lambda e: e.request_time)
                # Move train to the emergency's start station
                while self.train_location != emergency.start_station:
                    self.current_time += 1
                    self.move_train(emergency.start_station)
                    self.process_alighting()
                    self.process_boarding()
                    # Check for new emergencies during movement
                    new_emergencies = [e for e in self.emergency_requests if e.request_time <= self.current_time]
                    for e in new_emergencies:
                        self.emergency_requests.remove(e)
                        pending_emergencies.append(e)

                # Board the emergency
                emergency.boarding_time = self.current_time
                self.onboard_emergencies.append(emergency)
                pending_emergencies.remove(emergency)
                print(f"Time {self.current_time}: Emergency boarded at station {self.train_location} going to {emergency.destination_station}")

            # Deliver onboard emergencies
            if self.onboard_emergencies:
                emergency = self.onboard_emergencies[0]
                # Move train to emergency's destination
                while self.train_location != emergency.destination_station:
                    self.current_time += 1
                    self.move_train(emergency.destination_station)
                    self.process_alighting()
                    self.process_boarding()
                    # Check for new emergencies during movement
                    new_emergencies = [e for e in self.emergency_requests if e.request_time <= self.current_time]
                    for e in new_emergencies:
                        self.emergency_requests.remove(e)
                        pending_emergencies.append(e)
                        # Break to handle new emergency
                        break
                    else:
                        continue
                    break  # Break if new emergency is added

                # Alight emergency if at destination
                if self.train_location == emergency.destination_station:
                    self.process_alighting()
                    self.onboard_emergencies.remove(emergency)
                    print(f"Time {self.current_time}: Emergency alighted at station {self.train_location}, travel time {self.current_time - emergency.boarding_time}")
                    self.current_time += 1  # Advance time after alighting

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
                # Before moving, check for new emergencies
                pending_emergencies = [e for e in self.emergency_requests if e.request_time <= self.current_time]
                if pending_emergencies:
                    # Handle emergencies
                    self.handle_emergencies()
                    # Recalculate priorities after handling emergencies
                    for p in self.passenger_queue:
                        self.calculate_priority(p)
                    heapq.heapify(self.passenger_queue)
                    break  # Break to reprocess the passenger queue

                self.move_train(passenger.destination_station)
                self.process_alighting()
                self.process_boarding()

            # Check if passenger has alighted
            if passenger not in self.onboard_passengers:
                continue  # Passenger has already alighted

            # Passenger alights
            self.process_alighting()
            if self.train_location == passenger.destination_station:
                self.current_time += 1  # Advance time after alighting

    def run(self):
        # Start simulation
        while (self.passenger_requests or self.emergency_requests or self.onboard_passengers or
               self.onboard_emergencies or self.passenger_queue):

            self.process_alighting()
            self.process_boarding()

            # Collect any new emergencies whose request_time <= current_time
            pending_emergencies = [e for e in self.emergency_requests if e.request_time <= self.current_time]
            if pending_emergencies or self.onboard_emergencies:
                self.handle_emergencies()
                # Recalculate priorities after emergencies
                for passenger in self.passenger_queue:
                    self.calculate_priority(passenger)
                heapq.heapify(self.passenger_queue)
            elif self.passenger_queue or self.onboard_passengers:
                self.handle_passengers()
            else:
                # No one to handle, advance time
                self.current_time += 1

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
