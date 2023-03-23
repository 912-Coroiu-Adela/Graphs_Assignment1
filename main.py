import random
import tkinter as tk
from tkinter import filedialog
import os


class Directional_Graph:

    def __init__(self) -> None:
        self.inbound_nodes = {}
        self.outbound_nodes = {}
        self.costs = {}
        self.last_node = -1
        self.hidden = True

    def add_empty_node(self):
        node = self.get_last_node() + 1
        if node not in self.inbound_nodes:
            self.inbound_nodes[node] = [-2]
        if node not in self.outbound_nodes:
            self.outbound_nodes[node] = [-2]
        self.last_node = node

    def remove_empty_node(self, node):
        if node not in self.inbound_nodes or node not in self.outbound_nodes:
            return 
        if self.inbound_nodes[node] != [-2] or self.outbound_nodes[node] != [-2]:
            return
        del self.inbound_nodes[node]
        del self.outbound_nodes[node]

    def add_node(self, node, start, end, cost):
        if start not in self.inbound_nodes:
            self.inbound_nodes[start] = []
        if end not in self.outbound_nodes:
            self.outbound_nodes[end] = []
        self.inbound_nodes[end].append(start)
        self.outbound_nodes[start].append(end)
        self.costs[[start, end]] = cost   

    def remove_node(self, node):
        if node not in self.inbound_nodes or node not in self.outbound_nodes:
            raise ValueError("Node doesn't exist")
        self.delete_node_edges(node)
        del self.inbound_nodes[node]
        del self.outbound_nodes[node]


    def delete_node_edges(self, node):
        edges = []
        for edge in self.costs.keys():
            if edge[0] == node or edge[1] == node:
                edges.append(edge)

        for edge in edges:
            del self.costs[edge]
        
    def is_edge(self, start, end):
        return (start, end) in self.costs

    def is_node(self, node):
        if node == -1:
            return False
        if node > self.last_node:
            return False
        return node in self.inbound_nodes and node in self.outbound_nodes

    def add_edge(self, start, end, cost):
        if start not in self.inbound_nodes:
            raise ValueError("Invalid start node!")
        if end not in self.outbound_nodes:
            raise ValueError("Invalid end node!")
        if self.is_edge(start, end):
            raise ValueError("Edge already exists!")
        if -1 in self.inbound_nodes[end]:
            self.inbound_nodes[end].remove(-1)
        if -1 in self.outbound_nodes[start]:
            self.outbound_nodes[start].remove(-1)
        self.inbound_nodes[end].append(start)
        self.outbound_nodes[start].append(end)
        self.costs[(start, end)] = cost

    def remove_edge(self, start, end):
        self.inbound_nodes[end].remove(start)
        self.outbound_nodes[start].remove(end)
        del self.costs[(start, end)]
        if len(self.inbound_nodes[end]) == 0:
            self.inbound_nodes[end].append(-2)
        if len(self.outbound_nodes[start]) == 0:
            self.outbound_nodes[start].append(-2)

    def get_last_node(self):
        return self.last_node

    def get_cost(self, start, end):
        return self.costs[(start, end)]
    
    def set_cost(self, start, end, cost):
        self.costs[(start, end)] = cost
    
    def get_edge(self, start, end):
        return self.outbound_nodes[start][end]
    
    def get_inbound_nodes(self, node):
        return self.inbound_nodes[node]
    
    def get_outbound_nodes(self, node):
        return self.outbound_nodes[node]

    def get_number_of_nodes(self):
        return len(self.inbound_nodes)
    
    def get_number_of_edges(self):
        return len(self.costs)
    
    def get_nodes(self):
        nodes = []
        for node in self.inbound_nodes:
            if node == -1:
                continue
            nodes.append(node)
        return nodes
    
    def get_edges(self):
        return self.costs.keys()
    
    def get_inbound_edges(self, node):
        return self.inbound_nodes[node]
    
    def get_outbound_edges(self, node):
        return self.outbound_nodes[node]

    def get_in_degree(self, node):
        if self.inbound_nodes[node] == [-2]:
            return 0
        return len(self.inbound_nodes[node])

    def get_out_degree(self, node):
        if self.outbound_nodes[node] == [-2]:
            return 0
        return len(self.outbound_nodes[node])
    
    def get_inbound_edges_with_costs(self, node):
        return [(edge, self.costs[edge]) for edge in self.inbound_nodes[node]]
    
    def get_outbound_edges_with_costs(self, node):
        return [(edge, self.costs[edge]) for edge in self.outbound_nodes[node]]
    
    def string_representation(self):
        return f"Nodes: {self.get_nodes()}\nEdges: {self.costs.keys()}\nCosts: {self.costs.values()}"

    def load_from_file(self, file_str):
        with open(file_str, "r") as f:
            lines = f.readlines()
            n = int(lines[0].split()[0])
            m = int(lines[0].split()[1])
            for i in range(n):
                self.add_empty_node()
            for i in range(m):
                start = int(lines[i+1].split()[0])
                end = int(lines[i+1].split()[1])
                cost = int(lines[i+1].split()[2])
                self.add_edge(start, end, cost)

    def reindex_nodes_costs(self):
        new_nodes = {}
        new_costs = {}
        total = self.get_number_of_nodes()
        if total == self.last_node + 1:
            return
        for i in range(self.get_number_of_nodes()):
            new_nodes[i] = self.get_nodes()[i]
        percent = 0
        division = total / 100
        for i in range(self.get_number_of_nodes()):
            if i / division > percent:
                print(f"Reindexing costs: {percent}% done ({i}/{total})")
                percent += 1
            for j in range(self.get_number_of_nodes()):
                if (self.get_nodes()[i], self.get_nodes()[j]) in self.costs:
                    new_costs[(i, j)] = self.costs[(self.get_nodes()[i], self.get_nodes()[j])]
        self.inbound_nodes = new_nodes
        self.outbound_nodes = new_nodes
        self.costs = new_costs


    def save_to_file(self, file_str):
        self.reindex_nodes_costs()
        with open(file_str, "w+") as f:
            f.write(f"{self.get_number_of_nodes()} {self.get_number_of_edges()}\n")
            for edge in self.costs:
                f.write(f"{edge[0]} {edge[1]} {self.costs[edge]}\n")


class UI:
    def __init__(self, graph) -> None:
        self.graph = graph
     
    def print_menu(self):
        os.system("cls")
        print("\n---------Graph---------")
        if self.graph.get_number_of_nodes() == 0:
            print("The graph is empty")
        elif self.graph.hidden:
            print("The graph is hidden")
        else:
            print(self.graph.string_representation())
        print("\n---------Menu---------")
        print("1. Load graph from file")
        print("2. Generate a random graph")
        print("3. Modify the graph")
        print("4. Calculate the in degree and out degree of a node")
        print("8. Copy the graph to text file")
        print("9. Show/Hide Graph")
        print("0. Exit")

    def print_modify_menu(self):
        print("---------Modify Menu---------")
        print("1. Add a node")
        print("2. Remove a node")
        print("3. Add an edge")
        print("4. Remove an edge")
        print("5. Get the cost of an edge")
        print("6. Change the cost of an edge")
        print("0. Back")

    def get_modify_option(self):
        choice = input("Enter your choice: ")
        if choice == "1":
            self.graph.add_empty_node()
        elif choice == "2":
            try:
                node = int(input("Enter the node: "))
                self.graph.remove_node(node)
            except ValueError:
                print("Invalid node!")
        elif choice == "3":
            try:
                start = int(input("Enter the start node: "))
                end = int(input("Enter the end node: "))
                cost = int(input("Enter the cost: "))
                self.graph.add_edge(start, end, cost)
            except ValueError as e:
                print(e)
        elif choice == "4":
            try:
                start = int(input("Enter the start node: "))
                end = int(input("Enter the end node: "))
                self.graph.remove_edge(start, end)
            except ValueError as e:
                print("Invalid edge!")
        elif choice == "5":
            try:
                start = int(input("Enter the start node: "))
                end = int(input("Enter the end node: "))
                if not self.graph.is_edge(start, end):
                    print("The edge does not exist!")
                    input("Press enter to continue...")
                    raise ValueError
                print(f"The cost of the edge is: {self.graph.get_cost(start, end)}")
                input("Press enter to continue...")
            except ValueError as e:
                print("Invalid edge!")
        elif choice == "6":
            try:
                start = int(input("Enter the start node: "))
                end = int(input("Enter the end node: "))
                cost = int(input("Enter the new cost: "))
                if cost < 0:
                    print("The cost cannot be negative!")
                    input("Press enter to continue...")
                    raise ValueError("The cost cannot be negative!")
                if not self.graph.is_edge(start, end):
                    print("The edge does not exist!")
                    input("Press enter to continue...")
                    raise ValueError("The edge does not exist!")
                self.graph.set_cost(start, end, cost)      
            except ValueError as e:
                print("Invalid edge!")
        elif choice == "0":
            pass
        else:
            print("Invalid choice!")

    def start(self):
        while True:
            os.system("cls")
            self.print_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                root = tk.Tk()
                file_path = filedialog.askopenfilename()
                root.withdraw()
                print(file_path)
                self.graph.load_from_file(file_path)
            elif choice == "2":
                try:
                    n = int(input("Enter the number of nodes: "))
                    m = int(input("Enter the number of edges: "))
                    self.graph = generate_random_graph(n, m)
                except ValueError:
                    print("Invalid number!")
            elif choice == "3":
                self.print_modify_menu()
                self.get_modify_option()
            elif choice == "4":
                try:
                    node = int(input("Enter the node: "))
                    if self.graph.is_node(node):
                        print(f"In degree: {self.graph.get_in_degree(node)}")
                        print(f"Out degree: {self.graph.get_out_degree(node)}")
                        input("Press enter to continue...")
                    else:
                        print("Invalid node!")
                except ValueError:
                    print("Invalid node!")
            elif choice == "8":
                filename = input("Enter the name of the savefile (without.txt): ")
                self.graph.save_to_file(filename+ ".txt")
            elif choice == "9":
                self.graph.hidden = not self.graph.hidden
            elif choice == "0":
                break
            else:
                print("Invalid choice!")

def generate_random_graph(n, m):
    graph = Directional_Graph()
    for i in range(n):
        graph.add_empty_node()
    for i in range(m):
        start = random.randint(0, n-1)
        end = random.randint(0, n-1)
        while graph.is_edge(start, end):
            start = random.randint(0, n-1)
            end = random.randint(0, n-1)
        cost = random.randint(1, 100)
        graph.add_edge(start, end, cost)
    return graph


if __name__ == "__main__":
    graph = Directional_Graph()
    ui = UI(graph)
    ui.start()      