# Anil Kumar Ravuru
import random

def print_graph(G_adj_list):
	for i in range(len(G_adj_list)):
		for j in range(len(G_adj_list[0])):
			print(format(G_adj_list[i][j],'2d'),end=' ')
		print()

def print_graph_to_file(G_adj_list):
	with open('sample_graph.txt', 'w') as fp:
		for i in range(len(G_adj_list)):
			fp.write(' '.join(list(map(str, G_adj_list[i]))))
			fp.write('\n')

node_count = int(input('Number of vertices in the graph: '))
G_adj_list = [[0 for i in range(node_count)] for j in range(node_count)]
for i in range(node_count):
	for j in range(i+1, node_count):
		G_adj_list[i][j] = random.randint(1, 100)

if input('Print on terminal? (y/n): ').lower() == 'y':
	print_graph(G_adj_list)
if input('Output into sample_graph.txt? (y/n): ').lower() == 'y':
	print_graph_to_file(G_adj_list)

group_count = int(input('Number of groups in the graph: '))
groups = [[] for i in range(group_count)]
for i in range(node_count):
	groups[random.randint(0, group_count-1)] += [i]

with open('sample_graph_groups.txt', 'w') as fp:
	for x in groups:
		if len(x) != 0:
			fp.write(' '.join(list(map(str, x))))
			fp.write('\n')
