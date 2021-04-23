# -- coding: utf-8 --

import psutil,time,requests,json


class Collecter(object):

    def __init__(self):
        pass

    def Get_Cpu_Info(self):

        '''cpu 使用率'''
        used_percent = psutil.cpu_percent(interval=0.1)
        idle_percent = 100 - used_percent

        cpu_info = {
            'cpu_count': psutil.cpu_count(),
            'idle_cpu_time': psutil.cpu_times().idle,
            'use_percent': used_percent,
            'idle_percent': idle_percent,
            'cpu_loadavg': psutil.getloadavg()
                    }
        return json.dumps(cpu_info)


    def Get_Mem_Info(self):
        '''获取内存信息'''
        mem = psutil.virtual_memory()
        mem_info = {
            'total_mem': mem.total,
            'used_mem': mem.used,
            'available_mem': mem.available,
            'percent_mem': mem.percent
        }

        return json.dumps(mem_info)

    def Get_Disk_Space_Info(self):
        '''获取所有设备id'''
        all_disks = [i.device for i in psutil.disk_partitions(all=False)]

        '''新建列表，存储各设备空间使用情况'''
        all_disks_usage = {}

        '''获取不同分区的空间使用情况'''
        for i in all_disks:
            per_disk_usage = {}
            disk = psutil.disk_usage(i)
            per_disk_usage['total'] = disk.total
            per_disk_usage['used'] = disk.used
            per_disk_usage['free'] = disk.free
            per_disk_usage['percent'] = disk.percent

            all_disks_usage[i] = per_disk_usage

        return json.dumps(all_disks_usage)


    def Get_Disk_IO_Info(self):
        '''获取物理磁盘IO情况'''
        all_disks = psutil.disk_io_counters(perdisk=True)

        '''存储各物理磁盘io使用情况'''
        all_disks_io = {}

        for i in all_disks:
            '''存储单个磁盘io使用情况'''
            per_disk_io = {}
            per_disk_io['read_count'] = all_disks[i].read_count
            per_disk_io['write_count'] = all_disks[i].write_count
            per_disk_io['read_bytes'] = all_disks[i].read_bytes
            per_disk_io['write_bytes'] = all_disks[i].write_bytes
            per_disk_io['read_time'] = all_disks[i].read_time
            per_disk_io['write_time'] = all_disks[i].write_time

            all_disks_io[i] = per_disk_io

        return json.dumps(all_disks_io)


    def Get_Net_Info(self):

        '''获取网卡名字'''
        all_inter = psutil.net_if_stats()
        all_inter_info = {}

        for i in all_inter:
            per_net_info = {}
            '''获取单个网卡第一次接受和发送的总流量（bytes）'''
            first_net_sent = psutil.net_io_counters(pernic=True)[i].bytes_sent
            first_net_recv = psutil.net_io_counters(pernic=True)[i].bytes_recv
            time.sleep(0.5)
            '''获取单个网卡第二次接受和发送的总流量（bytes）'''
            current_net_sent = psutil.net_io_counters(pernic=True)[i].bytes_sent
            current_net_recv = psutil.net_io_counters(pernic=True)[i].bytes_recv

            per_net_info['net_sent'] = (current_net_sent - first_net_sent) * 2
            per_net_info['net_recv'] = (current_net_recv - first_net_recv) * 2

            all_inter_info[i] = per_net_info
        return json.dumps(all_inter_info)


if __name__ == "__main__":
    # psutil.cpu_percent(interval=10)
    collec = Collecter()
    collec.Get_Net_Info()





