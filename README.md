# Realtime-System-Monitoring-Solution

***

# Introduction

This project introduces an innovative IT lab monitoring system designed to address a common challenge: ensuring students’ productive engagement in the computer lab environment. Typically, computers in IT labs are oriented away from the teacher’s view, which can lead to distractions like gaming or other non-educational activities. Our system empowers teachers to effectively monitor and manage students’ activities, fostering a conducive learning environment. Beyond educational settings, this monitoring solution can find applications in various sectors where effective surveillance and supervision are essential.

# Problem

In many computer labs, there’s no way for teachers to see what students are doing on the computers. It’s impossible to supervise all the students individually, which leads to students sometimes using the computers for things unrelated to their studies.

# Aim

To create an effective monitoring system that empowers teachers to supervise and guide students’ activities in computer labs, promoting a productive and focused learning environment.

# Proposed Solution

Our IT lab monitoring system offers a comprehensive set of features to address the challenges identified in the problem statement. The proposed solution aims to create a conducive and monitored learning environment for students and teachers alike. Key features of the system include:

## 1. Live Student Screen Preview:
One of the core elements of our system is the ability to provide teachers with a real-time live preview of students' computer screens. This
feature allows teachers to instantly monitor and assess the tasks and activities of each student, ensuring they stay on track with their assignments.
## 2. Live File System Monitoring:
In addition to screen previews, our system also tracks changes made by students within the file system. Any modifications to files, folders, or the
addition/removal of content are shared in real-time with the teacher. This feature enhances the level of supervision and allows teachers to quickly identify and address any deviations from the educational tasks.
## 3. Direct Messaging Capability:
Our system also includes a feature that enables teachers to communicate directly with students from the teacher's computer. This real-time
messaging capability enhances communication within the learning environment, allowing teachers to provide immediate guidance and assistance.
With these functionalities, our system provides an effective and specialized solution for IT labs, offering teachers the tools they need to ensure a focused and productive learning environment for their students.

# How the client (student) and the server (teacher) communicate.
  
## Output

![Realtime system monitoring solution](https://github.com/rigvedmaanas/Realtime-System-Monitoring-Solution/assets/77579661/388a71db-1b7e-4d96-b037-31508b7cd8f9)

### Server (teacher) side
On the teacher's side, the system allows the teacher to view the screens of all connected students in real-time. It also includes a direct messaging capability, enabling teachers to communicate directly with students from their computer, thus facilitating immediate guidance and support. Additionally, the teacher has the capability to select individual student computers and access log files that provide a comprehensive record of all file system changes made by each respective student.
### Client (student) side
On the student's side, when the system is activated, the application operates silently in the background, without any noticeable changes in the system interface or performance. This discreet operation ensures that students can continue their work without disruptions.

# Scope of the project

## 1. Educational Settings:
Monitoring students' activity by teachers within computer labs or classrooms, promoting a focused learning environment.
## 2. Business Environments:
Allowing managers in companies or firms to effectively supervise and monitor their staff's activities using their own systems, enhancing productivity and ensuring adherence to work-related tasks.

## 3. Parental Control:
Empowering parents to monitor their children's computer activities at home, ensuring safe and responsible internet usage.

# Changes that could be made in the future

## 1. System Locking Functionality:
A valuable addition would be the ability for teachers to remotely lock student systems directly from the application, providing immediate control over student activities when necessary.
## 2. AI-Powered Activity Monitoring:
The implementation of artificial intelligence (AI) for real-time activity analysis, enabling the system to detect non-educational activities such as gaming, and automatically alerting the teacher for timely intervention and guidance.

# Conclusion
In its current form, the system showcased here operates on a local host, with both the client (student) and the server (teacher) running on the same system. However, it's important to note that the system's architecture is flexible and scalable. It has the potential to be expanded for implementation in scenarios where the server and client are separate systems or connected to different networks.

#### Me with my friend Devanandhan during the competition
![Me with my friend Devanandhan during the competition](https://github.com/rigvedmaanas/Realtime-System-Monitoring-Solution/assets/77579661/369b1e08-bced-4fe7-a0ff-1b5b7a94739f)


***

Note: This project was made for the Science Fair in Kerala and got A grade in Sub-district level (Aluva). The description given above is from the project report.

# How to run this program

## Dependencies

 - opencv-python~=4.8.0.76
 - numpy~=1.25.2
 - Pillow~=10.0.0
 - darkdetect~=0.8.0
 - customtkinter~=5.2.0
 - zfec~=1.5.7.2
 - setuptools~=65.5.1
 - mss~=9.0.1
 - watchdog~=3.0.0

## To install the required dependencies

```
pip3 install -r requirement.txt
```

## Change the IP in `main.py` `client.py`
## Run `main.py` in the teacher's computer
## Run `client.py` in the student's computer
