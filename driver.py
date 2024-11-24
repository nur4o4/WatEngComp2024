# simple program to read from csv
import csv

def indexFunc(e):
	return e[2]

# read in all of the server data from the server csv
servers = []
max_params = [0, 0] # cores, ram
tot_params = [0, 0] # cores, ram
with open('./test_data/servers1.csv') as f:
	data = csv.DictReader(f)
	for line in data:
		servers.append([int(line['Sever Number']), int(line['Number of Cores']), int(line['Number of Watts']), int(line['Total RAM'])])
		if(int(line['Number of Cores']) > max_params[0]):
			max_params[0] = int(line['Number of Cores'])
		if(int(line['Total RAM']) > max_params[1]):
			max_params[1] = int(line['Total RAM'])
		tot_params[0] += int(line['Number of Cores'])
		tot_params[1] += int(line['Total RAM'])
servers.sort(key=indexFunc)

# read in all of the tasks from the task csv
all_tasks = []
tot_task_params = [0, 0]
with open('./test_data/tasks1.csv') as f:
	data = csv.DictReader(f)
	for line in data:
		# choose not to run any task that exceeds the maximum resources of all of the servers
		possible = (int(line['Number of Cores']) <= max_params[1] or int(line['RAM']) <= max_params[1])-1
		all_tasks.append([int(line['Number of Cores']), int(line['Number of Turns']), int(line['RAM']), int(line['Complete in Turns']), possible, possible, 0])
		tot_task_params[0] += int(line['Number of Cores'])
		tot_task_params[1] += int(line['RAM'])

print("tasks: ", all_tasks)
print("\nservers: ", servers)
print("\n\nserver params: ", tot_params)
print("task params: ", tot_task_params)
print("multiples: ", tot_task_params[0]/tot_params[0], tot_task_params[1]/tot_params[1])

restrictive_param = (tot_task_params[1]/tot_params[1] > tot_task_params[0]/tot_params[0])*2
print("restrict: ", restrictive_param)

# preprocessing
# start deciding which server will run each task: if there is a task that can only possibly be completed by one server, assign that server to the task
for task in all_tasks:
	for i in range(0, len(servers)):
		if(servers[i][1] >= task[0] and servers[i][3] >= task[2]):
			task[6] = i
			break
		else:
			continue

print(all_tasks)
