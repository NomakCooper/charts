#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, Marco Noce <marco.X0178421@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: write_charts
author:
    - Marco Noce (@NomakCooper)
description:
    - Generate charts in image format on the ansible control node.
requirements:
  - Plotly Python Library
  - Tenacity Python Library
  - Packaging Python Library
  - Kaleido Python Library
short_description: Generate charts in image format on the ansible control node.
notes:
  - |
    this module generates image files in the control node. To use this module, the python library Plotly is required
options:
    type:
        description:
            - The chart type.
        required: true
        type: str
        choices:
            - line
            - bar
            - pie
            - donut
    titlechart:
        description:
            - The chart title.
        required: false
        type: str
    imgwidth:
        description:
            - The image file width.
        required: false
        type: int
        default: 1920
    imgheight:
        description:
            - The image file height.
        required: false
        type: int
        default: 1080
    format:
        description:
            - The image file format.
        required: false
        type: str
        default: png
        choices:
            - png
            - jpeg
            - webp
            - svg
            - pdf
            - eps
    path:
        description:
            - The path where the image file should be saved.
        required: true
        type: str
    filename:
        description:
            - The name of the image file
        required: true
        type: str
    xaxis:
        description:
            - The X axis data.
        required: false
        type: list
        elements: str
    xaxisname:
        description:
            - The X axis title name.
        required: false
        type: str
    yaxis:
        description:
            - The Y axis data.
        required: false
        type: list
    yaxisname:
        description:
            - The Y axis title name.
        required: false
        type: list
        elements: str
    yaxiscolor:
        description:
            - The Y axis color.
        required: false
        type: list
        elements: str
    shape_line:
        description:
            - The chart chape line.
        required: false
        type: str
        choices:
            - spline
            - linear
    fontsize:
        description:
            - The text font size.
        required: false
        type: int
        default: 18
    fontcolor:
        description:
            - The text font color.
        required: false
        type: str
        default: "#000000"
    titlelegend:
        description:
            - The legend title.
        required: false
        type: str
    slicedata:
        description:
            - The pie/donut chart data.
        required: false
        type: list
    slicelabel:
        description:
            - The pie/donut chart labels.
        required: false
        type: list
        elements: str
    slicecolor:
        description:
            - The pie/donut chart color.
        required: false
        type: list
        elements: str
    sizehole:
        description:
            - The size of the hole in the centre of the donut chart
        required: false
        type: float
        default: .5
'''

EXAMPLES = r'''
- name: set line axis data
  set_fact:
    xdata: ['00:00','02:00','04:00','06:00','08:00','10:00','12:00','14:00','16:00','18:00','20:00','22:00']
    y1data: [20,20,30,40,50,80,70,60,40,30,20,10]
    y2data: [05,15,25,20,45,50,40,35,30,20,15,05]

- name: run line chart
  become: false
  write_charts:
    titlechart: "Day Performance"
    type: line
    xaxis: '{{xdata}}'
    xaxisname: "Date time"
    yaxis:
    - '{{y1data}}'
    - '{{y2data}}'
    yaxisname:
    - "%cpu"
    - "%memory"
    yaxiscolor:
    - "#1500ff"
    - "#ff00b7"
    titlelegend: "Line Legend"
    shape_line: "spline"
    imgwidth: 1920
    imgheight: 1080
    format: png
    path: /tmp/chart_collection
    filename: "day_performance_linechart"
  register: chartline
  delegate_to: localhost

- name: run bar chart
  become: false
  write_charts:
    titlechart: "Day Performance"
    type: bar
    xaxis: '{{xdata}}'
    xaxisname: "Date time"
    yaxis:
    - '{{y1data}}'
    - '{{y2data}}'
    yaxisname:
    - "%cpu"
    - "%memory"
    yaxiscolor:
    - "#1500ff"
    - "#ff00b7"
    imgwidth: 1920
    imgheight: 1080
    format: png
    path: /tmp/chart_collection
    filename: "day_performance_barchart"
  register: chartbar
  delegate_to: localhost

- name: set pie fact
  set_fact:
    pielabel: ['sys','dba','webservice','application']
    piedata: [10, 50, 20, 20]
    piecolor: ["#1500ff", "#ff000d", "#eaff00", "#8700e8"]

- name: run pie chart
  become: false
  write_charts:
    titlechart: "cpu usage"
    type: pie
    slicedata: '{{piedata}}'
    slicelabel: '{{pielabel}}'
    slicecolor: '{{piecolor}}'
    imgwidth: 1920
    imgheight: 1080
    format: png
    path: /tmp/chart_collection
    filename: "cpu_usage_piechart"
  register: chartpie
  delegate_to: localhost

- name: run donut chart
  become: false
  write_charts:
    titlechart: "cpu usage"
    type: donut
    slicedata: '{{piedata}}'
    slicelabel: '{{pielabel}}'
    slicecolor: '{{piecolor}}'
    sizehole: .5
    imgwidth: 1920
    imgheight: 1080
    format: png
    path: /tmp/chart_collection
    filename: "cpu_usage_donutchart"
  register: chartpie
  delegate_to: localhost

'''

RETURN = r'''
changed:
    description: The change status.
    type: bool
    returned: if image files have been generated
    sample: true
'''

from ansible.module_utils.basic import AnsibleModule
from plotly import graph_objects as go


def run_module():

    module_args = dict(

        titlechart=dict(type='str'),
        type=dict(type='str', required=True, choices=['line', 'bar', 'pie', 'donut']),

        xaxis=dict(type='list', default=['']),
        xaxisname=dict(type='str'),
        yaxis=dict(type='list', default=['']),
        yaxisname=dict(type='list', default=['']),
        yaxiscolor=dict(type='list', default=['']),

        imgwidth=dict(type='int', default=1920),
        imgheight=dict(type='int', default=1080),
        shape_line=dict(type='str', choices=['spline', 'linear']),

        format=dict(type='str', default='png', choices=['png', 'jpeg', 'webp', 'svg', 'pdf', 'eps']),
        path=dict(type='str', required=True),
        filename=dict(type='str', required=True),
        fontsize=dict(type='int', default=18),
        fontcolor=dict(type='str', default='#000000'),

        titlelegend=dict(type='str'),

        slicedata=dict(type='list', default=['']),
        slicelabel=dict(type='list', default=['']),
        slicecolor=dict(type='list', default=['']),

        sizehole=dict(type='float', default=.5),
    )

    result = dict(
        changed=False
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    charttype = module.params['type']

    if charttype == "line" or charttype == "bar":

        xdata = module.params.get('xaxis')

        fig = go.Figure()

        ydata = module.params.get('yaxis')
        yname = module.params.get('yaxisname')
        ycolor = module.params.get('yaxiscolor')

        if charttype == "line":
            shape = module.params.get('shape_line')

        fileformat = module.params.get('format')
        filepath = module.params.get('path')
        imgname = module.params.get('filename')

        if charttype == "line":
            for multidata, multiname, multicolor in zip(ydata, yname, ycolor):
                fig.add_trace(go.Scatter(x=xdata, y=multidata, name=multiname, line_color=multicolor, line_shape=shape))

        if charttype == "bar":
            for multidata, multiname, multicolor in zip(ydata, yname, ycolor):
                fig.add_trace(go.Bar(x=xdata, y=multidata, name=multiname, marker_color=multicolor))

        if len(yname) > 1:
            fig.update_layout(
                autosize=False,
                width=module.params.get('imgwidth'),
                height=module.params.get('imgheight'),
                title=module.params.get('titlechart'),
                xaxis_title=module.params.get('xaxisname'),
                legend_title=module.params.get('titlelegend'),
                font=dict(
                    family="Courier New, monospace",
                    size=module.params.get('fontsize'),
                    color=module.params.get('fontcolor')
                )
            )
        else:
            fig.update_layout(
                autosize=False,
                width=module.params.get('imgwidth'),
                height=module.params.get('imgheight'),
                title=module.params.get('titlechart'),
                xaxis_title=module.params.get('xaxisname'),
                yaxis_title=' '.join(map(str, module.params.get('yaxisname'))),
                legend_title=module.params.get('titlelegend'),
                font=dict(
                    family="Courier New, monospace",
                    size=module.params.get('fontsize'),
                    color=module.params.get('fontcolor')
                )
            )

        fig.write_image(filepath + "/" + imgname + "." + fileformat)

    if charttype == "pie" or charttype == "donut":

        pievalue = module.params.get('slicedata')
        pielabel = module.params.get('slicelabel')
        piecolor = module.params.get('slicecolor')

        fileformat = module.params.get('format')
        filepath = module.params.get('path')
        imgname = module.params.get('filename')

        fig = go.Figure()

        if charttype == "pie":
            fig.add_trace(go.Pie(labels=pielabel, values=pievalue, marker=dict(colors=piecolor)))

        if charttype == "donut":
            holesize = module.params.get('sizehole')
            fig.add_trace(go.Pie(labels=pielabel, values=pievalue, marker=dict(colors=piecolor), hole=holesize))

        fig.update_layout(
            autosize=False,
            width=module.params.get('imgwidth'),
            height=module.params.get('imgheight'),
            title_text=module.params.get('titlechart'),
            font=dict(
                family="Courier New, monospace",
                size=module.params.get('fontsize'),
                color=module.params.get('fontcolor')
            )
        )

        fig.write_image(filepath + "/" + imgname + "." + fileformat)

    if module.check_mode:
        module.exit_json(**result)

    result['changed'] = True

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
