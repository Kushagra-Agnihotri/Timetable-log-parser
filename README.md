# Timetable log Parser
A tiny, dependency-free Python parser that reads your timetable.log and prints a concise report:

>total API requests and HTTP status counts

>endpoint popularity (request counts)

>per-endpoint performance (average + max response times in ms)

>timetable generation summary (total timetables found, calls, avg per call)

>algorithm usage counts (e.g. Heuristic Backtracking)

>unique user IDs and per-year unique coun

## Requirements

>Python 3.7+ 

>No external packages (uses collections from stdlib)

## Installation / Setup

Clone or download the repo:

>git clone https://github.com/Kushagra-Agnihotri/Timetable-log-parser
>cd timetable-log-parser


Put your log file in the repo folder (or note absolute path). The script uses P = "timetable.log" by default — edit that or pass your path by changing the PATH variable.
