import pulp
import time
from datetime import datetime, timedelta
from db_controller import Db_controller

def get_itinerary(day, budget, ids):
    # Query to db to get stands
    db = Db_controller()
    stands = db.get_stands(ids)
    # Generate costs, times, starts and ends arrays
    costs = []
    times = []
    starts = []
    ends = []
    for stand in stands:
        costs.append(10)
        #costs.append(stand[1])
        #times.append(stand[2])
        times.append(10)
        #values = str(stand[3]).split(':') 
        #start_minutes = int(values[0])*60 + int(values[1])
        #starts.append(start_minutes)
        #values = str(stand[4]).split(':') 
        #end_minutes = int(values[0])*60 + int(values[1])
        #ends.append(end_minutes)
        starts.append(8*60)
        ends.append(24*60)

    # Generate distance matrix
    distances = db.get_stands_distances(stands)

    # Define additional parameters
    medspeed = 300

    return solve_itinera(stands, int(budget), costs, distances, times, starts, ends, medspeed)
    
def solve_itinera(stands, budget, c, d, t, s, e, medspeed=60, simplified=True):


    n = len(stands)
    problem = pulp.LpProblem("Double-indexed MILP", pulp.LpMinimize)

    start = time.time()
    # Define decision variables
    x = pulp.LpVariable.dicts("x", [(i,j) for i in range(n) for j in range(n)], cat=pulp.LpBinary)
    z = pulp.LpVariable.dicts("z", [(i,j) for i in range(n) for j in range(n)], cat=pulp.LpBinary)

    # Define objective function
    problem += pulp.lpSum(z[i,j]*d[i][j] for i in range(n) for j in range(n))

    # Define constraints

    # Constraint: a stand is visited only once
    for i in range(n):
        problem += pulp.lpSum(x[i,j] for j in range(n)) == 1

    # Constraint: at a certain position there's only one stand
    for j in range(n):
        problem += pulp.lpSum(x[i,j] for i in range(n)) == 1

    # Constraint: a certain position can be occupied only if the previous one is occupied too
    #print("Defining stand constraint 3")
    #for i in range(n):
    #    for j in range(1,n):
    #        problem += x[i,j] <= pulp.lpSum(x[k,j-1] for k in range(n))

    # Constraint: the sum of the visited stands must be lower or equal to the turist budget
    #print("Defining stand constraint 4")
    #problem += pulp.lpSum(x[i,j]*int(c[i]) for i in range(n) for j in range(n)) <= budget

    # Constraint: conditional constraint for linearly implementing AnD 
    #print("Defining stand constraint 5")
    #for i in range(n):
    #    for k in range(n):
    #        for j in range(n-1):
    #            problem += z[i,j] >= x[i,j] + x[k, j+1] - 1

    # Constraint: total time constraint

#    print("Defining stand constraint 6")
#    problem += pulp.lpSum(z[i,k]*d[i][k]/medspeed for i in range(n) for k in range(n)) + pulp.lpSum(x[i,j]*t[i] for i in range(n) for j in range(n)) <= 16*60
#

    #if simplified: 
        # Consteaint: time order constraint (start-time) (simplified)
        #print("Defining stand constraint 7 (simplified)")
        #for i in range(n):
        #    for j in range(1,n):
        #        problem += x[i,j]*(s[i] - 10) <= pulp.lpSum(x[m,l]*t[m] + z[m,l]*d[m][l]/medspeed + 8*60 - 10 for m in range(n) for l in range(j-1))

        # Constaint: time order constraint (end-time) (simplified)
        #print("Defining stand constraint 8 (simplified)")
        #for i in range(n):
        #    for j in range(1,n):
        #        problem += x[i,j]*(e[i] + 10 - t[i]) >= pulp.lpSum(x[m,l]*t[m] + z[m,l]*d[m][l]/medspeed for m in range(n) for l in range(j-1))

    # Solve problem
    print("Solving")
    problem.solve()


    end = time.time()

    # Print solution
    itinerary = [0 for _ in range(n)]
    actual_stands = 0

    for i in range(n):
        for j in range(n):
            if x[i,j].value() == 1:
                actual_stands+=1
                itinerary[j] = stands[i][0]

    print(f'Itinerary lenght: {actual_stands}')
    print(f'Actual required time: {end-start}')    
    print(stands)
    return str(itinerary[0:actual_stands])[1:-1]
