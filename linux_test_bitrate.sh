#!/usr/bin/env bash

case $1 in
  ""|-h|--help)
    echo "Test throughput between two computers"
    echo "  $0 server"
    echo "  $0 client <server_ip>"
    ;;
  server) exec iperf -s;;
  client) exec iperf -c "$2";;
esac
