import sys
from jinja2 import Template as temp # type: ignore
import matplotlib.pyplot as plt # type: ignore

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
            <td colspan="2" align="center">Total Marks</td>
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
    <title>Course Data</title>
</head>
<body>
    <h1>Course Details</h1>
    <table border="1">
        <thead>
            <tr>
                <th>Average Marks</th>
                <th>Maximum Marks</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{{ avg }}</td>
                <td>{{ max_marks }}</td>
            </tr>
        </tbody>
    </table>
    <img src="{{ image }}">
</body>
</html>
"""

name1 = sys.argv[1]
id = int(sys.argv[2])
data = []

with open('data.csv', 'r') as file:
    file.readline()  # Skip header
    for row in file:
        row = list(map(int, row.strip().split(',')))
        if name1 == "-s" and row[0] == id:
            data.append(row)
        elif name1 == "-c" and row[1] == id:
            data.append(row)

if not data:
    with open('output.html', 'w') as output:
        output.write(wrong_inputs)
elif name1 == "-s":
    total_marks = sum(x[2] for x in data)
    template = temp(student_details)
    with open('output.html', 'w') as output:
        output.write(template.render(data=data, Sum=total_marks))
else:
    marks = [x[2] for x in data]
    if marks:  
        avg = sum(marks) / len(marks)
        max_marks = max(marks)
        plt.hist(marks)
        plt.xlabel('Marks')
        plt.ylabel('Frequency')
        plt.savefig('graph.png')
        plt.close()
        template = temp(course_details)
        with open('output.html', 'w') as output:
            output.write(template.render(avg=avg, max_marks=max_marks, image='graph.png'))
