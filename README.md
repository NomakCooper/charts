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

---

> [!warning]
> **This repository has been archived. The module is available via Ansible galaxy collection [nomakcooper.collection](https://galaxy.ansible.com/ui/repo/published/nomakcooper/collection/).**
---
### charts ansible custom module

#### Description : :information_source:

<b>charts</b> is a custom module for ansible that generate charts in image format on the ansible control node.

#### Purpose : :eyes:

The purpose of this project is to use ansible's control node to generate charts in image format. 
To do this, some of the functions of the Python Plotly library are used.<br>
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

#### Repo files: :open_file_folder:

```
├── /library                
│   └── write_charts.py     ##<-- python custom module
```

#### Requirements : :heavy_check_mark:

First of all, in order to use this module you <b>MUST</b> have installed the necessary library on your control node and/or in your environment.<br>

Python lib:
*  Plotly
*  Kaleido

You can install these libraries directly from <code>pip</code><br>
If you have no way of modifying your control node or environment, you can install the libraries by the [pip module] directly via the playbook that will use this module.

SAMPLE: :arrow_forward:
```yaml
  - name: Install plotly
    become: false
    ansible.builtin.pip:
      name: plotly=6.0.0
    delegate_to: localhost
```
You can also install the libraries via <b>.whl</b> files
```yaml
  - name: Install plotly
    become: false
    ansible.builtin.pip:
      name: /tmp/plotly-6.0.0-py3-none-any.whl
    delegate_to: localhost
```

#### Parameters : :clipboard:

| Parameter      | Type      | Required | Sample                                      | Comment |
|--------------|----------|----------|--------------------------------|----------------------------------------------------------------------------------------------------------------|
| **titlechart**   | `str`    | ❌ No    | `"CPU Usage Over Time"`         | Title displayed at the top of the chart. |
| **type**        | `str`    | ✅ Yes   | `"line"`                        | Type of chart. Options: `"line"`, `"bar"`, `"pie"`, `"donut"`. |
| **xaxis**       | `list`   | ❌ No    | `["2025-02-06T12:10", "2025-02-06T12:20"]` | X-axis data values (time or categories). |
| **xaxisname**   | `str`    | ❌ No    | `"Timestamp"`                   | Label for the X-axis. |
| **yaxis**       | `list`   | ❌ No    | `[[12.3, 14.5, 13.1], [5.2, 6.3, 5.8]]`  | List of Y-axis data series. |
| **yaxisname**   | `list`   | ❌ No    | `["User %", "System %"]`        | List of labels for Y-axis data series. |
| **yaxiscolor**  | `list`   | ❌ No    | `["red", "blue"]`               | Colors for each Y-axis series. |
| **imgwidth**    | `int`    | ❌ No    | `1920`                           | Width of the output image (pixels). |
| **imgheight**   | `int`    | ❌ No    | `1080`                           | Height of the output image (pixels). |
| **shape_line**  | `str`    | ❌ No    | `"spline"`                       | Shape of lines in `line` charts. Options: `"spline"`, `"linear"`. |
| **format**      | `str`    | ❌ No    | `"png"`                          | Output format. Options: `"png"`, `"jpeg"`, `"webp"`, `"svg"`, `"pdf"`, `"eps"`. |
| **path**        | `str`    | ✅ Yes   | `"/charts"`                      | Directory where the chart image is saved. |
| **filename**    | `str`    | ✅ Yes   | `"cpu_usage"`                    | Name of the saved image file (without extension). |
| **fontsize**    | `int`    | ❌ No    | `20`                             | Font size for text elements. |
| **fontcolor**   | `str`    | ❌ No    | `"#333333"`                      | Font color for all chart text. |
| **titlelegend** | `str`    | ❌ No    | `"CPU Breakdown"`                | Title displayed for the legend. |
| **slicedata**   | `list`   | ❌ No    | `[50, 30, 20]`                   | Values for `pie` or `donut` charts. |
| **slicelabel**  | `list`   | ❌ No    | `["Cache", "Swap", "RAM"]`       | Labels for `pie` or `donut` chart slices. |
| **slicecolor**  | `list`   | ❌ No    | `["orange", "blue", "green"]`    | Colors assigned to each slice in `pie` or `donut` charts. |
| **sizehole**    | `float`  | ❌ No    | `0.5`                            | Size of the hole in a `donut` chart (`0` for `pie`). |

#### Attributes : :clipboard:

|Attribute |Support|Description                                                                         |
|----------|-------|------------------------------------------------------------------------------------|
|check_mode|full   |Can run in check_mode and return changed status prediction without modifying target.|

#### EXAMPLES : :bar_chart:

![line-chart][cpu-file]
This portion of code converts the load average data collected by sar using my other module sar_facts.
```yaml
    - name: Collect CPU Usage Data
      sar_facts:
        type: "cpu"
        date_start: "2025-02-06"
        date_end: "2025-02-07"

    - name: Generate CPU Usage Line Chart
      charts:
        titlechart: "CPU Usage Over Time (Multi-Day)"
        type: "line"
        xaxis: "{{ ansible_facts.sar_cpu | map(attribute='date') | zip(ansible_facts.sar_cpu | map(attribute='time')) | map('join', 'T') | list }}"
        xaxisname: "Timestamp"
        yaxis:
          - "{{ ansible_facts.sar_cpu | selectattr('%user', 'defined') | map(attribute='%user') | map('float') | list }}"
          - "{{ ansible_facts.sar_cpu | selectattr('%system', 'defined') | map(attribute='%system') | map('float') | list }}"
          - "{{ ansible_facts.sar_cpu | selectattr('%idle', 'defined') | map(attribute='%idle') | map('float') | list }}"
        yaxisname: ["User %", "System %", "Idle %"]
        yaxiscolor: ["#FF5733", "#33A1FF", "#28A745"]
        imgwidth: 1920
        imgheight: 1080
        shape_line: "spline"
        format: "png"
        path: "/tmp"
        filename: "cpu_usage_chart_multi_day"
        titlelegend: "CPU Breakdown"
      delegate_to: localhost
```

#### Return :

*  This module return <code>'changed': True</code>

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
[sar]: https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/4/html/introduction_to_system_administration/s3-resource-tools-sar-sar#s3-resource-tools-sar-sar

[cpu-file]: cpu_usage_chart_multi_day.png
