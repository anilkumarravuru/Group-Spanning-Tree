# Anil Kumar Ravuru

from collections import defaultdict 
import math
from functools import reduce


def minDistance(dist, queue):
		minimum = math.inf
		min_index = -1
		for i in range(len(dist)):
			if dist[i] < minimum and i in queue:
				minimum = dist[i]
				min_index = i
		return min_index

def compute_length(parent, order):
	global G_adv_list
	length = 0
	for i in range(1, len(order)):
		length += G_adv_list[order[i]][parent[order[i]]]
	return length

def dijkstra(src):
	global G_adv_list
	global node_count
	global group_count
	dist = [math.inf] * node_count
	parent = [-1] * node_count
	dist[src] = 0
	queue = []
	order = []
	visited_groups = [False] * group_count
	for i in range(node_count):
		queue.append(i)
	while queue:
		u = minDistance(dist, queue)
		order.append(u)
		queue.remove(u)
		for gp in range(group_count):
			if u in groups[gp]:
				visited_groups[gp] = True
			if reduce(lambda x,y: x and y, visited_groups):
				return compute_length(parent, order), order
		for i in range(node_count):
			if G_adv_list[u][i] and i in queue:
				if dist[u] + G_adv_list[u][i] < dist[i]:
					dist[i] = dist[u] + G_adv_list[u][i]
					parent[i] = u
	return compute_length(parent, order), order

# Read Graph
G_adv_list = []
with open('sample_graph.txt', 'r') as lines:
	for line in lines:
		ex = list(map(int, line.split(' ')))
		G_adv_list += [list(map(int, line.split(' ')))]
node_count = len(G_adv_list)

for i in range(node_count-1):
	for j in range(i+1, node_count):
		if G_adv_list[i][j] > 0:
			G_adv_list[j][i] = G_adv_list[i][j]

# Read Groups
groups = []
min_degree, min_degree_group = node_count, 0
with open('sample_graph_groups.txt', 'r') as lines:
	line_no = 0
	for line in lines:
		ex = list(map(int, line.split(' ')))
		groups += [ex]
		if min_degree > len(ex):
			min_degree = len(ex)
			min_degree_group = line_no
		line_no += 1

group_count = len(groups)

start_group = min_degree_group

# Apply Dijkstra’s from every node in start_group
optimal_gst_len = math.inf
optimal_gst_path = []
for st in groups[start_group]:
	temp_gst_length, gst_path = dijkstra(st)
	if temp_gst_length < optimal_gst_len:
		optimal_gst_len = temp_gst_length
		optimal_gst_path = gst_path
print('Optimal GST Length: ', optimal_gst_len)
print('Path: ', optimal_gst_path)

