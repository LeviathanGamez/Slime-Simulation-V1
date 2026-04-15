import matplotlib.pyplot as plt
file = open("Simulator/data.txt", "r") 
# time population living avg speed avg range, avg food, avg water,

all_time = []
all_population = []
all_living = []
all_speed = []
all_range = []
all_potatoes = []
data = [all_time,all_population,all_living,all_speed,all_range,all_potatoes]
# time population living avg speed avg range, avg food, avg water,
for line in file:
   numbs = line.split(",")
   if len(numbs) > 2:
      for i in range(len(data)):
         data[i].append(int(numbs[i]))
mover = 0
mover = data[3]
data[3] = data[4]
data[4] = mover
titles = ["Population + Living","Average Speed + Range","Potatoes"]
axes = ["Pop + Living","Speed + Range","Potatoes"]
labels = ["Population","Living","Range","Speed","Potatoes"]
#len(data)-1
colors = ["#eb15bc","#28e81a","#0505f2","#f2db05","#f27005","#05cbf2","#fff708"]
for i in range(len(data)-1):
   if i % 2 == 1:
      plt.plot(data[0],data[i+1],color=colors[i],label=labels[i])
      plt.legend()
      plt.fill_between(data[0],data[i+1],color=colors[i],alpha=0.3)
   else:
      plt.figure(figsize=(800,600))
      plt.title(titles[int(i/2)])
      plt.plot(data[0],data[i+1],color=colors[i],label=labels[i]) 
      plt.xlabel('Time')
      plt.ylabel(axes[int(i/2)])
      print(i,len(data))
      if i + 2 >= len(data):
         plt.fill_between(data[0],data[i+1],color=colors[i],alpha=0.3)
      else:
         plt.fill_between(data[0],data[i+1],data[i+2],color=colors[i],alpha=0.3)
plt.show()














