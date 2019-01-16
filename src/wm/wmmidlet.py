#!/usr/bin/python

def install(wmodule, path, javapass):
    ans = wmodule.call_waiting("AT^SJAM=0,\"A:/%s\",\"%s\"" % (path, javapass), "OK", "ERROR")
    return ans[1] == "OK"

def start(wmodule, path, javapass):
    ans = wmodule.call_waiting("AT^SJAM=1,\"A:/%s\",\"%s\"" % (path, javapass), "OK", "ERROR")
    return ans[1] == "OK"

def stop(wmodule, path, javapass):
    ans = wmodule.call_waiting("AT^SJAM=2,\"A:/%s\",\"%s\"" % (path, javapass), "OK", "ERROR")
    return ans[1] == "OK"

def remove(wmodule, path, javapass):
    ans = wmodule.call_waiting("AT^SJAM=3,\"A:/%s\",\"%s\"" % (path, javapass), "OK", "ERROR")
    return ans[1] == "OK"
