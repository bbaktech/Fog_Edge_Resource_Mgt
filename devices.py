
from datetime import datetime 
from config import CLOUD_COST_UNIT_TIME, CLOUD_CPU_SPEED, CPU_SPEED1, CPU_SPEED2, CPU_SPEED3, DATA_SIZE1, FD_CAPACITY1, FD_CAPACITY3, FD_CAPACITY5, LATENCY_CS_FR, LATENCY_ED_FR, MAX_SIMULATION_TIME, NO_INSTRUCTIONS1, NO_INSTRUCTIONS2, NO_INSTRUCTIONS3, NORMAL_ALERTS, SLOT_TIME
import random

class TimeTracker:
    def __init__(self):
        self.maxTimetakenbyTask = 0.
        self.minTimetakenbyTask= 100.
        self.sumTimetakenbyTask= 0.
        self.no_tasks=0

    def RecordTimeDetails(self,jb):
        extime = jb.duration
        delay = jb.ex_timestamp - jb.sb_timestamp
        timetakenbytask = delay + extime
        if (timetakenbytask > self.maxTimetakenbyTask):
            self.maxTimetakenbyTask = timetakenbytask
        if (timetakenbytask < self.minTimetakenbyTask):
            self.minTimetakenbyTask = timetakenbytask
        self.sumTimetakenbyTask = self.sumTimetakenbyTask + timetakenbytask
        self.no_tasks+=1

    def PrintTimeDetails(self):
        avgTimetakenbyTask = self.sumTimetakenbyTask /self.no_tasks
        imd = (self.maxTimetakenbyTask - self.minTimetakenbyTask) / avgTimetakenbyTask
        print("Total Number of Tasks:" + str(self.no_tasks ))
        print()
        print("max Timetaken for Task :" + str(self.maxTimetakenbyTask ))
        print("min Timetaken for Task :" + str(self.minTimetakenbyTask ))
        print("avg TimeTaken byTasks:" + str(avgTimetakenbyTask ))

class Job:
    def  __init__(self):
        self.data_size = DATA_SIZE1
        self.job_type = NORMAL_ALERTS
        self.no_instructions = NO_INSTRUCTIONS1
        self.ed_name = ""
        self.no_instructions = 0
        self.dest =""
        self.duration = 0.
        self.fd_devid =0

    def setSerial(self, n):
        self.id = n
		
    def setSlotNo(self, sn):
        self.slotno = sn

    def setSubmitime(self, sim_time):
        self.sb_timestamp = sim_time
        
    def setExecutionstarttime(self, delay):
        self.ex_timestamp = self.sb_timestamp+ delay

    def setExecutionduration(self , d):
        self.duration = d
          
class FileWrite:
    def __init__(self):
        current_time = datetime.now()
        dt_string = current_time.strftime("%d-%m-%Y%H-%M-%S")
        self.fnameSlots = "slots-" + dt_string +".txt"
        self.fnameJobs = "jobs-"  + dt_string +".txt"
        print(self.fnameJobs)

    def WriteStringToJobsLog(self, jb):
        tt.RecordTimeDetails(jb)
        with open(self.fnameJobs, 'a') as f:
            strval = "Id:"+str(jb.id) +" SlotNo:"+ str(jb.slotno)+" Source:"+jb.ed_name +" Size:"+ str(jb.no_instructions) +" Duration:"+ str(jb.duration) + " SubmitTime:"+str(jb.sb_timestamp) +" Destination:"+ jb.dest + " Executed at:"+str(jb.ex_timestamp) +" Delay:"+ str(jb.ex_timestamp+jb.duration-jb.sb_timestamp) +"\n"
            f.write(strval)
            f.close()

    def WriteStringToSlotsLog(self,str):
        with open(self.fnameSlots, 'a') as f:
            f.write(str)
            f.close()

class EdgeDevice :
    def __init__(self,n):
        self.id = id
        self.name = n
    def setClusterId(self, n):
        self.connected_cl_id = n
    def CreateUploadJob(self):
        # create a random job from the list
        jobtypelist = [0,1, 2, 3]
        job_type=random.choice(jobtypelist)
        job =Job()
        job.ed_name = self.name
        job.fd_devid = self.connected_cl_id

        match job_type:
            case 1:
                job.data_size = DATA_SIZE1
                job.job_type = NORMAL_ALERTS
                job.no_instructions = NO_INSTRUCTIONS1
                return job
            case 2:
                job.data_size = DATA_SIZE1
                job.job_type = NORMAL_ALERTS
                job.no_instructions = NO_INSTRUCTIONS2
                return job
            case 3:
                job.data_size = DATA_SIZE1
                job.job_type = NORMAL_ALERTS
                job.no_instructions = NO_INSTRUCTIONS3
                return job
            case 0:
                return 

class Cloud:
    def __init__(self) :
        self.slot_job_count = 0
        self.total_job_count = 0
        self.busy_time = 0
        self.cost_per_unit_time = CLOUD_COST_UNIT_TIME
        self.cpu_speed = CLOUD_CPU_SPEED
        self.name = "Cloud Server"

    def ExecutesTask(self, jb):
        jb.setExecutionstarttime(LATENCY_ED_FR + LATENCY_CS_FR)
        jb.dest = self.name
        self.total_job_count +=1
        self.slot_job_count+=1
        ex_duration = jb.no_instructions / self.cpu_speed
        jb.setExecutionduration(ex_duration)
        self.busy_time = self.busy_time + jb.no_instructions / self.cpu_speed
        logentry.WriteStringToJobsLog(jb)
    
    def clear(self):
        self.slot_job_count = 0

    def WriteSlotSummary(self):
        logentry.WriteStringToSlotsLog("Cloud Exicuted:"+str(self.slot_job_count)+"Jobs \n")
          
    def PrintNoTasksExecuted(self):
	    print("Cloud executed :"+str(self.total_job_count)+" Jobs" + "\n       Time Used:"+str(self.busy_time)  + "\n       Cost:"+ str(self.busy_time*self.cost_per_unit_time))

class FogDevice :
    def __init__(self,id,name):
        self.id = id
        self.name = name
        self.total_time = 0.
        self.total_Comp_time = 0.
        self.noTasksExecuted = 0
        self.cores =3
        self.cpu_speed = 2000
        self.busy_power = 107.339
        self.idle_power = 83.4333

        #slot level variables
        self.slot_core_balance=0
        self.slot_no_jobs_ex= 0
        self.slot_busy_time = 0
        x = id % 3
        match x:
            case 0:
                self.no_core = FD_CAPACITY1
                self.cpu_speed = CPU_SPEED1
                self.busy_power = 107.339
                self.idle_power = 83.4333
            case 1:
                self.no_core = FD_CAPACITY3
                self.cpu_speed = CPU_SPEED2
                self.busy_power = 107.339
                self.idle_power = 83.4333
            case 2:
                self.no_core = FD_CAPACITY5
                self.cpu_speed = CPU_SPEED3
                self.busy_power = 107.339
                self.idle_power = 83.4333

    def clean(self):
        self.slot_core_balance = 0
        self.slot_busy_time = 0
        self.slot_no_jobs_ex = 0

    def ExecutesTask(self,jb):
        global logentry
        self.slot_core_balance += 1    
        if (self.slot_core_balance <= self.no_core):
            jb.setExecutionstarttime(LATENCY_ED_FR)
            jb.dest = self.name
            self.slot_no_jobs_ex += 1
            ex_duration = jb.no_instructions / self.cpu_speed
            jb.setExecutionduration(ex_duration)
            logentry.WriteStringToJobsLog(jb)
            self.slot_busy_time = self.slot_busy_time + jb.no_instructions / self.cpu_speed      
        else:
            cs.ExecutesTask(jb)			

    def ComputeSlotLoad(self):
        msg = "Cluster:"+ self.name 
        logentry.WriteStringToSlotsLog(msg)
        if (self.slot_core_balance > self.no_core):
            self.noTasksExecuted = self.noTasksExecuted + self.no_core	
            msg = " No Jobs Exicuted:"+str(self.no_core)
            logentry.WriteStringToSlotsLog(msg)

        else:
            msg = " No Jobs Exicuted:"+str(self.slot_core_balance)
            logentry.WriteStringToSlotsLog(msg)			
            self.noTasksExecuted = self.noTasksExecuted + self.slot_core_balance	
                
        if (self.slot_busy_time > 0):
            self.slot_busy_time = self.slot_busy_time / self.no_core

        msg = " Capacity:"+ str(self.no_core) +" Busy Time:" + str(self.slot_busy_time) + "\n" 
        logentry.WriteStringToSlotsLog(msg)
        self.total_Comp_time = self.total_Comp_time + self.slot_busy_time
        self.total_time = self.total_time + SLOT_TIME

    def PrintResult(self,  slot):
        total_idletime = self.total_time - self.total_Comp_time
        energy_utilised = total_idletime * self.idle_power +self.total_Comp_time * self.busy_power
        TH = self.noTasksExecuted / MAX_SIMULATION_TIME
        cpu_utilization = self.total_Comp_time / self.total_time *100;
        print("Device:"+ self.name );
        print("      Total Jobs Executed:"+str(self.noTasksExecuted))
        print("      Total Busy Time:" + str(self.total_Comp_time) )
        print("      Total Idle Time:" + str(total_idletime) )
        print("      Total Time:" + str(self.total_time ))
        print("      CPU Utilization:"+ str(cpu_utilization))
        print("      Total Power Utilised:" + str( energy_utilised ))
        print("      Throughput:" + str(TH ))

logentry = FileWrite()
cs = Cloud()
tt = TimeTracker()
