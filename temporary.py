import heapq

# Passenger class with comparison methods
class Passenger:
    def __init__(self, start_station, destination_station, request_time, is_emergency=False):
        self.start_station = start_station.upper()
        self.destination_station = destination_station.upper()
        self.request_time = request_time
        self.is_emergency = is_emergency
        self.priority = None  # Will be calculated dynamically

    def calculate_priority(self, current_station, current_time):
        # Priority based on wait time and distance from current station
        station_positions = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        wait_time = current_time - self.request_time
        distance = abs(station_positions[current_station] - station_positions[self.start_station])
        # Higher priority for passengers who have waited longer and are closer
        self.priority = distance - wait_time  # Adjust as needed for desired behavior

    def __lt__(self, other):
        return self.priority < other.priority

# TrainSystem class containing the priority queue and emergency stack
class TrainSystem:
    def __init__(self):
        self.passenger_queue = []
        self.emergency_stack = []
        self.current_time = 0  # Simulated time units
        self.current_station = 'A'  # Starting station
        self.station_positions = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        self.train_moving = False
        self.destination_station = None  # Station the train is moving towards
        self.train_arrival_time = 0  # Time when the train will arrive at the destination
        self.passengers = []  # List of all passengers for tracking purposes

    def add_passenger(self, start_station, destination_station):
        passenger = Passenger(start_station, destination_station, self.current_time)
        self.passengers.append(passenger)
        print(f"Added passenger from {start_station.upper()} to {destination_station.upper()} at time {self.current_time}")
        # Recalculate priorities when new passengers are added
        self.recalculate_priorities()
        self.current_time += 1  # Increment time after each action

    def add_emergency(self, start_station, destination_station):
        passenger = Passenger(start_station, destination_station, self.current_time, is_emergency=True)
        self.emergency_stack.append(passenger)
        print(f"Emergency added for passenger from {start_station.upper()} to {destination_station.upper()} at time {self.current_time}")
        # Emergencies are handled immediately if the train is not moving
        if not self.train_moving:
            self.handle_emergency(passenger)
        self.current_time += 1  # Increment time after each action

    def calculate_travel_time(self, start_station, destination_station):
        return abs(self.station_positions[start_station] - self.station_positions[destination_station])

    def recalculate_priorities(self):
        for passenger in self.passengers:
            if not passenger.is_emergency and passenger not in self.passenger_queue:
                # Only recalculate for passengers not yet in the queue
                passenger.calculate_priority(self.current_station, self.current_time)
                heapq.heappush(self.passenger_queue, passenger)

    def handle_emergency(self, passenger):
        if self.train_moving:
            print(f"Train is currently moving to {self.destination_station}, cannot handle emergency immediately.")
            return
        print(f"Handling emergency for passenger from {passenger.start_station} to {passenger.destination_station} at time {self.current_time}")
        # Move train to passenger's start station
        travel_time_to_start = self.calculate_travel_time(self.current_station, passenger.start_station)
        self.current_time += travel_time_to_start
        print(f"Train moved from {self.current_station} to {passenger.start_station} in {travel_time_to_start} time units.")
        self.current_station = passenger.start_station
        # Then move to destination
        travel_time_to_destination = self.calculate_travel_time(passenger.start_station, passenger.destination_station)
        self.current_time += travel_time_to_destination
        print(f"Train moved from {passenger.start_station} to {passenger.destination_station} in {travel_time_to_destination} time units.")
        self.current_station = passenger.destination_station
        # Emergency handled
        self.passengers.remove(passenger)

    def run(self):
        total_passengers = len(self.passengers)
        total_travel_time = 0
        while self.passengers or self.train_moving:
            # Process emergencies first
            if self.emergency_stack:
                passenger = self.emergency_stack.pop()
                self.handle_emergency(passenger)
                continue
            # If the train is moving, advance time until arrival
            if self.train_moving:
                time_to_advance = self.train_arrival_time - self.current_time
                self.current_time = self.train_arrival_time
                self.current_station = self.destination_station
                print(f"Train arrived at {self.current_station} at time {self.current_time}")
                self.train_moving = False
                self.destination_station = None
                # Recalculate priorities after arriving
                self.recalculate_priorities()
            else:
                if not self.passenger_queue:
                    # No passengers to process, advance time
                    self.current_time += 1
                    continue
                # Get next passenger from queue
                passenger = heapq.heappop(self.passenger_queue)
                # Move train to passenger's start station if not already there
                if self.current_station != passenger.start_station:
                    travel_time_to_start = self.calculate_travel_time(self.current_station, passenger.start_station)
                    self.train_moving = True
                    self.destination_station = passenger.start_station
                    self.train_arrival_time = self.current_time + travel_time_to_start
                    print(f"Train is moving from {self.current_station} to {self.destination_station}, will arrive at time {self.train_arrival_time}")
                    continue  # Will handle arrival in next iteration
                # Move train to passenger's destination
                travel_time_to_destination = self.calculate_travel_time(self.current_station, passenger.destination_station)
                self.train_moving = True
                self.destination_station = passenger.destination_station
                self.train_arrival_time = self.current_time + travel_time_to_destination
                print(f"Passenger from {passenger.start_station} to {passenger.destination_station} boarded at time {self.current_time}")
                print(f"Train is moving to {self.destination_station}, will arrive at time {self.train_arrival_time}")
                total_travel_time += travel_time_to_destination
                self.passengers.remove(passenger)
                # Recalculate priorities
                self.recalculate_priorities()

        average_travel_time = total_travel_time / total_passengers if total_passengers else 0
        print(f"Average travel time per passenger: {average_travel_time:.2f}")

# Main function to interact with the user
def main():
    train_system = TrainSystem()
    print("Welcome to the Train System Simulation")
    print("Stations available: A, B, C, D")
    while True:
        print("\nOptions:")
        print("1. Add a passenger")
        print("2. Add an emergency")
        print("3. Run the train system")
        print("4. Exit")
        choice = input("Please enter your choice (1-4): ").strip()
        
        if choice == '1':
            start_station = input("Enter the starting station (A-D): ").strip().upper()
            destination_station = input("Enter the destination station (A-D): ").strip().upper()
            if start_station in 'ABCD' and destination_station in 'ABCD' and start_station != destination_station:
                train_system.add_passenger(start_station, destination_station)
            else:
                print("Invalid stations entered. Please try again.")
        elif choice == '2':
            start_station = input("Enter the starting station for the emergency (A-D): ").strip().upper()
            destination_station = input("Enter the destination station for the emergency (A-D): ").strip().upper()
            if start_station in 'ABCD' and destination_station in 'ABCD' and start_station != destination_station:
                train_system.add_emergency(start_station, destination_station)
            else:
                print("Invalid stations entered. Please try again.")
        elif choice == '3':
            print("\nRunning the train system simulation...")
            train_system.run()
            break  # Exit after running
        elif choice == '4':
            print("Exiting the simulation.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

# Run the main function
if __name__ == "__main__":
    main()
