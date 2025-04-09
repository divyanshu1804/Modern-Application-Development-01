wrong_inputs="""
<!DOCTYPE html>
<html>
<head> 
    <title>Something Went Wrong</title>
</head>
<body> 
    <h1>Wrong Inputs</h1>
    <p><strong>Something went wrong</strong></p>
</body>
</html>
    
"""

student_details="""
<!DOCTYPE html>
<html>
<head> 
    <title>Student Details</title>
</head>
<body>
    <h1>Student Details</h1>
    <table border="1">
        <thead>
            <tr>
                <th>Student id</th>
                <th>Course id</th>
                <th>Marks</th>
            </tr>
        </thead>
        <tbody>
        {% for row in data %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
            </tr>
        {% endfor %}
        <tr>
            <td colspan="2" align ="centre">Total Marks</td>
            <td>{{ Sum }}</td>
        </tr>
        </tbody>
    </table>
</body>
</html>
"""
course_details="""
<!DOCTYPE html>
<html>
<head>
    <title>Course Data </title>
</head>
<body>
    <h1>Course Details</h1>
    <table border="1">
        <thead>
            <tr>
                <th>Average Marks</th>
                <th>Maximum Marks</th>
                <tr>
        </thead>
        <tbody>
            <tr>
                <td>{{ avg }}</td>
                <td>{{ max }}</td>
            </tr>
        </tbody>
    </table>
    <img src={{ image }}>
</body>
</html>
"""

import sys
from jinja2 import Template as temp
import matplotlib.pyplot as plt

name1=sys.argv[1]
id=int(sys.argv[2])
data=[]
with open('data.csv','r') as file:
    file.readline()
    if name1=="-s":
        for row in file:
            row=list(map(int,row.strip().split(',')))
            if row[0]==id:
                data.append(row)
    elif name1=="-c":
        for row in file:
            row=list(map(int,row.strip().split(',')))
            if row[1]==id:
                data.append(row)
                   
if len(data)==0:
        with open('output.html','w') as output:
            output.write(wrong_inputs)
elif name1=="-s":
        sum=sum(x[2] for x in data) 
        template=temp(student_details)
        with open('output.html','w') as output:
            output.write(template.render(data=data,Sum=sum))
else:
    marks=[x[2] for x in data if x[1]==id]
    avg=sum(marks)/len(marks)
    max=max(marks)
    plt.hist(marks)
    plt.xlabel('Marks')
    plt.ylabel('Frequency')
    plt.savefig('graph.png')
    template=temp(course_details)
    with open('output.html','w') as output:
        output.write(template.render(avg=avg,max=max,image='graph.png'))
        
                
            
            