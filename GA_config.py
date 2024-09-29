#simulation Time
MAX_SIMULATION_TIME = 1000
	
#cloud server attributes
CLOUD_COST_UNIT_TIME = 0.01
CLOUD_CPU_SPEED = 48000

#capacity
FD_CAPACITY1 = 10
FD_CAPACITY3 = 15
FD_CAPACITY5 = 20
	
#CPU speed instructions per second
CPU_SPEED1 = 2000
CPU_SPEED2 = 3000
CPU_SPEED3 = 5000
	
#latency
LATENCY_CS_FR = 50
LATENCY_ED_FR = 2
	
#three types of jobs
#job types
NORMAL_ALERTS   = 1
EMERGENCY_ALERTS = 2
RECOMENDATIONS  =  3

#number of instructions (in bytes) in each job Type
NO_INSTRUCTIONS1 = 30000
NO_INSTRUCTIONS2 = 40000
NO_INSTRUCTIONS3 = 50000
	
#job data size
DATA_SIZE1 = 500
DATA_SIZE2 = 1000
DATA_SIZE3 = 1500

SLOT_TIME =  NO_INSTRUCTIONS3 / CPU_SPEED1