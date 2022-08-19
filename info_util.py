import platform
from collections import namedtuple
import psutil

uname = platform.uname()  # Preload uname


def get_info():
    # CPU frequency is broken on M1 Macs
    try:
        cpu_frequency = psutil.cpu_freq()
    except Exception as e:
        cpu_frequency = namedtuple('cpu_frequency', ['current', 'min', 'max', 'note'])(0, 0, 0, str(e))

    # Temperature is only available on Linux
    try:
        temp = psutil.sensors_temperatures()
    except Exception as e:
        temp = {'note': f'You\'re not on Linux, so the program says "{e}"'}

    ram = psutil.virtual_memory()
    disks = psutil.disk_partitions()

    info = {'os': uname.system,
            'release': uname.release,
            'version': uname.version,
            'boot_time': psutil.boot_time(),
            'cpu': {
                'usage_percent': psutil.cpu_percent(),
                'core_count': psutil.cpu_count(),
                'frequency': {
                    'current': cpu_frequency.current,
                    'max': cpu_frequency.max,
                    'min': cpu_frequency.min
                }
            },
            'ram': {
                'total': ram.total,
                'used': ram.used
            },
            'disks': [],
            'temperature': temp
            }

    # Add information about disks
    for i in disks:
        disk_data = psutil.disk_usage(i.mountpoint)
        info['disks'].append({'total': disk_data.total,
                              'used': disk_data.used,
                              'free': disk_data.free,
                              'percent': disk_data.percent,
                              'fs_type': i.fstype})

    return info


if __name__ == '__main__':
    print(get_info())
