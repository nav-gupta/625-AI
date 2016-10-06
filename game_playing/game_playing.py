import sys


class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children

def print_minimax(root):
    if (root.children == None):
        return
    count = 0;
    for node in root.children:
        count += 1
        if (node.value == root.value):
            print(count, " ")
            print_minimax(node)

def build_node(stack):
    nodes_list = []
    ch = stack.pop()
    while (ch != '('):
        nodes_list.append(ch)
        ch = stack.pop()
    nodes_list.reverse()
    return Node(0, nodes_list)

def parse_tree(tree):
    stack = []
    nums = "0123456789"
    i = 0
    while i < len(tree):
        # print stack
        char = tree[i]
        if char == '(':
            stack.append(char)
        if char == ')':
            stack.append(build_node(stack))
        if char == '-':
            sign = char
            j = i + 1
            number = ""
            while tree[j] in nums:
                number += tree[j]
                j += 1
            i = j - 1
            number = sign + number
            node = Node(int(number))
            stack.append(node)
        if char in nums:
            number = char
            j = i + 1
            while tree[j] in nums:
                number += tree[j]
                j += 1
            i = j - 1
            node = Node(int(number))
            stack.append(node)
        i += 1
    return stack.pop()


def min_value(root, alpha = None, beta = None):
    if root.children == None:
        return root.value
    value = +10000
    for node in root.children:
        value = min(value, max_value(node, alpha, beta))
        if alpha != None:
            if value <= alpha:
                print("MIN cut")
                return value
            beta = min(beta, value)
    root.value = value
    return value


def max_value(root, alpha = None, beta = None):
    if root.children == None:
        return root.value
    value = (-1)*sys.maxsize
    for node in root.children:
        value = max(value, min_value(node, alpha, beta))
        if alpha != None:
            if value >= beta:
                print("MAX cut")
                return value
            alpha = max(alpha, value)
    root.value = value
    return value

def minimax(root):
    v = max_value(root)
    return v

def alpha_beta(root):
    v = max_value(root, (-1) * sys.maxsize, sys.maxsize)
    return v

if __name__ == '__main__':
    tree = parse_tree("(((1(4 7)) (3 ((5 2) (2 8 9) 0 -2) 7 (5 7 1)) (8 3)) (((8 (9 3 2) 5) 2 (9 (3 2) 0)) ((3 1 9) 8 (3 4))))")
    print("\n mini - max \n")
    minimax_value = minimax(tree)
    print(minimax_value)
    print_minimax(tree)
    print("\n alpha - beta \n")
    print(alpha_beta(tree))
    print("\n next \n")

    tree = parse_tree("((11 22 33) (44 55 66))")
    print("\n mini - max \n")
    minimax_value = minimax(tree)
    print(minimax_value)
    print_minimax(tree)
    print("\n alpha - beta \n")
    print(alpha_beta(tree))

