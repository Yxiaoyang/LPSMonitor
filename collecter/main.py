# -- coding: utf-8 --

import psutil,time,requests,json

class Collecter(object):

    def __init__(self):
        pass

    def Get_Cpu_Info(self):
        '''cpu 逻辑核心数'''
        cpu_count = psutil.cpu_count()
        '''cpu 占比时长信息'''
        cpu_times = psutil.cpu_times()
        user_cpu = cpu_times.user
        system_cpu = cpu_times.system
        idle_cpu = cpu_times.idle
        '''cpu 使用率'''
        use_percent = psutil.cpu_percent(interval=0.1)
        idle_percent = 100 - use_percent
        '''load avg'''
        psutil.getloadavg()
        cpu_loadavg = psutil.getloadavg()

        cpu_info = {
            'cpu_count': cpu_count,
            'use_cpu_time': user_cpu + system_cpu,
            'total_cpu_time': user_cpu + system_cpu + idle_cpu,
            'use_percent': use_percent,
            'idle_percent': idle_percent,
            'cpu_loadavg': cpu_loadavg
                    }
        print(cpu_info)
        return json.dumps(cpu_info)


if __name__ == "__main__":
    # psutil.cpu_percent(interval=10)
    collec = Collecter()
    while True:
        collec.Get_Cpu_Info()
        time.sleep(1)




