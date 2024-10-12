import heapq

# Passenger class with comparison methods
class Passenger:
    def __init__(self, start_station, destination_station, request_time):
        self.start_station = start_station.upper()
        self.destination_station = destination_station.upper()
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

# TrainSystem class containing the priority queue and emergency stack
class TrainSystem:
    def __init__(self):
        self.passenger_queue = []
        self.emergency_stack = EmergencyStack()
        self.current_time = 0  # To track the time for request_time
        self.station_positions = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    
    def add_passenger(self, start_station, destination_station):
        passenger = Passenger(start_station, destination_station, self.current_time)
        heapq.heappush(self.passenger_queue, passenger)
        print(f"Added passenger from {start_station.upper()} to {destination_station.upper()}")
        self.current_time += 1  # Increment time after each passenger is added

    def add_emergency(self, start_station, destination_station):
        passenger = Passenger(start_station, destination_station, self.current_time)
        self.emergency_stack.push(passenger)
        print(f"Emergency added for passenger from {start_station.upper()} to {destination_station.upper()}")
        self.current_time += 1  # Increment time after each emergency is added

    def calculate_priority(self, current_station, destination_station):
        distance = abs(self.station_positions[current_station] - self.station_positions[destination_station])
        return distance  # Smaller distance means higher priority

    def recalculate_priorities(self, current_station):
        temp_passengers = []
        
        # Remove all passengers from the heap
        while self.passenger_queue:
            passenger = heapq.heappop(self.passenger_queue)
            # Recalculate priority based on current station
            passenger.priority = self.calculate_priority(current_station, passenger.destination_station)
            temp_passengers.append(passenger)
        
        # Rebuild the heap with updated priorities
        for passenger in temp_passengers:
            heapq.heappush(self.passenger_queue, passenger)

    def calculate_travel_time(self, start_station, destination_station):
        return abs(self.station_positions[start_station] - self.station_positions[destination_station])

    def run(self):
        current_station = 'A'  # Starting station
        total_time = 0
        passenger_count = 0
        
        while self.passenger_queue or not self.emergency_stack.is_empty():
            # Handle emergencies first
            if not self.emergency_stack.is_empty():
                passenger = self.emergency_stack.pop()
                print(f"Handling emergency for passenger from {passenger.start_station} to {passenger.destination_station}")
                # Assume immediate processing
                travel_time = self.calculate_travel_time(current_station, passenger.destination_station)
                total_time += travel_time
                passenger_count += 1
                current_station = passenger.destination_station
            else:
                passenger = heapq.heappop(self.passenger_queue)
                print(f"Processing passenger from {passenger.start_station} to {passenger.destination_station} at station {current_station}")
                travel_time = self.calculate_travel_time(current_station, passenger.destination_station)
                total_time += travel_time
                passenger_count += 1
                current_station = passenger.destination_station
                # Recalculate priorities after each trip
                self.recalculate_priorities(current_station)
        
        average_time = total_time / passenger_count if passenger_count else 0
        print(f"Average travel time per passenger: {average_time:.2f}")

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
            # After running, reset the train system if you want to allow new inputs
            break
        elif choice == '4':
            print("Exiting the simulation.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

# Run the main function
if __name__ == "__main__":
    main()
