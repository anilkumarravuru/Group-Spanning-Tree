# Anil Kumar Ravuru

def get_num(num):
	global max_len
	return format(num, '{}d'.format(max_len)).replace(' ', '0')

# Read Graph
G_adv_list = []
with open('sample_graph.txt', 'r') as lines:
	for line in lines:
		G_adv_list += [list(map(int, line.split(' ')))]
node_count = len(G_adv_list)
max_len = len(str(node_count-1))
out_edges = [[] for i in range(node_count)]
for i in range(node_count-1):
	for j in range(i+1, node_count):
		if G_adv_list[i][j] > 0:
			out_edges[i] += [j]
			out_edges[j] += [i]
for i in range(node_count):
	out_edges[i].sort()

# Read Groups
groups = []
with open('sample_graph_groups.txt', 'r') as lines:
	for line in lines:
		groups += [list(map(int, line.split(' ')))]
group_count = len(groups)

# Variables for vertices and edges
s_vars = []
x_vars = []
with open('integral_variables.txt', 'w') as ivp:
	for i in range(node_count):
		s_vars += ['s'+get_num(i)]
		ivp.write('s'+get_num(i)+'\n')
	for i in range(node_count-1):
		for j in range(i+1, node_count):
			if G_adv_list[i][j] > 0:
				x_vars += ['x'+get_num(i)+get_num(j)]
				ivp.write('x'+get_num(i)+get_num(j)+'\n')
	ivp.close()

# Variables for flows
f_vars = []
with open('float_variables.txt', 'w') as fvp:
	flow_vars = []
	for sr in range(group_count-1):
		for si in range(sr+1, group_count):
			if sr != si:
				for i in range(node_count-1):
					for j in range(i+1, node_count):
						if G_adv_list[i][j] > 0:
							f_vars += ['f'+get_num(sr)+get_num(si)+get_num(i)+get_num(j), 'f'+get_num(sr)+get_num(si)+get_num(j)+get_num(i)]
							fvp.write('f'+get_num(sr)+get_num(si)+get_num(i)+get_num(j)+'\n')
							fvp.write('f'+get_num(sr)+get_num(si)+get_num(j)+get_num(i)+'\n')

final_constraints = []

# Integral Constraints for vertices and Edges
for x in s_vars:
	cnst = '(1)({}) <= 1'.format(x)
	final_constraints.append(cnst)

for x in x_vars:
	cnst = '(1)({}) <= 1'.format(x)
	final_constraints.append(cnst)

# Constraint: Atleast one vertex from each group
for grp in groups:
	cnsts = []
	for idx in grp:
		cnsts.append('(1)(s{})'.format(get_num(idx)))
	final_constraints.append('+'.join(cnsts)+' >= 1')

# Choose vertex only if atleast one edge is choosen
for idx in range(node_count):
	neighbor_edges = out_edges[idx]
	ed_cnts = []
	for ed in neighbor_edges:
		temp_edge_cnt = '(-1)(x{}{})'.format(get_num(min(idx, ed)), get_num(max(idx, ed)))
		final_constraints.append('(1)(s{})+'.format(get_num(idx)) + temp_edge_cnt + ' >= 0')
		ed_cnts.append(temp_edge_cnt)
	final_constraints.append('(1)(s{})+'.format(get_num(idx)) + '+'.join(ed_cnts) + ' <= 0')

# Flow constraints
for x in f_vars:
	final_constraints.append('(1)({}) <= 1'.format(x))

# Constraints for edge pick up if there is flow
for x in f_vars:
	fro, to = x[-2*max_len: -max_len], x[-max_len:]
	final_constraints.append('(1)({})+(-1)(x{}{}) <= 0'.format(x, min(fro, to), max(fro, to)))

# Actual flow constraints

for source_group in range(group_count):
	for sink_group in range(source_group+1, group_count):
		if source_group != sink_group:
			for rest in range(group_count):
				if rest == source_group:
					# Source constraints
					source_vertices = groups[source_group]
					out_flow_vars, in_flow_vars = [], []
					for ver in source_vertices:
						for out_ver in out_edges[ver]:
							if out_ver not in source_vertices:
								out_flow_vars.append('f{}{}{}{}'.format(get_num(source_group), get_num(sink_group), get_num(ver), get_num(out_ver)))
								in_flow_vars.append('f{}{}{}{}'.format(get_num(source_group), get_num(sink_group), get_num(out_ver), get_num(ver)))
					temp_flow_cnt = '+'.join(list(map(lambda x: '(1)({})'.format(x), out_flow_vars)))
					temp_flow_cnt += '+' + '+'.join(list(map(lambda x: '(-1)({})'.format(x), in_flow_vars)))
					final_constraints.append(temp_flow_cnt + ' <= 1')
					final_constraints.append(temp_flow_cnt + ' >= 1')
				elif rest == sink_group:
					# Sink constraints
					sink_vertices = groups[sink_group]
					out_flow_vars, in_flow_vars = [], []
					for ver in sink_vertices:
						for out_ver in out_edges[ver]:
							if out_ver not in sink_vertices:
								in_flow_vars.append('f{}{}{}{}'.format(get_num(source_group), get_num(sink_group), get_num(out_ver), get_num(ver)))
								out_flow_vars.append('f{}{}{}{}'.format(get_num(source_group), get_num(sink_group), get_num(ver), get_num(out_ver)))
					temp_flow_cnt = '+'.join(list(map(lambda x: '(1)({})'.format(x), in_flow_vars)))
					temp_flow_cnt += '+' + '+'.join(list(map(lambda x: '(-1)({})'.format(x), out_flow_vars )))
					final_constraints.append(temp_flow_cnt + ' <= 1')
					final_constraints.append(temp_flow_cnt + ' >= 1')
				else:
					# Intermediate constraints
					rest_vertices = groups[rest]
					for ver in rest_vertices:
						in_flow_vars, out_flow_vars = [], []
						for out_ver in out_edges[ver]:
							in_flow_vars.append('f{}{}{}{}'.format(get_num(source_group), get_num(sink_group), get_num(out_ver), get_num(ver)))
							out_flow_vars.append('f{}{}{}{}'.format(get_num(source_group), get_num(sink_group), get_num(ver), get_num(out_ver)))
						temp_flow_cnt = '+'.join(list(map(lambda x: '(1)({})'.format(x), in_flow_vars)))
						temp_flow_cnt += '+' + '+'.join(list(map(lambda x: '(-1)({})'.format(x), out_flow_vars)))
						final_constraints.append(temp_flow_cnt + ' <= 0')
						final_constraints.append(temp_flow_cnt + ' >= 0')


with open('constraints.txt', 'w') as cp:
	for cnt in final_constraints:
		cp.write(cnt)
		cp.write('\n')

obj_vals = []
for i in range(0, node_count-1):
	for j in range(i+1, node_count):
		if G_adv_list[i][j] > 0:
			obj_vals.append((G_adv_list[i][j], 'x{}{}'.format(get_num(i), get_num(j))))
with open('objective.txt', 'w') as op:
	op.write('Min\n')
	op.write('+'.join(list(map(lambda x: '({})({})'.format(x[0], x[1]), obj_vals))))
	op.write('\n')








