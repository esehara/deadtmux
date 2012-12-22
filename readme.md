                                                                  
       ,--.                  ,--.  ,--.                               
     ,-|  | ,---.  ,--,--. ,-|  |,-'  '-.,--,--,--.,--.,--.,--.  ,--. 
    ' .-. || .-. :' ,-.  |' .-. |'-.  .-'|        ||  ||  | \  `'  /  
    \ `-' |\   --.\ '-'  |\ `-' |  |  |  |  |  |  |'  ''  ' /  /.  \  
     `---'  `----' `--`--' `---'   `--'  `--`--`--' `----' '--'  '--' 
                                                                

Why?
----

  tmux is powerful, and great terminal multiplexer. but, it is bother to
write shell script for layout tmux.Then, I write this script :).

My Test Environment
-------------------
* Ubuntu 12.10 and byobu
* tmux
* Python 2.7

Get Start !!
------------

Overview
=======
if you use Python:

    python setup.py install

and any configure yaml file (see example) write.

    deadtmux foobar.yaml foobar.sh

deadtmux makes shell script for tmux. and run.

    source foobar.sh

Write Configure Yaml
====================

please see example file.

deadtmux yaml file has tree parts in root:

    * configure
    * is_global
    * window

configure
---------

 configure example.

    - configure:
        - run: byobu (need)
        - focus-window: foobar (need)
        - focus-pane: 1 (need)

 **run** is method that run tmux.

 **focus-window** is, when done prepare layout tmux, tmux will focus it.
 **focus-pane** is, too, for pane.

window
------

 window example:

    - window:
        name: foobar
        panes:
          - send-keys:
            - send foobar
          - split-window: horizon

 **name** is window name.
 **panes** are each split pane setting. first pane have not to write **split-window**, but second pane (and after) have to write **split-window**. (because, deadtmux don't know how you want to split :) ).

panes
-----

 panes example:

    - panes:
        - send-keys:
            - cd foobar
        - resize:
            up: 10
        - export:
            foo: bar
        - alias:
            l: ls
        - workspace:
            root: /home/foobar/workspace/
            src: src

 **send-keys** is, when pane create, do send-keys .
 **resize** is pane resize. example, resize: up: 10  ->  'tmux resize-pane -U 10'.
 **export** is .. example, export: foo: bar -> 'export foo=bar'
 **alias** is .. example, alias: l: ls -> 'alias l=ls'
 **workspace** is create alias to each path.it needs 'root'. if root set, other is maked relative path from root.example, root is /home/foobar/workspace/, src is /home/foobar/workspace/src/

 panes can became global settings. it is is_global. it use any nest.. root, window. 
