import argparse
import heapq
from datetime import datetime

def write_output(output_file, text: str):
    print(text)
    output_file.write(text + "\n")

def prompt_until_valid(prompt: str, validator, error_msg: str):
    while True:
        value = input(prompt).strip()
        validated = validator(value)
        if validated is not None:
            return validated
        print(error_msg)

def read_input_file(input_filename):
    with open(input_filename, "r") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    if not lines:
        raise ValueError(f"file {input_filename} has no data, program terminated")

    try:
        num_vertices, num_edges = map(int, lines[0].split())
    except Exception:
        raise ValueError("The first line must contain two integers, program terminated")

    edges = []
    for ln in lines[1:]:
        parts = ln.split()
        if len(parts) != 3:
            continue
        try:
            from_node, to_node, edge_weight = map(int, parts)
            edges.append((from_node, to_node, edge_weight))
        except ValueError:
            continue
    return num_vertices, num_edges, edges

def build_adjacency_list(num_vertices, edges, output_file):
    adjacency_list = [[] for _ in range(num_vertices)]
    for from_node, to_node, edge_weight in edges:
        if num_vertices == 0:
            write_output(output_file, f"This is an empty graph - Cannot add edge: {from_node}, {to_node}, {edge_weight}")
            continue
        if from_node < 0 or to_node < 0 or from_node >= num_vertices or to_node >= num_vertices:
            write_output(output_file, f"This is an invalid source or destination vortex - Cannot add edge: {from_node}, {to_node}, {edge_weight} - Request ignored")
            continue
        if edge_weight <= 0:
            write_output(output_file, f"This is an invalid weight - Cannot add edge: {from_node}, {to_node}, {edge_weight} - Request ignored")
            continue
        adjacency_list[from_node].append((to_node, edge_weight))
        adjacency_list[to_node].append((from_node, edge_weight))
        write_output(output_file, f"Edge Added: {from_node}, {to_node}, {edge_weight}")
        write_output(output_file, f"Edge Added: {to_node}, {from_node}, {edge_weight}")
    return adjacency_list

def print_adjacency_list(adjacency_list, output_file, title):
    write_output(output_file, title)
    for i, neighbors in enumerate(adjacency_list):
        line = f"Adj[{i}] -> " + " ".join(f"({to_node}, {cost})" for to_node, cost in neighbors)
        write_output(output_file, line)

def compute_mst(num_vertices, adjacency_list, output_file):
    if num_vertices == 0:
        write_output(output_file, "This is an empty graph - No MST")
        return

    visited = [False] * num_vertices
    priority_queue = [(0, 0, -1)]
    mst_adjacency_list = [[] for _ in range(num_vertices)]
    total_cost = 0

    write_output(output_file, "Minimum Spanning Tree")

    while priority_queue and sum(visited) < num_vertices:
        edge_weight, to_node, from_node = heapq.heappop(priority_queue)
        if visited[to_node]:
            continue
        visited[to_node] = True
        if from_node != -1:
            write_output(output_file, f"Edge: {to_node} - {from_node} weight: {edge_weight}")
            total_cost += edge_weight
            mst_adjacency_list[from_node].append((to_node, edge_weight))
            mst_adjacency_list[to_node].append((from_node, edge_weight))
        for neighbor, cost in adjacency_list[to_node]:
            if not visited[neighbor]:
                heapq.heappush(priority_queue, (cost, neighbor, to_node))

    write_output(output_file, f"Total cost of MST: {total_cost}")
    print_adjacency_list(mst_adjacency_list, output_file, "MST Graph - Adjacency List")

def main():
    parser = argparse.ArgumentParser(description="MST Test Program (Prim's Algorithm)")
    parser.add_argument("-i", "--input", help = "Input graph file (.dat)")
    parser.add_argument("-o", "--output", help = "Output results file (.out)")
    args = parser.parse_args()

    print("Welcome to the MST Test Program")

    if args.output:
        output_filename = args.output
    else:
        default_out = f"MST_{datetime.now().strftime('%Y%m%d_%H%M%S')}.out"
        output_filename = input(f"Enter an output file name or press enter for default '{default_out}'): ").strip()
        if output_filename == "":
            output_filename = default_out

    while True:
        try:
            output_file = open(output_filename, "w", encoding = "utf-8")
            break
        except OSError as e:
            print(f"file {output_filename} cant be opened - {e.strerror}. Please try again.")
            output_filename = input("Enter another output file name: ")

    write_output(output_file, "Welcome to the MST Test Program")

    write_output(output_file, "Testing the Default Scenario")
    compute_mst(0, [], output_file)

    input_filename = args.input or input("Enter a file name for the graph data: ")

    while True:
        try:
            num_vertices, num_edges, edges = read_input_file(input_filename)
            break
        except FileNotFoundError:
            print(f"The file {input_filename} cant be opened or does not exist - please try again the program is terminated")
            input_filename = input("Enter a file name for the graph data: ")
        except ValueError as ve:
            print(f"{ve} please try again")
            input_filename = input("Enter a file name for the graph data: ")

    write_output(output_file, "Testing the file data")
    write_output(output_file, f"The file name for the graph data: {input_filename}")

    if num_vertices < 0:
        write_output(output_file, f"Error: number of vertices: {num_vertices} is less than zero")
        write_output(output_file, "An empty graph will be created")
        compute_mst(0, [], output_file)
    elif num_vertices == 0 or num_edges < num_vertices - 1:
        write_output(output_file, f"Error: {num_edges} edges invalid to create a connected graph")
        write_output(output_file, "An empty graph will be created")
        compute_mst(0, [], output_file)
    else:
        write_output(output_file, f"A graph with {num_vertices} and {num_edges} will be created")
        write_output(output_file, f"The number of input edges to process is: {num_edges}")
        adjacency_list = build_adjacency_list(num_vertices, edges, output_file)
        print_adjacency_list(adjacency_list, output_file, "Full Graph - Adjacency List")
        compute_mst(num_vertices, adjacency_list, output_file)

    write_output(output_file, "Thank you for running the MST Test Program written by Shafaq Alhusseini!")
    output_file.close()

if __name__ == "__main__":
    main()
