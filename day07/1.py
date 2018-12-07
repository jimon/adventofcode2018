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

visited = []
while set(nodes) != all_values:
    stack_sorted = sorted(list(stack), key=lambda x: ord(x))
    #print(stack_sorted)
    if len(stack_sorted) == 0:
        break

    head = None
    for x in stack_sorted:
        if can_I_visit_this(x, visited, req):
            head = x
            break

    if head is None:
        print('?')
        break

    if head not in visited:
        visited.append(head)
    stack.remove(head)
    stack.update(graph[head])

print(''.join(visited))
#print('2', 'CABDFE')