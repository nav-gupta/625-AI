import sys


class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children


def calc_min(stack):
    min_list_nodes = []
    min_list_values = []
    ch = stack.pop()
    while (ch != '('):
        # print "calc_min", ch
        min_list_nodes.append(ch)
        min_list_values.append(ch.value)
        ch = stack.pop()
    min_value = min(min_list_values)
    min_list_nodes.reverse()
    min_node = Node(min_value, min_list_nodes)
    return min_node


def calc_max(stack):
    max_list_nodes = []
    max_list_values = []
    ch = stack.pop()
    while (ch != '('):
        # print "calc_max", ch
        max_list_nodes.append(ch)
        max_list_values.append(ch.value)
        ch = stack.pop()
    max_value = max(max_list_values)
    max_list_nodes.reverse()
    max_node = Node(max_value, max_list_nodes)
    return max_node


def build_node(stack, depth):
    if (depth % 2) == 0:
        return calc_min(stack)
    else:
        return calc_max(stack)


def print_path(root):
    if (root.children == None):
        return
    count = 0;
    for node in root.children:
        count += 1
        if (node.value == root.value):
            print(count, " ")
            print_path(node)


def parse_tree(tree):
    stack = []
    nums = "0123456789"
    depth = 0
    number = ""
    i = 0
    while i < len(tree):
        # print stack
        char = tree[i]
        if char == '(':
            stack.append(char)
            depth += 1
        if char == ')':
            stack.append(build_node(stack, depth))
            depth -= 1
        if char == '-':
            sign = char
            j = i + 1
            number = ""
            while (tree[j] in nums):
                number += tree[j]
                j += 1
            i = j - 1
            number = sign + number
            node = Node(int(number))
            stack.append(node)
        if char in nums:
            number = char
            j = i + 1
            while (tree[j] in nums):
                number += tree[j]
                j += 1
            i = j - 1
            node = Node(int(number))
            stack.append(node)
        i += 1
    return stack.pop()


def min_value(root, alpha, beta):
    if (root.children == None):
        return root.value
    value = +10000
    for node in root.children:
        value = min(value, max_value(node, alpha, beta))
        if value <= alpha:
            print("MIN cut")
            return value
        beta = min(beta, value)
    return value


def max_value(root, alpha, beta):
    if (root.children == None):
        return root.value
    value = (-1)*sys.maxsize
    for node in root.children:
        value = max(value, min_value(node, alpha, beta))
        if value >= beta:
            print("MAX cut")
            return value
        alpha = max(alpha, value)
    return value


def alpha_beta(root):
    v = max_value(root, (-1) * sys.maxsize, sys.maxsize)
    return v

if __name__ == '__main__':
    node = parse_tree("(((1(4 7)) (3 ((5 2) (2 8 9) 0 -2) 7 (5 7 1)) (8 3)) (((8 (9 3 2) 5) 2 (9 (3 2) 0)) ((3 1 9) 8 (3 4))))")
    print("\n mini - max \n")
    print(node.value)
    print_path(node)
    print("\n alpha - beta \n")
    print(alpha_beta(node))
    print("\n next \n")

    node = parse_tree("((11 22 33) (44 55 66))")
    print("\n mini - max \n")
    print(node.value)
    print_path(node)
    print("\n alpha - beta \n")
    print(alpha_beta(node))

