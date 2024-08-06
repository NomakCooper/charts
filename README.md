<meta name="author" content="Marco Noce">
<meta name="description" content="Ansible write_charts generate charts in image format on the ansible control node.">
<meta name="copyright" content="Marco Noce 2024">
<meta name="keywords" content="ansible, module, write, charts, image">

<div align="center">

![Ansible Custom Module][ansible-shield]
![ansible charts][charts shield]
![python][python-shield]
![license][license-shield]

</div>

### write_charts ansible custom module

#### Description :

<b>write_charts</b> is a custom module for ansible that generate charts in image format on the ansible control node.

#### Purpose :

The purpose of this project is to use ansible's control node to generate charts in image format. To do this, some of the functions of the Python Plotly library are used.<br>
This module is very basic and uses only a few functions in comparison with the vast number of possibilities offered by the Plotly library.

* [Official link Plotly Python]
* [Official link Plotly Python GitHub]

It is currently possible to generate charts of this type:
*  line
*  bar
*  pie
*  donut

In images of these formats:
*  png
*  jpeg
*  webp
*  svg
*  pdf
*  eps

#### Repo files:

```
├── /library                
│   └── write_charts.py     ##<-- python custom module
```

#### Requirements :

First of all, in order to use this module you <b>MUST</b> have installed the necessary library on your control node and/or in your environment.<br>
Precisely this module uses plotly 5.22.0

Python lib:
*  Plotly
*  Kaleido

Depending on the libraries already present, you may also need:
* Tenacity
* Packaging

You can install these libraries directly from <code>pip</code><br>
If you have no way of modifying your control node or environment, you can install the libraries by the [pip module] directly via the playbook that will use this module.

SAMPLE:
```yaml
  - name: Install plotly
    become: false
    ansible.builtin.pip:
      name: plotly=5.22.0
    delegate_to: localhost
```
You can also install the libraries via <b>.whl</b> files
```yaml
  - name: Install plotly
    become: false
    ansible.builtin.pip:
      name: /tmp/plotly-5.22.0-py3-none-any.whl
    delegate_to: localhost
```

#### Parameters :

|Parameter|Type  |Required|Sample                      |Comment                                                                                                                 |
|---------|------|--------|----------------------------|------------------------------------------------------------------------------------------------------------------------|
|type|string|true|"line"|The chart type. Choice: <b>line</b> - <b>bar</b> - <b>pie</b> - <b>donut</b> |
|titlechart|string|false|"sample title"|The chart title.|
|imgwidth|int|false|1920|The image file width.|
|imgheight|int|false|1080|The image file height.|
|format|string|false|"png"|The image file format. Choice: <b>png</b> - <b>jpeg</b> - <b>webp</b> - <b>svg</b> - <b>pdf</b> - <b>eps</b>|
|path|string|true|"/tmp/output"|The path where the image file should be saved.|
|filename|string|true|"sample_name"|The name of the image file|
|xaxis|list|line/bar|['00:00','02:00','04:00']|The X axis data.|
|xaxisname|string|line/bar|"Time"|The X axis title name.|
|yaxis|list|line/bar|[20,20,30]|The Y axis data.|
|yaxisname|list|line/bar|["cpu","memory"]|The Y axis title name.|
|yaxiscolor|list|line/bar|["#1500ff","#ff00b7"]|The Y axis color.|
|shape_line|string|line|"spline"|The chart shape line. Choice: <b>spline</b> - <b>linear</b>|
|fontsize|int|false|18|The text font size.|
|fontcolor|string|false|"#000000"|The text font color.|
|titlelegend|string|false|"sample legend"|The legend title.|
|slicedata|list|pie/donut|[20, 80]|The pie/donut chart data.|
|slicelabel|list|pie/donut|['sys','dba']|The pie/donut chart labels.|
|slicecolor|list|pie/donut|["#1500ff","#ff00b7"]|The pie/donut chart color.|
|sizehole|float|donut|.5|The size of the hole in the centre of the donut chart|

#### Attributes :

|Attribute |Support|Description                                                                         |
|----------|-------|------------------------------------------------------------------------------------|
|check_mode|full   |Can run in check_mode and return changed status prediction without modifying target.|

#### EXAMPLES :

* Some theoretical examples can be found in [EXAMPLES.md] file

* Below are two more practical examples of how to transform data into charts.

[![swap-barchart.png](https://i.postimg.cc/Hxf05NQk/swap-barchart.png)](https://postimg.cc/ftf0QB2G)
This portion of code converts the data collected yesterday by sar on the swap usage of a linux host into the bar chart above.
```yaml
---
  vars:
    LCTIME: "LC_TIME=en_UK.utf8"
    DAY: "yesterday"
    EGREP: "Linux|RESTART|%|Average|^$"

  tasks:
  - name: Create directory on localhost
    become: false
    ansible.builtin.file:
      path: /tmp/chart_collection
      state: directory
    delegate_to: localhost

  - name: collect swap sar output
    shell: "{{LCTIME}} sar -f /var/log/sa/sa$(date +%d -d '{{DAY}}') -S | egrep -v '{{EGREP}}' | awk '{print $1,$4,$6}'"
    register: sarcmd

  - name: set bar axis data
    set_fact:
      xdata: "{{ xdata|default([]) + [item.split(' ')[0]] }}"
      y1data: "{{ y1data|default([]) + [item.split(' ')[1] | float]}}"
      y2data: "{{ y2data|default([]) + [item.split(' ')[2] | float]}}"
    with_items:
      - "{{ sarcmd.stdout_lines}}"

  - name: run bar chart
    become: false
    write_charts:
      titlechart: "Swap Summary"
      type: bar
      xaxis: '{{xdata}}'
      xaxisname: Time
      yaxis: 
      - '{{y1data}}'
      - '{{y2data}}'
      yaxisname: 
      - "%swpused"
      - "%swpcad"
      yaxiscolor:
      - "#1500ff"
      - "#ff00b7"
      imgwidth: 1920
      imgheight: 1080
      format: png
      path: /tmp/chart_collection
      filename: "swap_barchart"
    delegate_to: localhost
```

[![ldavg-linechart.png](https://i.postimg.cc/k5WjvZNG/ldavg-linechart.png)](https://postimg.cc/Z9KFTwMz)

This portion of code converts the data collected yesterday by sar on the load average of a linux host into the line chart above.
```yaml
---
  vars:
    LCTIME: "LC_TIME=en_UK.utf8"
    DAY: "yesterday"
    EGREP: "Linux|RESTART|ldavg|Average|^$"

  tasks:
  - name: Create directory on localhost
    become: false
    ansible.builtin.file:
      path: /tmp/chart_collection
      state: directory
    delegate_to: localhost

  - name: collect ldavg sar output
    shell: "{{LCTIME}} sar -f /var/log/sa/sa$(date +%d -d '{{DAY}}') -q | egrep -v '{{EGREP}}' | awk '{print $1,$4,$5,$6}'"
    register: sarcmd

  - name: set line axis data
    set_fact:
      xdata: "{{ xdata|default([]) + [item.split(' ')[0]] }}"
      y1data: "{{ y1data|default([]) + [item.split(' ')[1] | float]}}"
      y2data: "{{ y2data|default([]) + [item.split(' ')[2] | float]}}"
      y3data: "{{ y3data|default([]) + [item.split(' ')[3] | float]}}"
    with_items:
      - "{{ sarcmd.stdout_lines}}"

  - name: run line chart
    become: false
    write_charts:
      titlechart: "Load Average Summary"
      type: line
      xaxis: '{{xdata}}'
      xaxisname: Time
      yaxis: 
      - '{{y1data}}'
      - '{{y2data}}'
      - '{{y3data}}'
      yaxisname: 
      - "ldavg-1"
      - "ldavg-5"
      - "ldavg-15"
      yaxiscolor:
      - "#1500ff"
      - "#ff00b7"
      - "#f007c9"
      titlelegend: "ldavg Legend"
      shape_line: "spline"
      imgwidth: 1920
      imgheight: 1080
      format: png
      path: /tmp/chart_collection
      filename: "ldavg_linechart"
    delegate_to: localhost
```

#### Return :

*  This module return <code>'changed': True</code> when image file is written.

|Key              |Type     |Sample |
|-----------------|---------|-------|
|changed          |boolean  |True   |                                                                               |

## Integration

1. Assuming you are in the root folder of your ansible project.

Specify a module path in your ansible configuration file.

```shell
$ vim ansible.cfg
```
```ini
[defaults]
...
library = ./library
...
```

Create the directory and copy the python modules into that directory

```shell
$ mkdir library
$ cp path/to/module library
```

2. If you use Ansible AWX and have no way to edit the control node, you can add the /library directory to the same directory as the playbook .yml file

```
├── root repository
│   ├── playbooks
│   │    ├── /library                
│   │    │   └── write_charts.py        ##<-- python custom module
│   │    └── your_playbook.yml          ##<-- you playbook
```   

[ansible-shield]: https://img.shields.io/badge/Ansible-custom%20module-blue?style=for-the-badge&logo=ansible&logoColor=lightgrey
[charts shield]: https://img.shields.io/badge/ansible-write_charts-blue?style=for-the-badge&logo=ansible&logoColor=white
[python-shield]: https://img.shields.io/badge/python-blue?style=for-the-badge&logo=python&logoColor=yellow
[license-shield]: https://img.shields.io/github/license/nomakcooper/svcs_attr_facts?style=for-the-badge&label=LICENSE

[Official link Plotly Python]: https://plotly.com/python/
[Official link Plotly Python GitHub]: https://github.com/plotly/plotly.py

[pip module]: https://docs.ansible.com/ansible/latest/collections/ansible/builtin/pip_module.html

[EXAMPLES.md]: EXAMPLES.md
