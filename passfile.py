#!/usr/bin/env python3

# Requirements:
# pass: https://www.passwordstore.org/
# at daemon: http://blog.calhariz.com/tag/at

import argparse
from os import environ as env
from os.path import isfile
import subprocess

def get_path(p):
    homedir = env['HOME']
    path = p.replace("~", homedir).replace("$HOME", homedir)
    if isfile(path):
        print("the file %s already exists. exiting..." % path)
        exit(3)
    return path

def delete_file(wait_minutes, plaintext_path):
    cmd = "echo \"rm " + plaintext_path + "\" | at now + %s minutes" % wait_minutes
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    if not output.__contains__(str.encode("commands will be executed")):
        print("Error with the atd command:")
        print(str(output).replace("\\n", "\n").strip("b").strip("'"))
        exit(1)

# get the arguments using python's argparse module:
parser = argparse.ArgumentParser(description="pass/atd wrapper for writing and deleting sensitive files")
parser.add_argument('-t', '--time', type=int, help='minutes before deleting the file (0 for never)', required=False, default=600)
parser.add_argument('account', metavar='ACCOUNT', type=str, nargs=1, help='the account to be unlocked by pass')
args = vars(parser.parse_args())

account = args['account'][0]

# Run the command
cmd = "pass files/%s" % account
ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
output, err = ps.communicate()
retcode = ps.returncode

# Check for errors
if retcode == 1:
    print("pass returned code 1 - account not found")
    exit(1)
elif err != None:
    print("pass sent the following to stderr:")
    print(err)
    exit(2)

output_lines = output.decode("utf-8").split('\n')

# now its time to write the data to a file
# the first line should be the path the data will be written to
dest = get_path(output_lines[0])

with open(dest, "w") as outfile:
    for line in output_lines[1:-1]:
        outfile.write(line + "\n")
    # handle the last line outside of the loop to avoid adding an extra newline
    outfile.write(output_lines[-1])
print("successfully wrote to %s" % dest)

# now we add a job to atd to delete the plaintext after a certain amount of time
delete_time = args['time']
# don't delete if the user provides 0 or a negative time value
if delete_time < 1:
    exit(0)
delete_file(delete_time, dest)
print("added an atd job to delete %s in %s minutes" % (dest, delete_time))
