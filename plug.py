import re
from datetime import datetime, timedelta
import subprocess
import os
import tinytuya

env = os.environ

EXPIRE_MINUTES = 10

cache = {
    'expire': None,
    'plug': None
}


def get_plug():
    now = datetime.now()
    expired = cache['expire'] is None or now > cache['expire']
    if expired:
        cache['plug'] = create_plug()
    cache['expire'] = now + timedelta(minutes=EXPIRE_MINUTES)
    return cache['plug']


def create_plug():
    ip = find_ip()
    plug = tinytuya.OutletDevice(
        env['TUYA_DEV_ID'],
        ip,
        env['TUYA_LOCALKEY']
    )
    plug.set_version(3.3)
    return plug


def find_ip():
    iprange = env['TUYA_IP_RANGE']
    res = subprocess.run(
        ['sudor', 'nmap', '-p6668', iprange, '-oG', '-'],
        check=True, text=True, capture_output=True)
    for line in res.stdout.split('\n'):
        m = re.match('Host: (.*?) .*Ports: 6668/open', line)
        if m:
            return m.group(1)
    raise Exception(f'Cannot find tuya IP')
