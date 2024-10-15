import heapq

#Requirement 1 - Priority Queue class for storing passengers based on priority
class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, passenger):
        heapq.heappush(self.queue, passenger)

    def pop(self):
        return heapq.heappop(self.queue)

    def empty(self):
        return len(self.queue) == 0

#Requirement 2 - Linked List stack
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.stack.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0

#Requirement 4 - Passenger Class
class Passenger:
    def __init__(self, start_station, destination_station, request_time, priority):
        self.start_station =  start_station
        self.destination_station = destination_station
        self.request_time = request_time
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

#System to simulate a train
class TrainSystem():
    def __init__(self, stations):
        self.stations = stations
        self.passengers = PriorityQueue()
        self.emergencies = Stack()
        self.current_time = 0
        self.train_location = self.stations[0]
        self.onboard_passengers = []
        self.CarryCount = 0
        self.totalTravel = 0

    #Pick up a passenger
    def pick_up_passenger(self, passenger):
        self.onboard_passengers.append(passenger)
        self.CarryCount += 1

    #Drop off a passenger
    def drop_off_passenger(self, passenger):
        self.totalTravel += self.calculate_traveltime(passenger)
        self.onboard_passengers.remove(passenger)

    def calculate_traveltime(self, p):
        return abs(self.current_time - self.p.request_time)

def main():
    stations = ['Station A', 'Station B', 'Station C', 'Station D']
    train_system = TrainSystem(stations)

    #Add passengers to the priority queue
    passengers = [
        Passenger('Station A', 'Station B', 10, 1),
        Passenger('Station B', 'Station C', 20, 2),
        Passenger('Station C', 'Station A', 30, 3),
        Passenger('Station A', 'Station D', 40, 4),
        Passenger('Station D', 'Station B', 50, 5),
        Passenger('Station B', 'Station A', 60, 6),
        Passenger('Station A', 'Station B', 70, 7)
    ]

    for passenger in passengers:
        train_system.passengers.put(passenger)

    #Add emergencies to the stack
    emergencies = [
        Passenger('Station B', 'Station C', 15, 1),
        Passenger('Station C', 'Station A', 25, 2)
    ]

    for emergency in emergencies:
        train_system.add_emergency(emergency)


main()
