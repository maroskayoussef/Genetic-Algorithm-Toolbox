def format_solution(problem, routes):
    depot = problem.depot
    total_distance = 0
    total_load = 0
    blocks = []

    for vehicle_id, route in enumerate(routes):
        if not route:                       # unused vehicle, skip it
            continue

        route_distance = problem.route_distance(route)
        route_load = 0

        # the depot is printed first with load 0
        text = f"Route for vehicle {vehicle_id}:\n"
        text += f" {depot} Load({route_load}) -> "
        for customer in route:
            route_load += problem.demands[customer]   # load after pickup
            text += f" {customer} Load({route_load}) -> "
        text += f" {depot} Load({route_load})\n"      # back at the depot
        text += f"Distance of the route: {route_distance}m\n"
        text += f"Load of the route: {route_load}\n"

        blocks.append(text)
        total_distance += route_distance
        total_load += route_load

    lines = [f"Objective: {total_distance}"]
    lines += blocks
    lines.append(f"Total distance of all routes: {total_distance}m")
    lines.append(f"Total load of all routes: {total_load}")
    return "\n".join(lines)


def print_solution(problem, routes, feasible=True):
    """Print the solution, with a warning if it breaks a constraint."""
    if not feasible:
        print("WARNING: this solution is NOT feasible "
              "(a vehicle is over capacity).\n")
    print(format_solution(problem, routes))