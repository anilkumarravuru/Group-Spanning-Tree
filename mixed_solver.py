# Anil Kumar Ravuru

import time
from ortools.linear_solver import pywraplp
solver = pywraplp.Solver('simple_mip_program', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

integral_variable_names = list(map(lambda x: x[:-1], open('integral_variables.txt', 'r').readlines()))
float_variable_names = list(map(lambda x: x[:-1], open('float_variables.txt', 'r').readlines()))
variable_names = integral_variable_names + float_variable_names

# Non Negative Constraints
variables = [solver.IntVar(0.0, solver.infinity(), integral_variable_names[i]) for i in range(len(integral_variable_names))]
variables += [solver.NumVar(0.0, solver.infinity(), float_variable_names[i]) for i in range(len(float_variable_names))]

# Integral Constraints
with open('constraints.txt', 'r') as lines:
	for line in lines:
		# print(line)
		left, right = line.split('=')
		is_less = left[-1] == '<'
		left, right = left[:-2].split('+'), float(right.strip())
		consts = list(map(lambda x: (float(x[1:x.index(')(')]), x[x.index(')(')+2:-1]), left))
		temp_constraint = 0
		for cnt in consts:
			temp_constraint += cnt[0]*variables[variable_names.index(cnt[1])]
		if is_less:
			solver.Add(temp_constraint <= right)
		else:
			solver.Add(temp_constraint >= right)

# Objective Function
typ, obj_fn = open('objective.txt', 'r').readlines()
is_max = typ == 'Max\n'
obj_fn_vars = list(map(lambda x: (float(x[1:x.index(')(')]), x[x.index(')(')+2:-1]), list(map(str, obj_fn[:-1].split('+')))))
temp_objective = 0
for cnt in obj_fn_vars:
	temp_objective += cnt[0]*variables[variable_names.index(cnt[1])]
if is_max:
	solver.Maximize(temp_objective)
else:
	solver.Minimize(temp_objective)

# status = solver.Solve()
# if status == pywraplp.Solver.OPTIMAL:
# 	opt_solution = sum(list(map(lambda x: x[0]*variables[variable_names.index(x[1])].solution_value(), obj_fn_vars)))
# 	print('Optimum Value: ', opt_solution)
# 	for i in range(len(variable_names)):
# 		print(variable_names[i] + ' : ', variables[i].solution_value())

start_time = time.time()
status = solver.Solve()
end_time = time.time()
print('Time to Solve LP Problem: ', int(end_time-start_time), 'secs')
# print(status)
if status == pywraplp.Solver.OPTIMAL:
	opt_solution = sum(list(map(lambda x: x[0]*variables[variable_names.index(x[1])].solution_value(), obj_fn_vars)))
	print('Optimum Value: ', opt_solution)
	for i in range(len(integral_variable_names)):
		if variables[i].solution_value() > 0:
			print(variable_names[i] + ' : ', variables[i].solution_value())

