from tsp import *
from time import sleep, time
from os import name, system


def read_tsplib(path):
    f=open(path, 'r')
    rows=f.readlines()
    f.close()
    instance=set()
    for start in range(len(rows)):
        if rows[start]=="NODE_COORD_SECTION\n": break
    for i in range(start+1, len(rows)-(1 if "EOF" in rows[-1] else 0)):
        cols=rows[i].split(" ")
        n, x, y=int(cols[0]), float(cols[1]), float(cols[2])
        instance.add(City(y, x, f"C{n}"))
    return instance


def find_p_nearest_neighbours(instance, p):
    counter=[1]
    def find_p_nearest_neighbours_to_city(instance1, city, p1, counter):
        output = list()
        print(f"City {counter} of {len(instance1)}\n{counter[0]/len(instance)*100} %")
        counter[0]+=1
        for city_to_compare in sorted(list(instance1), key=lambda x: x.name):
            if city_to_compare == city: continue

            dist = distance(city, city_to_compare)
            
            if len(output)<p1:
                output.append((dist, city_to_compare))
                if len(output)==p: output=sorted(output, key=lambda x: x[0])
            elif dist<output[-1][0]:
                del output[-1]
                for i in range(len(output), 0, -1):
                    if dist>=output[i-1][0]: output.insert(i, (dist, city_to_compare)); break
        return {o[1] for o in output}
    return {city: find_p_nearest_neighbours_to_city(instance, city, p, counter) for city in instance}


def partial_cost(X, Y, square_distance_flag=False):
    if len(X)!=len(Y): raise Exception(f"ERROR: X has {len(X)} element, while Y has {len(Y)} elements)")
    return sum(distance(Y[i][0], Y[i][1])-distance(X[i][0], X[i][1]) for i in range(len(X)))
    

def lin_kernighan_recursion(tour, neighbours, old_X, old_Y, old_cost):
    x1=old_X[-1]
    for city_y1, _ in sorted([(c, partial_cost([(c, tour.pred(c)), (c, c)], [(c, x1[1]), (x1[0], tour.pred(c))])) for c in neighbours[x1[1]]], key=lambda z: z[1]):
        if city_y1==tour.pred(x1[1]): continue # probably to fix the condition
        y1=(x1[1], city_y1)
        if y1 in old_X+old_Y or tuple(reversed(y1)) in old_X+old_Y: continue
        for c3, v, _ in sorted([(tour.pred(y1[1]), True, distance(y1[1], tour.pred(y1[1]))), (tour.succ(y1[1]), False, distance(y1[1], tour.succ(y1[1])))], key=lambda z: z[2], reverse=True):
            if c3==old_X[0][0]: continue
            x2=(y1[1], c3)
            if x2 in old_X+old_Y or tuple(reversed(x2)) in old_X+old_Y: continue
            y2=(x2[1], old_X[0][0])
            if (y2[1]==tour.pred(x2[1]) and v) or (y2[1]==tour.succ(x2[1]) and not v) : continue
            if y2 in old_X+old_Y or tuple(reversed(y2)) in old_X+old_Y: continue
            if not lin_kernighan_check_exchange(tour, old_X+[x2], old_Y[:-1]+[y1, y2]): continue
            cost=old_cost+partial_cost([old_Y[-1]]+[x2], [y1, y2])
            if cost>=0: continue
            best_X, best_Y, best_cost=lin_kernighan_recursion(tour, neighbours, old_X+[x2], old_Y[:-1]+[y1, y2], cost)
            if best_cost<cost: return best_X, best_Y, best_cost # <= ?
            return old_X+[x2], old_Y[:-1]+[y1, y2], cost
    return old_X, old_Y, old_cost


def lin_kernighan_move(tour, neighbours):
    for city_x1 in tour.list:
        x1=(city_x1, tour.succ(city_x1))
        for city_y1, _ in sorted([(c, partial_cost([(c, tour.pred(c)), (c, c)], [(c, x1[1]), (x1[0], tour.pred(c))])) for c in neighbours[x1[1]]], key=lambda z: z[1]):
            y1=(x1[1], city_y1)
            x2=(y1[1], tour.pred(y1[1]))
            y2=(x2[1], x1[0])
            if y1[1]==x1[0] or y1[1]==tour.succ(x1[1]): continue
            cost=partial_cost([x1, x2], [y1, y2])
            if cost>=0: continue
            return lin_kernighan_recursion(tour, neighbours, [x1, x2], [y1, y2], cost)[:2]
    return [], []


def lin_kernighan_check_exchange(tour, X, Y):
    new_tour=tour.copy()
    c1=new_tour.index(X[0][0])
    new_tour.shift(c1)
    c1, c2=0, 1
    for i in range(len(X)-1):
        idx, temp=new_tour.succ(X[i+1][0], index=True)
        if temp==X[i+1][1]:
            c3, c4=idx-1, idx
        else:
            c3, c4=idx-2, idx-1
        # c3, c4=tuple(sorted((new_tour.index(X[i+1][1]), new_tour.index(X[i+1][0]))))
        segment1=new_tour.list[:c2]
        segment2=new_tour.list[c2:c4]
        segment3=new_tour.list[c4:]
        segment2.reverse()
        new_tour.list=segment1+segment2+segment3
    for i in range(len(X)):
        if X[i][1]==new_tour.succ(X[i][0]) or X[i][1]==new_tour.pred(X[i][0]):
            return False
    for i in range(len(Y)):
        if Y[i][1]!=new_tour.succ(Y[i][0]) and Y[i][1]!=new_tour.pred(Y[i][0]):
            return False
    return True


def lin_kernighan(instance, tour, p=5, max_iter=100000, verbose=False, animation=False, s_time=0.5, screen=""):
    if animation: plt.ion(); tour.plot(); plt.pause(1.5)
    screen=screen+f"Initial cost: {tour.length()}\n\nFinding {p} nearest neighbours . . . "
    cls()
    print(screen)
    neighbours=find_p_nearest_neighbours(instance, p)
    screen+="DONE\n\nStart local search . . . "
    cls()
    print(screen)
    for i in range(max_iter):
        if not verbose: cls(); print(screen+f"Iteration: {i+1}")
        X, Y = lin_kernighan_move(tour, neighbours)
        if animation: plot_differences(X, Y); plt.pause(s_time);
        old_cost=tour.length()
        gain=partial_cost(X, Y)
        expected_new_cost=old_cost+gain
        if len(X)==0: break
        c1=tour.index(X[0][0])
        tour.shift(c1)
        c1, c2=0, 1
        for j in range(len(X)-1):
            c3, c4=tuple(sorted((tour.index(X[j+1][1]), tour.index(X[j+1][0]))))
            segment1=tour.list[:c2]
            segment2=tour.list[c2:c4]
            segment3=tour.list[c4:]
            segment2.reverse()
            tour.list=segment1+segment2+segment3
        new_cost=tour.length()
        if verbose: print(f"Iteration: {i+1}\t\t{len(X)}-opt move;\t\tNew cost: {new_cost}")
        if abs(new_cost-expected_new_cost)>0.1: raise Exception("ERROR: expected cost not respected")
        if animation: plt.clf(); tour.plot(); plt.pause(s_time)
    else:
        print("Maximum number of iteration reached: tour may be not a local optimum")
    if not verbose:
        cls()
        print(screen[:-2]+"DONE\n")
    print(f"Cost of the best found tour: {tour.length()}")
    plt.ioff()
    return tour


def plot_differences(X, Y):
    for i in range(len(X)):
        x1, x2 = X[i]
        y1, y2 = Y[i]
        plt.plot([x1.x, x2.x], [x1.y, x2.y], 'r-')
        plt.plot([y1.x, y2.x], [y1.y, y2.y], 'g-')
    plt.show()


if __name__=='__main__':
    # instance = generate_random_instance(1686, 100, 100, 2153)
    instance=read_tsplib("qa194.tsp")
    # tour = random_tour(instance, True, 2154)
    tour=nearest_neighbor_algorithm(instance)
    tour.plot()
    tour=lin_kernighan(instance, tour, p=15)
    best_cost=tour.length()
    best_tour=tour.copy()
    print(f"Cost: {best_cost}")
    tour.plot()
    for i in instance:
        tour=nearest_neighbor_algorithm(instance, i)
        tour=random_tour(instance, False)
        tour=lin_kernighan(instance, tour)
        cost=tour.length()
        if cost<best_cost: best_cost=cost; best_tour=tour.copy()
        print(f"Cost: {tour.length()}")
    print(f"Best cost found: {best_cost}")
    best_tour.plot()


def cls():
   # for mac and linux(here, os.name is 'posix')
   if name == 'posix':
      _ = system('clear')
   else:
      # for windows platfrom
      _ = system('cls')


def lk_based_metaheuristic(instance, constructive, cycles=1, loop_initial_city=False, p=5, max_iter=10000, verbose=False, animation=False, s_time=0.5):
    best_tour=None
    best_cost=None
    if loop_initial_city:
        for i, city in enumerate(instance):
            tour=constructive(instance, city)
            tour=lin_kernighan(instance, tour, p, max_iter, verbose, animation, s_time, screen=f"Initial tour number: {i+1}\n\n")
            cost=tour.length()
            if best_cost==None: best_cost=cost; best_tour=tour.copy()
            elif cost<best_cost: best_cost=cost; best_tour=tour.copy()
    else:
        for i in range(cycles):
            tour=constructive(instance)
            tour=lin_kernighan(instance, tour, p, max_iter, verbose, animation, s_time, screen=f"Initial tour number: {i+1}\n\n")
            cost=tour.length()
            if best_cost==None: best_cost=cost; best_tour=tour.copy()
            elif cost<best_cost: best_cost=cost; best_tour=tour.copy()
    return best_tour




"""
- loop unitl stopping criterion broken:
    - r = 2
    - loop:
        - try r-opt move
        - check criterion to increase r

r-opt move:
    - set X and Y constructed element by element
    - criterion:
        - sequential exchange: x_1=(t_1, t_2), y_1=(t_2, t_3), ..., x_r=(t_2r-1, t_2r), y_r=(t_2r, t_1)
        - feasibility: for i>=2, x_i=(t_2i-1, t_2i) chosen s.t. if (t_2i, t_1) is added, it is a tour
        MODIFIED - negative partial cost: for all i, G_i = c(y_i)-c(x_i)+c(y_i-1)-c(x_i-1)+...+c(y_1)-c(x_1) < 0
        - X and Y disjoint

    - search rules:
        - limit the search for (t_2i, t_2i+1) to the p (5) nearest neighbours to t_2i
        TO DO (MAYBE NOT) - for i>=4 no link x_i must be broken if it is common to 2-5 solution tours
        - search for improvement stopped if current tour is the same as a previous solution tour

    - priority:
        MODIFIED - for i>=2, if link y_i has to be chosen, each possible choice has priority c(x_i+1)-c(y_i)
        - if there are 2 alternatives for x_4, the one with highest cost is chosen
"""

