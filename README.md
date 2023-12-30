<p align="center">
  <img width="18%" align="center" src="https://github.com/Raph-Romeo/SAE-Piloter-un-projet-informatique/blob/main/client%20application/icons/taskmasterpro.png" alt="logo">
</p>
  <h1 align="center">
  Task Master Pro
</h1>
<p align="center">
  <b>Task Master Pro</b> is a cross-platform <b>task management</b> application designed for Windows (11 and 10). Built using Python and PyQt5, it boasts a modern and intuitive user interface.
</p>

<p align="center">
<b>Language</b> : English
</p>

### Application interface :
![Interface](https://lh3.googleusercontent.com/drive-viewer/AEYmBYSgEWbBtPvw1YL7Qo75fUsKezMTuiPpnrkmyxrbt4hUKMpLnCv-soKzpjy4rXclw5idyHf6X3yGLu3uHU7rlnizqamXNA=s1600)
### Optional Dark Mode :
![Interface](https://lh3.googleusercontent.com/drive-viewer/AEYmBYSChSCnwuRCFlXBqvDGDJvDlNO2_ZNAkx3N1Fk_1K0f1kUPkRXGuv_yZyKRm7pEMVuVRhjSyyJeYu2DxHCGOgxPNAgxyA=s1600)

## Features
- **User Accounts** : Create and manage user accounts with the option to add friends.
- **Task Creation** : Easily create tasks with detailed information, including a description, start date, deadline, and more.
- **Friend Collaboration** : Collaborate with friends by assigning tasks to them.
- **Calendar View** : A user-friendly calendar displays tasks for each day of the week, and each hour of the day.
- **Dynamic Status Updates** : Task status dynamically updates, marking tasks as "Completed," "Active" (once the start date is reached), or "Expired" (if the deadline passes without completion).

# Getting started.

## Server (Back end)
### ⚠️ All of the following actions are performed within the 📁 docker directory from this repository.

System requirements :
 - **Docker**
 - **git**
 - **Operating system** : Linux

**Start by cloning the git repository**
```bash
git clone https://github.com/Raph-Romeo/SAE-Piloter-un-projet-informatique
cd SAE-Piloter-un-projet-informatique/docker
```
**Give permission to the auto deploy docker script**
```bash
sudo chmod +x deploy.sh
```
**Run the deploy bash script**
```bash
./deploy.sh
```
The server should install itself and be up and running.

## Application (Front end)
```bat
git clone "https://github.com/Raph-Romeo/SAE-Piloter-un-projet-informatique"
```

### ⚠️ All of the following actions are performed within the 📁 client application directory from this repository.

System requirements :
 - **Python** : version 3.9 or greater
 - **git**
 - **Operating system** : Windows 10/11
 - **Storage** : 160Mb

There are two methods to run the application.
### First method using Python

```bat
pip install -r requirements.txt
```

Once all packages are installed you may run main.py

```bat
python main.py
```

Or alternatively, you may run the run.bat file.

### Second method -- Executable

Ensure that Python is accessible from your environment variable : **PATH**

Please run the **package.bat** file.
_This will create a virtual environment containing the application's essential modules (from requirements.txt) and then it will create an executable file to run the application. It will be created inside a folder called **packaged_application**_

You may then run the created executable located at **packaged_application/TaskMasterPro.exe**

# Our team :
 - **Raphael ROMEO** - 📧 raphael.romeo@uha.fr
 - **Emir ERASLAN** - 📧 emir.eraslan@uha.fr
 - **Elmir BATJARI** - 📧 elmir.batjari@uha.fr
 - **Elias LAMINE** - 📧 elias.lamine@uha.fr
 - **Khalil DAOUDI** - 📧 khalil.daoudi@uha.fr
 - **Mehdi REHM** - 📧 medhi.rehm@uha.fr
 - **Shpend RASHITI** - 📧 shpend.rashiti@uha.fr

### Backend : 
 - **Shpend RASHITI** (Backend developper and database) 
 - **Elias LAMINE** (Main backend developper)
 - **Mehdi REHM** (Auth + Account security development)

### Front-end :
 - **Emir ERASLAN** (Beta tester and bug fixer)
 - **Raphael ROMEO** (Concept designer and functionality developper)
 - **Khalil DAOUDI** (Application graphics + quality)
 - **Mehdi REHM** (Bug fixer and functionality developper)
 - **Elmir BATJARI** (Data handling developper)
### Deployment :
 - **Elmir BATJARI** ( Dockerfile + Dockercompose environment for backend service)
 - **Raphael ROMEO** ( Front-end app packaging into .exe)
