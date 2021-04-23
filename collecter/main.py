# -- coding: utf-8 --

import psutil,time,requests,json,subprocess
import configparser

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

    def Get_Extend_Info(self, key, value):
        '''获取自定义脚本数据'''
        value = subprocess.Popen(value.strip("'"), shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read().decode('utf8').strip('\r\n')
        return value

if __name__ == "__main__":
    '''初始化相关信息'''
    collect = Collecter()
    conf = configparser.ConfigParser()
    conf.read('monitor.conf', 'utf8')
    poll_time = conf.get('collect', 'poll_time')
    extend_status = conf.get('collect', 'extend_status')
    server_url = conf.get('server', 'url')
    server_port = conf.get('server', 'port')
    server_perfix = '/insert_info'
    server_apikey = conf.get('server', 'apikey')

    while True:
        all_info = {}
        '''获取扩展脚本信息'''
        if extend_status == 'True':
            for k,v in conf.items('extend'):
                all_info[k] = collect.Get_Extend_Info(k,v)

        all_info['cpus'] = collect.Get_Cpu_Info()
        all_info['mems'] = collect.Get_Mem_Info()
        all_info['disks_space'] = collect.Get_Disk_Space_Info()
        all_info['disks_io'] = collect.Get_Disk_IO_Info()
        all_info['nets'] = collect.Get_Net_Info()

        '''提交数据到服务端'''
        # requests.post(server_url,data=all_info)

        print(all_info)
        time.sleep(int(poll_time))







