class object:
    def __init__(self, id, size):
        self.refcount = 0
        self.id = id
        self.size = size
        self.outgoing_ref = []
        self.ongoing_ref = []

        self.alive = True
        self.marked = False

    def increment(self):
        self.refcount += 1

    def decrement(self):
        self.refcount -= 1

    def initref(self):
        self.refcount = 0

    def initref2(self):
        self.refcount = 1

    def addref(self, obj):
        if obj not in self.outgoing_ref:
            self.outgoing_ref.append(obj)
            if self not in obj.ongoing_ref:
                obj.ongoing_ref.append(self)

    def removeref(self, obj):
        if obj in self.outgoing_ref:
            self.outgoing_ref.remove(obj)
        if self in obj.ongoing_ref:
            obj.ongoing_ref.remove(self)

    def isreferced(self, obj):
        return obj in self.outgoing_ref

    def get_id(self):
        return self.id



rootset = []
heap = {}


def FREE(obj):
    if obj is None or not obj.alive or obj.refcount != 0:
        return

    obj.alive = False


    while obj.id in rootset:
        rootset.remove(obj.id)


    refs = list(obj.outgoing_ref)
    obj.outgoing_ref.clear()
    for other in refs:
        if obj in other.ongoing_ref:
            other.ongoing_ref.remove(obj)
        if other.alive:
            other.decrement()
            if other.refcount == 0:
                FREE(other)
    obj.ongoing_ref.clear()


def ALLOC(id, size):
    a = object(id, size)
    if id in rootset:
        a.initref2()
    else:
        a.initref()
    heap[id] = a
    return a


def REF(src, dst):
    if src is None or dst is None:
        return
    if not src.alive or not dst.alive:
        return

    if not src.isreferced(dst):
        src.addref(dst)
        dst.increment()


def DELREF(src, dst):
    if src is None or dst is None:
        return
    if not src.alive or not dst.alive:
        return

    if src.isreferced(dst):
        src.removeref(dst)
        dst.decrement()
        if dst.refcount == 0:
            FREE(dst)


def ADDroot(obj):
    if obj is None or not obj.alive:
        return
    rootset.append(obj.id)
    obj.increment()


def DELroot(obj):
    if obj is None or not obj.alive:
        return
    if obj.id in rootset:
        rootset.remove(obj.id)
    obj.decrement()
    if obj.refcount == 0:
        FREE(obj)


def solve_p1(input):
    global rootset, heap

    lines = [line.strip() for line in input.splitlines() if line.strip()]
    if len(lines) < 2:
        return 0

    _n, r, _k = map(int, lines[0].split())
    rootset = [int(x) for x in lines[1].split()] if lines[1] else []
    heap = {}

    for line in lines[2 : 2 + r]:
        parts = line.split()
        op = parts[0]

        if op == "ALLOC":
            ALLOC(int(parts[1]), int(parts[2]))
        elif op == "REF":
            src = heap.get(int(parts[1]))
            dst = heap.get(int(parts[2]))
            REF(src, dst)
        elif op == "DELREF":
            src = heap.get(int(parts[1]))
            dst = heap.get(int(parts[2]))
            DELREF(src, dst)
        elif op == "ADDROOT":
            obj = heap.get(int(parts[1]))
            ADDroot(obj)
        elif op == "DELROOT":
            obj = heap.get(int(parts[1]))
            DELroot(obj)

    return sum(obj.size for obj in heap.values() if obj.alive)



def gc(heap, rootset):
    for obj in heap.values():
        obj.marked = False

    stack = []
    for rid in list(rootset):
        root_obj = heap.get(rid)
        if root_obj is not None and root_obj.alive and not root_obj.marked:
            root_obj.marked = True
            stack.append(root_obj)

    while stack:
        cur = stack.pop()
        for dst in cur.outgoing_ref:
            if dst.alive and not dst.marked:
                dst.marked = True
                stack.append(dst)

    dead = [obj for obj in heap.values() if obj.alive and not obj.marked]

    for obj in dead:
        obj.alive = False
        while obj.id in rootset:
            rootset.remove(obj.id)

    for obj in dead:
        
        for dst in list(obj.outgoing_ref):
            if obj in dst.ongoing_ref:
                dst.ongoing_ref.remove(obj)
        obj.outgoing_ref = []

    
        for src in list(obj.ongoing_ref):
            if obj in src.outgoing_ref:
                src.outgoing_ref.remove(obj)
        obj.ongoing_ref = []


def solve_p2(input):
    lines = [line.strip() for line in input.splitlines() if line.strip()]
    if len(lines) < 2:
        return 0

    n, r, k = map(int, lines[0].split())
    initial_roots = [int(x) for x in lines[1].split()] if lines[1] else []

    p2_heap = {}

    p2_rootset = list(initial_roots)

    mutated = False
    effective_ops = 0
    for line in lines[2 : 2 + r]:
        parts = line.split()
        op = parts[0]
        if op == "ALLOC":
            obj_id = int(parts[1])
            size = int(parts[2])
            o = object(obj_id, size)
            p2_heap[obj_id] = o
            if obj_id in initial_roots:
    
                pass
                
        elif op == "REF":
            src = p2_heap.get(int(parts[1]))
            dst = p2_heap.get(int(parts[2]))
            if src is not None and dst is not None and src.alive and dst.alive:
                if dst not in src.outgoing_ref:
                    src.outgoing_ref.append(dst)
                    src.referced = src.outgoing_ref
                    if src not in dst.ongoing_ref:
                        dst.ongoing_ref.append(src)
                    mutated = True

        elif op == "DELREF":
            src = p2_heap.get(int(parts[1]))
            dst = p2_heap.get(int(parts[2]))
            if src is not None and dst is not None and src.alive and dst.alive:
                if dst in src.outgoing_ref:
                    src.outgoing_ref.remove(dst)
                    if src in dst.ongoing_ref:
                        dst.ongoing_ref.remove(src)
                    mutated = True

        elif op == "ADDROOT":
            obj = p2_heap.get(int(parts[1]))
            if obj is not None and obj.alive:
                p2_rootset.append(obj.id)
                mutated = True

        elif op == "DELROOT":
            obj = p2_heap.get(int(parts[1]))
            if obj is not None and obj.alive:
                if obj.id in p2_rootset:
                    p2_rootset.remove(obj.id)
                mutated = True

        if mutated:
            effective_ops += 1
            if k > 0 and effective_ops % k == 0:
                gc(p2_heap, p2_rootset)

    p2 = sum(obj.size for obj in p2_heap.values() if obj.alive)
    p1 = solve_p1(input)
    return p2 * 1000000 + abs(p2 - p1)

if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as f:
        content = f.read()
    result = solve_p1(content)
    result2 = solve_p2(content)
    print(result)
    print(result2)
