<p align="center">
  <img width="18%" align="center" src="https://github.com/Raph-Romeo/SAE-Piloter-un-projet-informatique/blob/main/client%20application/icons/taskmasterpro.png" alt="logo">
</p>
  <h1 align="center">
  Task Master Pro
</h1>
<p align="center">
  <b>Task Master Pro</b> is a desktop <b>task management</b> application designed for Windows (11 and 10). Built using Python, PyQt5 and QFluent-Widgets, it boasts a modern and intuitive user interface.
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
The docker-compose will redirect the server container's port on the host's port. Therefore, to communicate with the server, all you will need to do is put the host's ip address with the default port of **5240**.


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

There are three methods to run the application.
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

### Third method -- Conda Environment
Create the conda environment :
```bat
conda env create -f environment.yml
```
Activate the conda environment :
```bat
conda activate TaskMasterProCondaEnv
```
Run the client application :
```bat
python main.py
```

# Our team :
<pre><img align="center" style="height:35px;width:35px;border-radius:50%;" src="https://avatars.githubusercontent.com/u/95073137?s=100" <p><b> • Raph-Romeo </b></p> <a href="mailto:raphael.romeo@uha.fr">Raphael ROMEO</a><br></pre>
#
<pre><img align="center" style="height:35px;width:35px;border-radius:50%;" src="https://avatars.githubusercontent.com/u/92865322?s=100" <p><b> • Emir6868 </b></p><a href="mailto:emir.eraslan@uha.fr">Emir ERASLAN</a><br></pre>
#
<pre><img align="center" style="height:35px;width:35px;border-radius:50%;" src="https://avatars.githubusercontent.com/u/92865807?s=100" <p><b> • Elmirbtj </b></p><a href="mailto:elmir.batjari@uha.fr">Elmir BATJARI</a><br></pre>
#
<pre><img align="center" style="height:35px;width:35px;border-radius:50%;" src="https://avatars.githubusercontent.com/u/92864882?s=100" <p><b> • ZitoouN </b></p><a href="mailto:mehdi.rehm@uha.fr">Mehdi REHM</a><br></pre>
#
<pre><img align="center" style="height:35px;width:35px;border-radius:50%;" src="https://avatars.githubusercontent.com/u/92865842?s=100" <p><b> • LAMINE-Lamine </b></p><a href="mailto:elias.lamine@uha.fr">Elias LAMINE</a><br></pre>
#
<pre><img align="center" style="height:35px;width:35px;border-radius:50%;" src="https://avatars.githubusercontent.com/u/92827452?s=100" <p><b> • shpendrashiti </b></p><a href="mailto:shpend.rashiti@uha.fr">Shpend RASHITI</a><br></pre>
#
<pre><img align="center" style="height:35px;width:35px;border-radius:50%;" src="https://avatars.githubusercontent.com/u/92865016?s=100" <p><b> • JLKayser </b></p><a href="mailto:khalil.daoudi@uha.fr">Khalil DAOUDI</a><br></pre>

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
