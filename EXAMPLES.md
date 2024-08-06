#### Generate this line chart <code>day_performance_linechart.png</code> in <code>/tmp/chart_collection</code>:
[![day-performance-linechart.png](https://i.postimg.cc/QdsFk71m/day-performance-linechart.png)](https://postimg.cc/4mL4Xm8H)
```yaml
---
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
    delegate_to: localhost
```
#### Generate this bar chart <code>day_performance_barchart.png</code> in <code>/tmp/chart_collection</code> with same data:
[![day-performance-barchart.png](https://i.postimg.cc/L8YHrBL2/day-performance-barchart.png)](https://postimg.cc/21YRWW0K)
```yaml
---
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
    delegate_to: localhost 
```
#### Generate this bar chart <code>day_performance_barchart.png</code> in <code>/tmp/chart_collection</code> with same X data but only one Y Data :
[![day-performance-barchart-1.png](https://i.postimg.cc/mgC6KtXt/day-performance-barchart-1.png)](https://postimg.cc/MnZDQK8S)
```yaml
---
  - name: run bar chart
    become: false
    write_charts:
      titlechart: "Day Performance"
      type: bar
      xaxis: '{{xdata}}'
      xaxisname: "Date time"
      yaxis: 
      - '{{y1data}}'
      yaxisname: 
      - "%cpu"
      yaxiscolor:
      - "#1500ff"
      imgwidth: 1920
      imgheight: 1080
      format: png
      path: /tmp/chart_collection
      filename: "day_performance_barchart"
    delegate_to: localhost
```
#### Generate this pie chart <code>cpu_usage_piechart.png</code> in <code>/tmp/chart_collection</code>:
[![cpu-usage-piechart.png](https://i.postimg.cc/YSXj7qjw/cpu-usage-piechart.png)](https://postimg.cc/d7yJmF8W)
```yaml
---
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
    delegate_to: localhost
```
#### Generate this donut chart <code>cpu_usage_donutchart.png</code> in <code>/tmp/chart_collection</code> with same data:
[![cpu-usage-donutchart.png](https://i.postimg.cc/C5g36bYM/cpu-usage-donutchart.png)](https://postimg.cc/hz2ZXzfN)
```yaml
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
    delegate_to: localhost
```
