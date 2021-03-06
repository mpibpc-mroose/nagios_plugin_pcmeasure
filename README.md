![GitHub release](https://img.shields.io/github/release/mpibpc-mroose/nagios_plugin_pcmeasure.svg) 
![GitHub](https://img.shields.io/github/license/mpibpc-mroose/nagios_plugin_pcmeasure.svg?color=blue) 
![code coverage 100%](https://img.shields.io/badge/coverage-100%25-brightgreen.svg) 

# check_pcmeasure.py 
Nagios/Icinga2 Plugin for https://messpc.de/ and https://pcmeasure.com Ethernet Boxes written in Python 3

An implementation for Perl already exists:
https://exchange.nagios.org/directory/Plugins/Hardware/Environmental/MessPC--2F-pcmeasure/details

... but is not maintained.

So I decided to implement it's functionality in Python.

There is no warranty for a 100% compatibility to the old plugin, but
requests for adaptions and error reports are always welcome.

# How to use it
## Example commandline
```
root@icinga-agent01:/usr/lib/nagios/plugins# ./check_pcmeasure.py -H 10.10.200.250 -S com1.1 -w 45 -c 55 -l 'celsius'
OK: 27.8 celsius | celsius=27.8
```

## Config files:
- copy `check_pcmeasure.py' to your Nagios/Icinga plugin folder
- define a command:
```
define command{
    command_name       check_pcmeasure
    command_line       $USER1$/check_pcmeasure.py -H $HOSTADDRESS$ -w $ARG1$ -c $ARG2$ -S $ARG3 -l $ARG4
}
```
- define a service
```
define service{
    use                     generic-service
    host_name               pcmeasure.example.com
    service_description     temperature sensor
    check_command           check_pcmeasure!28!30!com1.1!celsius
}
```
## Director:
- Icinga Director -> Define Data Fields:

|Label|Field name|
|-----|----------|
|Critical|critical|
|Warning|warning|
|Etherbox address|etherbox_address|
|Etherbox sensor label|etherbox_sensor_label|
|Etherbox sensor name|etherbox_sensor_name|
- Icinga Director -> Commands -> Templates -> Add:
![screenshot](https://s3.gifyu.com/images/check_pcmeasure_command_template.png)
- Click on "Fields":
![screenshot](https://s3.gifyu.com/images/check_pcmeasure_command_template_fields.png)
- Icinga Director -> Commands -> Commands -> Add:
![screenshot](https://s3.gifyu.com/images/check_pcmeasure_command.png)
- Click on "Arguments"
![screenshot](https://s3.gifyu.com/images/check_pcmeasure_command_arguments.png)
- Create a service as usual ...
- Enjoy :)
![screenshot](https://s3.gifyu.com/images/perfdata_icinga.png)