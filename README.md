## **Description**
This is an application for organizing events for a wide variety of purposes.

___

## **Deploying the project**
1. ### Clone the repository to your local machine

    ```bash
    git clone git@github.com:Mernus/volsu_app.git
    ```

2. ### Install docker and docker-compose:

    - #### https://docs.docker.com/engine/install/
    - #### https://docs.docker.com/compose/install/
    ##### If you have Linux machine do not forget about the steps after installation:
    - #### https://docs.docker.com/engine/install/linux-postinstall/
    ##### If you have Mac or Windows machine you can also install Docker Desktop App:
    - #### https://docs.docker.com/desktop/
    
3. ### Install python:
   
   Project by default working with python version 3.9. You can use your own version, but there 
   might be some troubles with working capacity of project. So I highly recommend to use python version
   which is the default for the project.
   
4. ### Create virtual environment:
   
    ```bash
    virtualenv .pyenv --python=python3
    ```

5. ### Activate environment and install requirements:
   
   ##### On Windows:
      ```posh
      .pyenv\Scripts\activate.bat
      ```
   ##### On Linux:
      ```bash
      source .pyenv/bin/activate 
      ```
   ##### Requirements:
      ```bash
      pip install -U -r requirements.txt
      ```
___

## **TODO**

- ### Setting up a project
- ### Table of environment variables
