# Lab7
Overview:
In this lab, students will simulate a train control system using a priority queue to optimize the boarding and routing of passengers. The system will dynamically update passenger priorities based on the current station of the train and the destination of each passenger. The goal is to minimize overall travel time for passengers by using priority-based decision-making, as well as to explore the differences between using a regular queue and a priority queue.

By the end of the lab, students will:

Understand how priority queues work and how they differ from regular queues.
Implement a priority queue using Python's heapq module.
Recalculate and update priorities dynamically as conditions change.
Optimize a system for routing and travel time using real-time decision-making.
 

Objectives
You are tasked with simulating a simplified train system where passengers board at one of four stations (A, B, C, or D) and travel to another station. Each train station exists in a static line, equally spaced apart, with A and one end and D at the opposite. The system needs to:

Handle passenger boarding requests with priorities based on the proximity of their destination.
Recalculate priorities dynamically as the train moves between stations to optimize the passenger processing order.
Manage emergency situations using a stack for emergency overrides (Last-In-First-Out).
Calculate the average time it takes for a passenger to reach their destination.
Requirements
Priority Queue:
Use Python’s heapq to create a priority queue where passengers with the highest priority are processed first.
Stack for Emergencies:
Implement a stack using a linked list to handle emergency overrides that need immediate attention.
Process emergencies with LIFO (Last-In-First-Out) behavior, ensuring that the most recent emergency is handled first.
Dynamic Priority Calculation:
Recalculate priorities after every trip based on the current station of the train and the passenger's destination.
The closer the passenger's destination to the current station, the higher the priority (lower priority number).
Passenger Class:
Each passenger should have a start_station, destination_station, request_time, and priority. The priority is initially based on the distance between their boarding station and destination.
Train System:
The train processes passengers from a priority queue. After each trip (when a passenger is dropped off), the system recalculates the priorities of all remaining passengers based on the current station of the train.
