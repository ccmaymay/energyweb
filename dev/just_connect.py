#!/usr/bin/env python


import socket


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('172.31.10.11', 4001))
    s.close()


if __name__ == '__main__':
    main()
