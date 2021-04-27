import os
import argparse
import sys
import trace
import subprocess
import threading
import time


def print_dict(dict):
    cMax = 0
    vMax = 0
    print("return codes:")
    for code in dict:
        print("code: ", code, "times: ", dict[code])
        if(dict[code] > vMax):
            vMax = dict[code]
            cMax = code
    return cMax


def run_command(command):
    code = os.system(command)
    return code

def execute_command(args, dict):
    command = get_command(args.Command)
    fails = 0
    strace = ""
    if(args.call_trace):
        strace += "strace -o log.txt"
        if(args.call_trace):
            strace += " -c "
    command = strace + command    
    N = args.failed_count
    if (N == None):
        N = args.c
    for i in range(args.c):
        code = run_command(command)
        if code in dict:
            dict[code] += 1
        else:
            dict[code] = 1
        if (code != 0):
            fails+=1
            if(args.call_trace):
                f = open("log.txt", "r")
                print(f.read())
                f.close()
            if (fails >= N):
                break




def get_command(str): #adding the list string to get the command
    command = ''
    for w in str:
        command += w + ' '
    return command

def get_args(): #parsing the args
    parser = argparse.ArgumentParser()
    parser.add_argument('Command', metavar='command', type=str, nargs='+', help='the command to be executed')
    parser.add_argument('-c', metavar='COUNT', action='store', type=int, default=1, help='Number of times to run the given command')
    parser.add_argument('--failed-count', metavar='N', action='store', type=int,
                        help='Number of allowed failed command invocation attempts before giving up')
    parser.add_argument('--sys-trace', action='store_true',
                        help='For each failed execution, create a log for each of the following values, measured during command execution:')
    parser.add_argument('--call-trace', action='store_true',
                        help='For each failed execution, add also a log with all the system calls ran by the command')
    parser.add_argument('--log-trace', action='store_true',
                        help='For each failed execution, add also the command output logs')
    parser.add_argument('--debug', action='store_true',
                        help='Debug mode, show each instruction executed by the script')
    parser.add_argument('--net-trace', action='store_true',
                        help='Debug mode, show each instruction executed by the script')

    args = parser.parse_args()
    return args

args = get_args()
dict = {}
tracer = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix], trace=args.debug, count=1)
tracer.run('execute_command(args, dict)')
#execute_command(args)
r = tracer.results()
r.write_results(show_missing=True, coverdir=".")
sys.exit(print_dict(dict))






