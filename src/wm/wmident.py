#!/usr/bin/python
    
def is_responding(wmodule):
    atok = wmodule.call_waiting("AT","OK")
    # raise exception if timeout expired or the answer is not recognized
    return atok[1] is not None