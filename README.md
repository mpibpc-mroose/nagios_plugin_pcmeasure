# Nagios Plugin for MessPC.de Ethernet Boxes

[![Build Status](https://travis-ci.org/mpibpc-mroose/nagios_plugin_pcmeasure.svg?branch=master)](https://travis-ci.org/mpibpc-mroose/nagios_plugin_pcmeasure)

An implementation for Perl already exists:
https://exchange.nagios.org/directory/Plugins/Hardware/Environmental/MessPC--2F-pcmeasure/details

... but is not maintained.

So I decided to implement it's functionality in Python.

There is no warranty for a 100% compatibilty to the old plugin, but
requests for adaptions and error reports are always welcome.

# How to use it

1. copy `check_pcmeasure.py' to your Nagios plugin folder
1. define a nagios command:
```
define command{
    command_name       check_messpc
    command_line       $USER1$/check_pcmeasure.py -H $HOSTADDRESS$ -w $ARG1$ -c $ARG2$ -S $ARG3
}
```
1. define a service
```
define service{
    use                     generic-service
    host_name               messpc.example.com
    service_description     temperature sensor
    check_command           check_messpc!28!30!com1.1
}
```