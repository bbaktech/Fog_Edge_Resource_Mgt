
from config import DATA_SIZE1, MAX_SIMULATION_TIME, NO_INSTRUCTIONS1, NORMAL_ALERTS, SLOT_TIME
from devices import Cloud, EdgeDevice, FogDevice, Job,logentry, cs,tt

#number of Cluster-Fog devices 
numOfFDs = 4
#number of Edge devices per cluster
numOfEDs = 20

#cluster manager co-ordinates Cluster-FRs if  clusterMgrCoordination = true
clusterMgrCloudonly = False
clusterMgrGACoordination = False

#create task list with empty 
jobQ = []
ClusterRs = []
EdgeRs =[]
#cloud computing server 

#create cluster-fog and edge devices and connects them
for i in range(numOfFDs):
    fr = FogDevice (i,"ClusterFR:"+str(i))
    ClusterRs.append(fr)
    for j in range(numOfEDs):
        #create edge device
        ed = EdgeDevice("EdgeD_"+str(i)+"_"+str(j))
        #set the cluster id to newly created edge
        ed.setClusterId(i)
        EdgeRs.append(ed)

print("Cluster-Fds (FogDevices)")
for device in  ClusterRs:
    print("   "+device.name +"  Cores:"+str(device.no_core) + "    CPU Speed:" + str(device.cpu_speed) )
print("Edge Devices " )
for device in EdgeRs:
    print ("   "+device.name + "(Connected to ClusterFR:"+ str(device.connected_cl_id) + ")")

Slot = 0
sim_time = 0.
if (clusterMgrCloudonly):
    print("Cluster-Resource Manager Cloud Only")
elif (clusterMgrGACoordination):
    print("Cluster-Resource Manager GA")			
else:
    print("Cluster-Resource Manager BFS")

print("Simulation Started")
sl_no = 0
slot_avg_delay =0.
while MAX_SIMULATION_TIME > sim_time:
    slot_avg_delay = 0. #used to write to file
    #clean buffer of cluster-fog devises to receive tasks
    for device in ClusterRs:
        device.clean()
    cs.clear()
    Slot+=1

	#all edge devices will place tasks for execution and are add to task list
    for device in EdgeRs:
        job = device.CreateUploadJob()
        if job is not None:
            sl_no+=1
            job.setSlotNo(Slot)
            job.setSubmitime(sim_time)
            job.setSerial(sl_no)
            #task is added to TaskQueue
            jobQ.append(job)

    msg = "\nSlot No:"+str(Slot)+ " Jobs:"+str(len(jobQ)) +"\n"
    #write slot number to slot_log file
    logentry.WriteStringToSlotsLog(msg)
    logentry.WriteStringToSlotsLog("-------------------------------------------------------------\n")

    if len(jobQ) > 0:
        if clusterMgrCloudonly :
            for job in jobQ:
                cs.ExecutesTask(job)
        elif (not clusterMgrGACoordination ):
            for job in jobQ:
                ClusterRs[job.fd_devid].ExecutesTask(job)
        else:
            #GA 
            pass

    jobQ.clear()
    sim_time = sim_time+ SLOT_TIME
    #write the summary of execution of task at each slot to slot_summary log file
    for device in ClusterRs:
        device.ComputeSlotLoad()
    cs.WriteSlotSummary()

print("Simulation Completed")
print("-----------Results--------------------")
print("Total Simulation Time:"+ str(MAX_SIMULATION_TIME))
print("Total Number of Slots:"+ str(Slot))		
tt.PrintTimeDetails()
print()
for device in ClusterRs:
    device.PrintResult(Slot )
    print()

cs.PrintNoTasksExecuted()
print()

print("\nYou could see:")
print("              " + logentry.fnameJobs+ " for details on each job ")
print("              " + logentry.fnameSlots + " for summary of each slot")
print("---------------------------------------");	
