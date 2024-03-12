def dfs(graph, start, end, path=[]):
    """
    使用深度优先搜索(DFS)找到图中从start到end的所有路径。
    graph: 图的邻接表表示。
    start: 起始节点。
    end: 目标节点。
    path: 当前路径（在递归调用中使用）。
    """
    # 将当前节点添加到路径中
    path = path + [start]

    # 如果当前节点是目标节点，则找到一条路径
    if start == end:
        return [path]

        # 递归地遍历当前节点的邻居
    paths = []
    for neighbor in graph[start]:
        if neighbor not in path:  # 避免环路
            newpaths = dfs(graph, neighbor, end, path)
            for newpath in newpaths:
                paths.append(newpath)

    return paths


# 示例：五个节点的Full Mesh网络
# 使用邻接表表示图，每个节点都与其他所有节点相连
graph = {
    'A': ['A', 'C', 'D', 'E'],
    'B': ['A', 'C', 'D', 'E'],
    'C': ['A', 'B', 'D', 'E'],
    'D': ['A', 'C', 'D', 'E'],
    'E': ['A', 'C', 'D', 'E'],
}

# 找到从节点'A'到节点'E'的所有路径
all_paths = dfs(graph, 'A', 'E')

total=0
start=['A','B', 'C', 'D', 'E']
end=['A','B', 'C', 'D', 'E']
for i in range(0,5):
    for j in range(0,5):
        if start[i]!=end[j]:
            all_paths = dfs(graph, start[i], end[j])
            total=total+len(all_paths)
print(total)

# 打印所有路径
# print(len(all_paths))
# for path in all_paths:
#     print(path)