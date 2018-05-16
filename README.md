# ABE_Experiments
## Procedure to install psychopy software on lab computers:
1. Uninstall all instances of Python or Psychopy
2. Download and install latest Psychopy version
3. Run `python --version` to make sure you're on python 2.7
4. Run `git clone https://github.coecis.cornell.edu/sd549/ABE_Experiments.git` in experiment directory
5. Run `python -m pip install image-slicer` (make sure this is done with admin priviliges)
6. Setup Complete! You can run the experiment from the terminal.

## Running the online experiment locally:

1. Before you run [experiment.html](experiment.html), make sure you have XAMPP which you can download from [here](https://www.apachefriends.org/download.html).
2. Once you have XAMPP installed, transfer the following items to the htdocs folder located in the XAMPP installation folder:
    - jsdataframe folder
    - jspsych folder
    - Stimuli folder
    - experiment.html
    - insert_ip.php
    - write_data.php
    - get_subject_id.php
    - finished_exp.php
    - mysql_commands.sql
3. Now you need to create the MySQL tables necessary for base functionality. Open up XAMPP and click on shell.
4. In the shell run the command `mysql -u root -p` and press enter when prompted for password
5. Run `create database ABE`
6. Run `use test;` in the terminal
7. Run `source mysql_commands.sql` in the terminal
8. You should be all set to open [experiment.html](experiment.html) in a new browser window (go to localhost/experiment.html)

### Notes:
1. You can only run the experiment.html once before it records your ip address and prevents you from running it again. To run the experiment again you need to run the following commands in mysql shell:
    - `delete from ipaddr;`
    - `delete from finishedexp;`
2. The subject ids are read from a mysql table and are sampled without replacement. Every so often you need to add more subject ids to the table or else the experiment will say that no more participants are being accepted. Run the following command to add more subject ids.
    - `insert into subjectsavail (subject) values (5), (8), (9);`
    
5, 8, and 9 can be replaced with any other subject ids and you can add more than three at a time.