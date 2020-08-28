import queue, itertools, matplotlib.pyplot as plt, sys

adj_list = {}
parent = {}
bfs = {}
shared_sides = {}
delaunay_list = []
coors_list = []

def main():

    tests = ["5nodes_qhull.txt", "5nodes_rbox.txt"]

    if len(sys.argv) == 1:
        test1 = tests[0]
        test2 = tests[1]
    elif len(sys.argv) == 3:
        test1 = sys.argv[1]
        test2 = sys.argv[2]


    f = open(test1, "r")
    for line in f:
        line = line.split()
        delaunay_list.append(line)

    g = open(test2, "r")
    for line in g:
        line = line.split()
        coors_list.append(line)

    delaunay_list.pop(0)
    # delaunay_list.append(['0', '1', '2'])


    for x in range(len(delaunay_list)):
        for y in range(len(delaunay_list[x])):
            key = delaunay_list[x][y]
            first = delaunay_list[x][(y + 1) % len(delaunay_list[x])]
            second = delaunay_list[x][(y + 2) % len(delaunay_list[x])]

            adj_list.setdefault(key, [])
            if (first not in adj_list[key]) and (second not in adj_list[key]):
                adj_list[key].append(first)
                adj_list[key].append(second)
            elif first not in adj_list[key]:
                adjacent = adj_list[key]
                adj_list[key].insert(adjacent.index(second), first)
            elif second not in adj_list[key]:
                adjacent = adj_list[key]
                adj_list[key].insert(adjacent.index(first) + 1, second)

            # finds triangles that share sides
            a = delaunay_list[x][y]
            b = delaunay_list[x][(y + 1) % len(delaunay_list[x])]
            side = min(a, b) + max(a, b)
            shared_sides.setdefault(side, [])
            shared_sides[side].append(delaunay_list[x])

    q = queue.Queue()
    bfs.setdefault('r', [])
    visitedBFS = set()

    for m in range(3):
        q.put(str(m))
        visitedBFS.add(str(m))
        bfs['r'].append(str(m))

    while not q.empty():
        next = q.get()
        children = adj_list.get(next)
        for i in range(len(children)):
            if not visitedBFS.__contains__(children[i]):
                # bfs and keeping track of parent for backtracking
                bfs.setdefault(next, [])
                bfs[next].append(children[i])
                parent[children[i]] = next

                visitedBFS.add(children[i])
                q.put(children[i])

    p1 = ['0']
    p2 = ['1']
    p3 = ['2']

    sperner_triangle(p1, p2, p3)


def sperner_triangle(p1, p2, p3):
    q = queue.Queue()
    visited = set()
    colour_path = {}

    for i in range(len(p1)):
        q.put(p1[i])
        visited.add(p1[i])
        colour_path[p1[i]] = 'ro'

    for i in range(len(p2)):
        q.put(p2[i])
        visited.add(p2[i])
        colour_path[p2[i]] = 'bo'

    for i in range(len(p3)):
        q.put(p3[i])
        visited.add(p3[i])
        colour_path[p3[i]] = 'go'

    # start search from portal between p1 and p2
    first = p1[-1]
    second = p2[0]

    col1 = colour_path[first]
    col2 = colour_path[second]
    col3 = 'x'

    while((col3 != col1) or (col3 != col2)):
        side = min(first, second) + max(first, second)
        for x in shared_sides[side]:
            if ((x.index(first) + 1) % len(x)) == x.index(second):
                next_tri = x
            elif ((first is '0' or first is '1' or first is '2') and
                 (second is '0' or second is '1' or second is '2')):
                next_tri = shared_sides[side][0]
                if next_tri[(next_tri.index(first)+1)% len(next_tri)] != second:
                    temp = first
                    first = second
                    second = temp

                    temp = col1
                    col1 = col2
                    col2 = temp

        third = next_tri[(next_tri.index(first) + 2) % len(next_tri)]

        # colours all nodes in path from third node to nearest coloured ancestor
        if not colour_path.__contains__(third):
            coloured_ancestor = parent[third]
            nodes_to_colour = []
            nodes_to_colour.append(third)

            while not colour_path.__contains__(coloured_ancestor):
                nodes_to_colour.append(coloured_ancestor)
                coloured_ancestor = parent[coloured_ancestor]

            col3 = colour_path[coloured_ancestor]
            for x in range(len(nodes_to_colour)):
                colour_path[nodes_to_colour[x]] = col3
        else:
            col3 = colour_path[third]
        # all three nodes are different colours
        if col1 != col2 and col1 != col3 and col2 != col3:
            spr_tri = next_tri
            print(spr_tri)

            # draws graph
            for x in range(len(delaunay_list)):
                idx1 = int(delaunay_list[x][0])
                idx2 = int(delaunay_list[x][1])
                idx3 = int(delaunay_list[x][2])

                plt.plot([float(coors_list[idx1][0]), float(coors_list[idx2][0]),
                          float(coors_list[idx3][0]), float(coors_list[idx1][0])],
                         [float(coors_list[idx1][1]), float(coors_list[idx2][1]),
                          float(coors_list[idx3][1]), float(coors_list[idx1][1])], 'm-')

                # nodes not coloured in path are black
                plt.plot(float(coors_list[idx1][0]), float(coors_list[idx1][1]),
                         colour_path[str(idx1)] if colour_path.__contains__(str(idx1)) else 'ko')
                plt.plot(float(coors_list[idx2][0]), float(coors_list[idx2][1]),
                         colour_path[str(idx2)] if colour_path.__contains__(str(idx2)) else 'ko')
                plt.plot(float(coors_list[idx3][0]), float(coors_list[idx3][1]),
                         colour_path[str(idx3)] if colour_path.__contains__(str(idx3)) else 'ko')

                # sperner triangle coloured cyan
                plt.plot([float(coors_list[int(first)][0]), float(coors_list[int(second)][0]),
                          float(coors_list[int(third)][0]), float(coors_list[int(first)][0])],
                         [float(coors_list[int(first)][1]), float(coors_list[int(second)][1]),
                          float(coors_list[int(third)][1]), float(coors_list[int(first)][1])], 'c-')
            plt.show()

            break
        elif col3 != col1:
            second = third
            col2 = col3
        elif col3 != col2:
            first = third
            col1 = col3

    path = {}
    bounds = p1 + p2 + p3

    for i in range(len(spr_tri)):
        curr = spr_tri[i]
        path.setdefault(i, [curr])
        while (not bounds.__contains__(curr)):
            path[i].append(parent[curr])
            curr = parent[curr]

    # last sperner triangle
    if(len(path[0])==1 and len(path[1])==1 and len(path[2])==1):
        return 0
    elif len(path[0]) + len(path[1]) + len(path[2]) <= 4:
        return 0

    # making new paths for next recursive step
    for i in range(len(path)):
        temp1 = path[i]
        temp2 = path[(i+1)%len(path)]
        p1rec = temp1[0:-1]

        if bounds.index(temp1[-1]) < bounds.index(temp2[-1]):
            p2rec = bounds[bounds.index(temp1[-1]):bounds.index(temp2[-1]) + 1]
        else:
            p2rec = bounds[bounds.index(temp1[-1]):]
            p2rec.extend(bounds[0:bounds.index(temp2[-1])+1])

        temp2 = temp2[0:-1]
        p3rec = temp2
        p3rec.reverse()

        if len(p1rec)==0:
            p1rec.append(p2rec.pop(0))
        if len(p3rec) == 0:
            p3rec.append(p2rec.pop(-1))

        # not enough nodes to create new partition
        if len(p1rec) == 0 or len(p2rec) == 0 or len(p3rec) == 0:
            continue

        sperner_triangle(p1rec, p2rec, p3rec)


if __name__ == "__main__":
    main()

