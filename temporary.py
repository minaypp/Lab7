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
        station_positions = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        wait_time = current_time - self.request_time
        distance = abs(station_positions[current_station] - station_positions[self.start_station])
        self.priority = distance - wait_time  # Adjust for priority calculation

    def __lt__(self, other):
        return self.priority < other.priority

# TrainSystem class with priority queue and emergency stack
class TrainSystem:
    def __init__(self):
        self.passenger_queue = []
        self.emergency_stack = []
        self.current_time = 0
        self.current_station = 'A'
        self.station_positions = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        self.train_moving = False
        self.destination_station = None
        self.train_arrival_time = 0
        self.passengers = []

    def add_passenger(self, start_station, destination_station):
        passenger = Passenger(start_station, destination_station, self.current_time)
        self.passengers.append(passenger)
        print(f"Added passenger from {start_station} to {destination_station} at time {self.current_time}")
        self.recalculate_priorities()
        self.current_time += 1

    def add_emergency(self, start_station, destination_station):
        passenger = Passenger(start_station, destination_station, self.current_time, is_emergency=True)
        self.emergency_stack.append(passenger)
        print(f"Emergency added for passenger from {start_station} to {destination_station} at time {self.current_time}")
        if not self.train_moving:
            self.handle_emergency(passenger)
        self.current_time += 1

    def calculate_travel_time(self, start_station, destination_station):
        return abs(self.station_positions[start_station] - self.station_positions[destination_station])

    def recalculate_priorities(self):
        self.passenger_queue = []  # Clear queue before recalculating
        for passenger in self.passengers:
            if not passenger.is_emergency:
                passenger.calculate_priority(self.current_station, self.current_time)
                heapq.heappush(self.passenger_queue, passenger)

    def handle_emergency(self, passenger):
        print(f"Handling emergency for passenger from {passenger.start_station} to {passenger.destination_station}")
        self.move_train_to(passenger.start_station)
        self.move_train_to(passenger.destination_station)
        self.passengers.remove(passenger)

    def move_train_to(self, station):
        travel_time = self.calculate_travel_time(self.current_station, station)
        self.current_time += travel_time
        print(f"Train moved from {self.current_station} to {station} in {travel_time} time units.")
        self.current_station = station

    def run(self):
        total_passengers = len(self.passengers)
        total_travel_time = 0

        while self.passengers or self.train_moving:
            if self.emergency_stack:
                passenger = self.emergency_stack.pop()
                self.handle_emergency(passenger)
                continue

            if self.train_moving:
                time_to_advance = self.train_arrival_time - self.current_time
                self.current_time = self.train_arrival_time
                self.current_station = self.destination_station
                print(f"Train arrived at {self.current_station} at time {self.current_time}")
                self.train_moving = False
                self.destination_station = None
                self.recalculate_priorities()
            else:
                if not self.passenger_queue:
                    self.current_time += 1
                    continue

                passenger = heapq.heappop(self.passenger_queue)
                if self.current_station != passenger.start_station:
                    self.move_train_to(passenger.start_station)

                self.move_train_to(passenger.destination_station)
                total_travel_time += self.calculate_travel_time(passenger.start_station, passenger.destination_station)
                self.passengers.remove(passenger)
                self.recalculate_priorities()

        average_travel_time = total_travel_time / total_passengers if total_passengers else 0
        print(f"Average travel time per passenger: {average_travel_time:.2f}")

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
            break
        elif choice == '4':
            print("Exiting the simulation.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
