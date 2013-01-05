#coding=utf-8


#----------------------------------------
def stop_ctrl(ctrl, message):
    ctrl.running = False

def enable_debug(ctrl, message):
    ctrl.debug = True

def disable_debug(ctrl, message):
    ctrl.debug = False

def enable_reload(ctrl, message):
    ctrl.reload = True


def disable_reload(ctrl, message):
    ctrl.reload = False

def clear_caches(ctrl, message):
    ctrl.clear_caches()



