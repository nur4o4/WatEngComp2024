# simple program to read from csv
import csv

def indexFunc(e):
	return e[2]

# read in all of the server data from the server csv
servers = []
max_params = [0, 0] # cores, ram
tot_params = [0, 0] # cores, ram
with open('./servers1.csv') as f:
	data = csv.DictReader(f)
	for line in data:
		servers.append([int(line['Sever Number']), int(line['Number of Cores']), int(line['Number of Watts']), int(line['Total RAM']), 0])#last is ram used
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
with open('./tasks1.csv') as f:
	data = csv.DictReader(f)
	for line in data:
		# choose not to run any task that exceeds the maximum resources of all of the servers
		all_tasks.append([int(line['Number of Cores']), int(line['Number of Turns']), int(line['RAM']), int(line['Complete in Turns']), int(line['Number of Turns']), 0, 0, 0])
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
			task[6] = -1

print(all_tasks)

counter = 0 # counter of finished tasks (both completed or failed)
turn = 0 #counter to go through tasks array
actualturn = 1 # turn number
whoswhere = [len(servers)]
print("loop start")
curr = [] #array of tasks currently on servers
while(counter<len(all_tasks)):
	if(all_tasks[turn][6]<0): # does not have an ideal server (RAM exceeds max server RAM)
		remove = [0,0,0,0,0]
		remove[0] = actualturn
		remove [1] = i
		remove[3] = servers[whoswhere[i]][2] * all_tasks[turn][1]
		with open("output.csv", mode='a', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(remove) 
		counter+=1
	else: # has an ideal server that exists
		curr.append(all_tasks[turn]) # add to array of tasks currently running
		for i in range(all_tasks[turn][6], len(servers)):#adding to a server
			if((servers[i][3]-servers[i][4])>all_tasks[turn][2]): #check which is the most ideal server is that can hold the task based on available RAM
				servers[i][4] += all_tasks[turn][2]
				#whoswhere[i] = i
				break
			else: # no server available, failed
				remove = [0,0,0,0,0]
				remove[0] = actualturn
				remove [1] = i
				#remove[3] = servers[whoswhere[i]][2] * all_tasks[turn][1]
				with open("output.csv", mode='a', newline='') as file: # write to output.csv
					writer = csv.writer(file)
					writer.writerow(remove)  
				counter+=1 # add one to counter of finished tasks
		min = curr[0][3]-curr[0][1] #setting minimum difference between Complete in Turns and Number of Turns to first task
		min_index = 0 # current index 0
		for i in range(len(curr)): # checking for minimum difference
			if (len(curr)==1):
				min_index = i # if only one task currently, min_index is 0
			elif((curr[i][3] - curr[i][1])<min):
				min_index = i # replace min index if found a smaller difference
				min = curr[i][3] - curr[i][1]
		curr[min_index][4]-=1 # delete from turn of task with the minimum difference
		numdel = 0 # if a number is deleted (fixes an error)
		for i in range(len(curr)):
			if(curr[i-numdel][4]==0):#completed, turn is 0
				done = [0,0,1,0,0]
				done[0] = actualturn
				done[1] = i-numdel
				#done[3] = servers[whoswhere[i]][2] * all_tasks[turn][1]
				with open("output.csv", mode='a', newline='') as file:
					writer = csv.writer(file)
					writer.writerow(done)  #write to output.csv
				counter+=1 # add one to completed/failed counter
				if(len(curr)>0): # remove task (if its not the only task currently)
					curr = curr[:i-numdel]+curr[i-numdel+1:]
					numdel+=1
			elif(curr[i-numdel][4]<0):# task turns exceeded, failed
				remove = [0,0,0,0,0]
				remove[0] = actualturn
				remove [1] = i-numdel
				#remove[3] = servers[whoswhere[i]][2] * all_tasks[turn][1]
				with open("output.csv", mode='a', newline='') as file:
					writer = csv.writer(file)
					writer.writerow(remove)  # write to output.csv
				counter+=1
	turn+=1 
	actualturn+=1
'''
while(counter < len(all_tasks)):
	# decide whether or not to read next task
	for server in servers:
		if(all_tasks[next_task][0] <= server[1] and all_tasks[next_task][2] <= server[3] and server[4] == None):
			all_tasks[next_task][7] = turn
			server[4] = all_tasks[next_task]
			next_task += 1
			break;
	
	# compute task progress
	for server in servers:
		if(turn - server[4][7] == server[4][1]):
			# turn complete
	
	turn += 1
	
for i in range (0, len(all_tasks)):
	print(i)
	print(all_tasks[i])
	if(all_tasks[i][6]<0):
		remove = [0,0,0,0,0]
		remove[0] = turn
		remove [1] = i
		with open("output.csv", mode='a', newline='') as file:
			writer = csv.writer(file)
			writer.writerow(remove)  # Append a single row
	else:
		continue
	turn+=1'''
