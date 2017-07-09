# -*- coding: utf-8 -*-

import platform
def isWindows():
    return 'Windows' in platform.system()

def isLinux():
    return 'Linux' in platform.system()