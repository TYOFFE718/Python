mport logging
from fabric.api import *


def servers():
    env.user = 'tyoffe'
    env.hosts = ['192.168.65.130', '192.168.65.129']




def check_uptime():
     run("uptime | awk '{print $1}'")
