#!/usr/bin/python
import argparse
parser = argparse.ArgumentParser()
osnames = ['darwin', 'linux', 'vmkernel', 'windows']
parser.add_argument('-v', '--vmx', help='vmx file', dest='vmx', action='store', type=argparse.FileType('r+b'))
parser.add_argument('-d', '--vmx-debug', help='vmx-debug file', dest='vmx_debug', action='store', type=argparse.FileType('r+b'))
parser.add_argument('-s', '--vmx-stats', help='vmx-stats file', dest='vmx_stats', action='store', type=argparse.FileType('r+b'))
parser.add_argument('-b', '--vmbase', help='vmwarebase file', dest='vmwarebase', action='store', type=argparse.FileType('r+b'))
parser.add_argument('-k', '--vmkctl', help='vmkctl file', dest='vmkctl', action='store', type=argparse.FileType('r+b'))
parser.add_argument('-o', '--osname', help='OS type', dest='osname', action='store', choices=osnames)
args = parser.parse_args()

parser.print_help()
print args
