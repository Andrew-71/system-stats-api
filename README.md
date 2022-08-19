## Simple flask API to retrieve system status
Ever wanted to know CPU and memory usage of your server remotely? Now you can!

## Arguments
```bash
usage: app.py [-h] [-p PORT] [-c CODE] [-dc DEFAULT_CODE] [-dp DEFAULT_PORT] [-dr DEFAULT_REFRESH] [-d]

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port to listen on
  -c CODE, --code CODE  Key to use to access the stats
  -dc DEFAULT_CODE, --default-code DEFAULT_CODE
                        Set a code as default
  -dp DEFAULT_PORT, --default-port DEFAULT_PORT
                        Set a port port as default
  -dr DEFAULT_REFRESH, --default-refresh DEFAULT_REFRESH
                        Set how often to update the stats (in seconds)
  -d, --debug           Run on Flask debug server

```

## Response format
```
{'os': os type (Linux, Darwin or Windows,
 'release': OS Release version, 
 'version': Long form of OS version, 
 'boot_time': timestamp of boot time,           
 'cpu': {
    'usage_percent': percentage of CPU usage, 
    'core_count': amount of physical cores, 
    'frequency': {
        // Does not work on M1, returns 0
        'current': current CPU frequency,
        'max': maximum CPU frequency,
        'min': minimum CPU frequency,
    }
 },
 'ram': {
   'total': Total amount of RAM (in bytes),
   'used': How much RAM is used (in bytes),
 }, 
 'disks': [
    // Per disk info of each partition
    {
        'total': Total amount of disk space (in bytes),
        'used': How much disk space is used (in bytes),
        'free': How much disk space is free (in bytes),
        'percent': Percentage of disk space used,
        'fstype': File system type,
        'mountpoint': Mount point of the disk
   }
 ],
 'temperature': {
    // Data from temperature sensors, only on Linux
 } 
}
