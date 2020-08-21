import queue, itertools, matplotlib.pyplot as plt

adj_list = {}
parent = {}
shared_sides = {}
delaunay_list = []
coors_list = []

def main():

    f = open("5pointDelaunay.txt", "r")
    for line in f:
        line = line.split()
        delaunay_list.append(line)

    g = open("coors_nodes.txt", "r")
    for line in g:
        line = line.split()
        coors_list.append(line)

    numNodes = int(delaunay_list.pop(0)[0])
    delaunay_list.append(['0', '1', '2'])

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

    bounds = p1 + p2 + p3

    while not q.empty():
        next = q.get()
        children = adj_list.get(next)
        colour = colour_path[next]

        if (bounds.__contains__(next)):
            bound1 = bounds[(bounds.index(next)-1)% len(bounds)]
            bound2 = bounds[(bounds.index(next)+1)% len(bounds)]

            if((bound1 is '0' or bound1 is '1' or bound1 is '2') and
                    (bound2 is '0' or bound2 is '1' or bound2 is '2')):
                temp = bound1
                bound1 = bound2
                bound2 = temp

            curr = bound2
            count = 1

            while(curr != bound1):
                curr = children[(children.index(bound2)+count) % len(children)]
                count = count + 1
                if (not visited.__contains__(curr)):
                    parent[curr] = next
                    visited.add(curr)
                    q.put(curr)
                    colour_path[curr] = colour
        else:
            for i in range(len(children)):
                if (not visited.__contains__(children[i])):
                    parent[children[i]] = next
                    visited.add(children[i])
                    q.put(children[i])
                    colour_path[children[i]] = colour


    # draws nodes only within bounds
    for x in range(len(delaunay_list)):
        idx1 = int(delaunay_list[x][0])
        idx2 = int(delaunay_list[x][1])
        idx3 = int(delaunay_list[x][2])
        if(visited.__contains__(str(idx1)) and visited.__contains__(str(idx2)) and visited.__contains__(str(idx3))):
            plt.plot([float(coors_list[idx1][0]), float(coors_list[idx2][0]), float(coors_list[idx3][0]),
                      float(coors_list[idx1][0])],
                     [float(coors_list[idx1][1]), float(coors_list[idx2][1]), float(coors_list[idx3][1]),
                      float(coors_list[idx1][1])], 'k-')

    for x in visited:
        plt.plot(float(coors_list[int(x)][0]), float(coors_list[int(x)][1]), colour_path[x])
    plt.show()


    # start search from between p1 and p2
    first = p1[-1]
    second = p2[0]

    if ((first is '0' or first is '1' or first is '2') and
            (second is '0' or second is '1' or second is '2')):
        temp = first
        first = second
        second = temp

    col1 = colour_path[first]
    col2 = colour_path[second]
    col3 = 'x'

    while((col3 != col1) or (col3 != col2)):
        side = min(first, second) + max(first, second)
        for x in shared_sides[side]:
            if((x.index(first) + 1) % len(x)) == x.index(second):
                spr_tri = x

        third = spr_tri[(spr_tri.index(first) + 2) % len(spr_tri)]
        col1 = colour_path[first]
        col2 = colour_path[second]
        col3 = colour_path[third]

        if col1 != col2 and col1 != col3 and col2 != col3:
            print(spr_tri)
            break
        elif col3 != col1:
            second = third
        elif col3 != col2:
            first = third


    path = {}
    for i in range(len(spr_tri)):
        curr = spr_tri[i]
        path.setdefault(i, [curr])
        while (not bounds.__contains__(curr)):
            path[i].append(parent[curr])
            curr = parent[curr]

    # last sperner triangle
    if(len(path[0])==1 and len(path[1])==1 and len(path[2])==1):
        return 0

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

        if len(p1rec)==0 or len(p2rec)==0 or len(p3rec)==0:
            continue

        sperner_triangle(p1rec, p2rec, p3rec)


if __name__ == "__main__":
    main()

