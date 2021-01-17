# christmas_pi, A program for Controlling Christmas Tree lights and more

Christmas Pi is a suite of two programs and several plugins for displaying
colorful patterns on a NeoPixel LED string. The first program, **xmastree**, is
for directly connected strings while the second program **porchlamps** is for
remotely stringssending out the patterns via the sACN protocol over the
network.

## Command Line

>**xmas\_tree** [options]

>**porchlamps** [options]

## Options

>-brightness=<value\> # Set overall brightness (0-100)

>-config=<filename\> # Name of config file of options

>-dir=<path\> # chdir to *path*

>-interval=<val\> # Sets the number of seconds to cycle between patterns

>-numlamps=<val\> # Sets the number of lamps in the string.

>-pattern=<pattern_list\> # Comma separated (no spaces) of names of patterns to run

### Options specific to porchlamps.py
>-ipaddr=<address\> # Sets the ip address of the sACN device controlling the

>string of laps

>-on\_times=<time_ranges\> # Comma separated time ranges (no spaces)

>**time ranges** 

>Time ranges are defined as an on time and an off time pair relative to midnight. The
>time is defined as *HH:MM*, while the time range is defines as *<time>-<time>*.
>The list is them defined as *-on\_times=<range>,<range>...<range>*.

### Config Files
Parameters for the operation can be stored into configuration file and passed
to either of the programs using the *-config=<filename>* option.

The any option, one per line and without the 'hyphen', can be included in the
config file, one per line. The options on the command line will take precedence
over those in the configuration file. 

### An example configuration file for porchlamps.py:

>numlamps=90

>brightness=100

>pattern=glitter

>pattern=candycane,randomcolors,random\_glitter,randomfade,christmas

>interval=180

>ipaddr=10.3.141.131

>on\_times=05:00-08:00,16:00-23:00

>dir=/home/pi/porchlamps


## Plugins
The *plugins* are small python modules that will be searched for in the folder
*<dir>./plugin/*. An object for each the plugins found in that folder will be be created, but
only those plugins listed in the *plugin* option will be sequenced through.

## Anatomy of a Plugin
A plugin consists of a uniquely named class object and a helper function named
*load_plugin()*. The helper fnction instantiates the class object for the
plugin and returns it.

The plugin *plugin/candycane.py* has comments describing the required functions
their paramters to make a plugin.
