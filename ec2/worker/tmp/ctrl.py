#coding=utf-8


#----------------------------------------
def stop(ctrl, _):    ctrl.stop()

def enable_debug(ctrl, _):
    ctrl.debug = True

def disable_debug(ctrl, _):
    ctrl.debug = False

def enable_reload(ctrl, _):
    ctrl.reload = True

def disable_reload(ctrl, _):
    ctrl.reload = False

def clear_caches(ctrl, _):
    ctrl.clear_caches()







