import numpy as np
import matplotlib.pyplot as plt

TIME=500
WORKER=100
FOG=10
OBJECTS=100

def f(truth_by_object):
    # This function captures the variation trend
    result=np.zeros((TIME,OBJECTS))
    for i in range(TIME):
        result[i]=truth_by_object+i*np.random.normal(0,10)
    return result

class system():
    def __init__(self):
        self.ground_truths=np.zeros((TIME,OBJECTS))
        self.worker_deviation=np.zeros(TIME)
        self.w_profile={}
        self.f_profile={}
        self.c_profile={}

    def gen_truths(self):
        ground_truth_by_object=np.random.uniform(0,100,OBJECTS)
        ground_truth_by_time=f(ground_truth_by_object)
        self.ground_truths+=ground_truth_by_time

    def gen_deviation(self):
        self.worker_deviation+=np.random.uniform(1,10,TIME)

    def worker_profile(self):
        mod=np.ceil(WORKER/FOG)
        for i in range(WORKER):
            self.w_profile[i]={'fog':i%mod,'ID':i,'deviation':self.worker_deviation[i]}

    def fog_profile(self):
        mod=np.ceil(WORKER/FOG)
        for i in range(FOG):
            w_profile=[self.w_profile[j] for j in range(WORKER) if j%mod==i]
            self.f_profile[i]={'ID':i,'w_profile':w_profile}
    def csp_profile(self):
        self.c_profile={'ID':0,'f_profile':self.f_profile}

    def add_csp(self):
        self.csp=CSP(self.c_profile)
        self.csp.fog_allocation()

    def add_worker(self,csp_info,fog_info,worker_info):
        pass
    def remove_worker(self,csp_info,fog_info,worker_info):
        pass
    def execute(self):
        pass
    def plot(self):
        pass
    def RMSE(self):
        pass
    def local_aggregate(self,csp_info,fog_info,time):
        pass

class CSP():
    def __init__(self,csp_profile):
        self.ID=csp_profile['ID']
        self.fog_profile=csp_profile['f_profile']
        self.fogs={}

    def fog_allocation(self):
        # fog_profile is a dict
        for fog_info in self.fog_profile.keys():
            self.fogs[fog_info]=fog(self.fog_profile[fog_info])
            self.fogs[fog_info].worker_allocation()

    def global_iterations(self):
        pass



class fog():
    def __init__(self,fog_info):

        # pre-defined attributes:dict
        self.ID=fog_info['ID']
        self.worker_profile=fog_info['w_profile']

        # post-defined attributes:np.array
        self.local_truths=np.zeros((TIME,OBJECTS))
        self.workers={}
        self.lt=np.zeros(OBJECTS)

    def worker_allocation(self):
        # worker_profile is a list
        for worker_info in self.worker_profile:
            # 建立的索引均是ID
            self.workers[worker_info['ID']]=worker(worker_info)
            self.workers[worker_info['ID']].init_weights()

    def add_worker(self,worker_info):
        self.workers[worker_info]=worker(worker_info)

    def remove_worker(self,worker_info):
        del self.workers[worker_info]

    def truths_update(self,t):
        for worker_id in self.workers.keys():
            self.workers[worker_id].sensing()
        w_list=[self.workers[worker_id].weight[t] for worker_id in self.workers.keys()]
        t_list=[self.workers[worker_id].local_data[t] for worker_id in self.workers.keys()]
        sumw=np.sum(w_list)
        sumwx=w_list*t_list
        self.lt=sumwx/sumw
    def weights_update(self):
        pass


class worker():
    def __init__(self,worker_info):
        self.ID=worker_info['ID']
        self.deviation=worker_info['deviation']

        self.local_data=np.zeros((TIME,OBJECTS))
        self.weight=np.zeros(TIME)

    def init_weights(self):
        # iCRH首先更新真值，在更新权重
        self.weight=np.ones(TIME)
    def sensing(self):
        self.local_data+=np.random.normal(0,self.deviation,(TIME,OBJECTS))






if __name__=="__main__":
    s=system()
    s.gen_truths()
    s.gen_deviation()
    s.worker_profile()
    s.fog_profile()
    s.csp_profile()
    s.add_csp()
    s.global_iteration()
    s.RMSE()
    s.plot()