import re

p = re.compile(r"""Step (.) must be finished before step (.) can begin\.""")

def parse(x):
    k = p.match(x)
    if k is None:
        raise ValueError("invalid '%s'" % (x))
    g = k.groups()
    return (g[0], g[1])

pairs = [parse(x.strip()) for i, x in enumerate(open("input1.txt").readlines())]
all_keys = set([x for x, y in pairs])
all_children = set([y for x, y in pairs])
all_values = all_keys.union(all_children)

graph = {}
for x, y in pairs:
    if y not in all_keys:
        graph[y] = set([])
    if x in graph:
        graph[x].add(y)
    else:
        graph[x] = set([y])

root = set([k for k, v in graph.items() if k not in all_children])

def rev_traverse(node):
    r = set([k for k, v in graph.items() if node in v])
    r2 = set([])
    for x in r:
        r2 = r2.union(rev_traverse(x))
    return r.union(r2)
req = {k: rev_traverse(k) for k in graph.keys()}
#print(req)

stack = set([k for k, v in graph.items() if k not in all_children])
nodes = []

def can_I_visit_this(node, visited, req):
    for x in req[node]:
        if x not in visited:
            return False
    return True


def upd_worker(worker):
    ind = worker[0]
    node = worker[1]
    tim = worker[2]
    if node is None or tim is None:
        return (ind, None, None)
    if tim <= 1:
        visited2.append(node)
        return (ind, None, None)
    return (ind, node, tim - 1)

visited2 = []

workers = [(i, None, None) for i in range(0, 5)]
kk = 0


visited = []
total_time = 0
while set(visited2) != all_values:

    if len([x for x in workers if x[2] is not None]) > 0:
        total_time += 1

    workers = [upd_worker(x) for x in workers]
    print(workers)
    

    free_workers = [x for x in workers if x[1] is None]

    #if kk > 20:
    #    break

    kk = 0
    while len(free_workers) > 0:
        kk += 1
        if kk > 100:
            break

        stack_sorted = sorted(list(stack), key=lambda x: ord(x))
        if len(stack_sorted) == 0:
            break
        
        head = None
        for x in stack_sorted:
            if can_I_visit_this(x, visited2, req):
                head = x
                break

        if head is None:
            break

        worker = free_workers[0]
        workers[worker[0]] = (worker[0], head, ord(head) - ord('A') + 60 + 1)
        print(workers[worker[0]])

        if head not in visited:
            visited.append(head)
        stack.remove(head)
        stack.update(graph[head])

        free_workers = [x for x in workers if x[1] is None]


#print(''.join(visited))
print(''.join(visited2))
print(total_time)
#print('2', 'CABDFE')