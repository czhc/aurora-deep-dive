#
Accelerate Database Development and Testing with Amazon Aurora

#

# Lab Guide

PART 1. Setup Environment        2

Task 1.1 – Sign in to Management Console, Select Region and Create Key Pair        2

Task 1.2 - Creating a Stack using CloudFormation        4

Task 1.3 - Connecting to the workstation EC2 instance        8

Task 1.4 – Set up the AWS CLI and seed the DB Cluster        8

PART 2. Cluster Endpoints and Auto Scaling        9

Task 2.1 – Running a read-only workload        9

PART 3. Cloning and backtracking databases        11

Task 3.1 - Creating a Clone        11

Task 3.2 - Backtracking the Database        14

PART 4. Performance Insights        15

Task 4.1 – Generate Load on Your Database Cluster        15

APPENDIX        17

Appendix 1 – Setting up PuTTY and connecting via SSH        17



# PART 1. Setup Environment

Please log into the AWS Management Console using the credentials provided to you on the separate card.

You will be using the **Ohio (US-EAST-2)** region.

In this part of the lab you will leverage AWS CloudFormation to provision an Aurora MySQL 5.6 compatible database cluster, along with a Linux EC2 instance to be used as a workstation. You will connect to the workstation using SSH.

The environment deployed using CloudFormation includes several components, as listed below. Please download the CloudFormation template (instructions below) and review it for more details.

1. Amazon VPC network configuration with public and private subnets
2. Database subnet group and relevant security groups for the cluster and workstation
3. Amazon EC2 instance configured with the software components needed for the lab
4. Roles with access permissions for the workstation and cluster permissions for enhanced monitoring, S3 access and logging
5. Custom cluster and DB instance parameter groups for the Amazon Aurora cluster, enabling logging and performance schema
6. Amazon Aurora DB cluster with 2 nodes: a writer and read replica
7. Read replica auto scaling configuration
8. AWS Systems Manager command document to execute a load test

## Task 1.1 – Sign in to Management Console, Select Region and Create Key Pair

1. Login to your AWS Isengard console and ensure you select **Ohio (US-EAST-2)**region before you start.
2. Enter the **Username** and **Password** from the credentials card, click **Sign In**.

1. Ensure the **Ohio (us-east-2)** region is selected in the top right corner, if not use that dropdown to choose the correct region

1. Open the **Key Pairs** section of the EC2 service console, using this short link: https://amzn.to/2XAeOqL.
2. Ensure you are still in the correct region, and click **Create Key Pair**.



1. Name the key pair &quot;dblabkeys&quot; and then click **Create** and download the file named **dblabkeys.pem** to your computer, save it in a memorable location like your desktop.  You will need this file later in the lab.



## Task 1.2 - Creating a Stack using CloudFormation

1. Download the CloudFormation template named **lab\_template.yml** from [http://bit.ly/aurora-dblab-template](http://bit.ly/aurora-dblab-template). Save it in a memorable location such as your desktop, you will need to reference it.
2. Open the **CloudFormation** service console located at: [https://amzn.to/2Lfqa1F](https://amzn.to/2Lfqa1F) and

Click **Create Stack.**

**Notice:** The CloudFormation console has been upgraded recently. Depending on your previous usage of the CloudFormation console UI, you may see the old design or the new design, you may also be presented with a prompt to toggle between them. In this lab we are using the **new design** for reference, although the steps will work similarly in the old console design as well, if you are more familiar with it.



1. Select the radio button named **Upload a template** , then **Choose file** and select the template file you downloaded previously named **lab\_template.yml** and then click **Next**.

1. In the field named **Stack Name** , enter the value &quot;dblabstack&quot;, select the **ec2KeyPair** value as &quot;dblabkeys&quot; (the key pair you have created previously).

Select all 3 AZs available in the drop down available for the &quot; **vpcAZs**&quot; field

and then click **Next**.



1. On the **Configure stack options** page, leave the defaults as they are, scroll to the bottom and click **Next**.

1. On the **Review dblabstack** page, scroll to the bottom, check the box that reads: **I acknowledge that AWS CloudFormation might create IAM resources with custom names** and then click **Create**.



1. The stack will take approximatively 20 minutes to provision, you can monitor the status on the **Stack detail** page. You can monitor the progress of the stack creation process by refreshing the **Events** tab. The latest event in the list will indicate **CREATE\_COMPLETE** for the **dblabstack** resource.

In the meantime we will discuss some important considerations when architecting and automating the deployment of Aurora clusters.

1. Once the status of the stack is **CREATE\_COMPLETE** , click on the **Outputs** tab. The values here will be critical to the completion of the remainder of the lab.   **Please take a moment to save these values somewhere that you will have easy access to them during the remainder of the lab.** The names that appear in the **Key** column are referenced directly in the instructions in subsequent steps, using the parameter format: **[outputKey]**

## Task 1.3 - Connecting to the workstation EC2 instance

**For Windows users:** We will use PuTTY and PuTTY Key Generator to connect to the workstation using SSH. If you do not have these applications already installed please use the steps in **Appendix 1 - Setting up PuTTY and connecting via SSH** below.

**For macOS or Linux users:** You can connect using the following command from a terminal, however you will need to change the permissions of the certificate file first:

**chmod**  **0600** **[path to downloaded .pem file]**

**ssh -i** **[path to downloaded .pem file]**  **ubuntu@**** [bastionEndpoint]**

## Task 1.4 – Set up the AWS CLI and seed the DB Cluster

1. Enter the following command in the SSH console to configure the AWS CLI:

**aws configure**

Then select the defaults for everything except the default region name.  For the default region name, enter &quot;us-east-2&quot;.

Ignore the region listed in the screen shot below. The correct region to chose is

&quot;us-east-2&quot;

1. Connect to the Aurora database using the following command:

**mysql -h** **[clusterEndpoint]**  **-u masteruser -p mylab**

Unless otherwise specified the cluster master username is **masteruser** and the password is **Password1**

1. Run the following queries on the database server, they will create a table, and load data from S3 into it:





**DROP TABLE IF EXISTS `sbtest1`;**

**CREATE TABLE `sbtest1` (
 `id` int(10) unsigned NOT NULL AUTO\_INCREMENT,
 `k` int(10) unsigned NOT NULL DEFAULT &#39;0&#39;,
 `c` char(120) NOT NULL DEFAULT &#39;&#39;,
 `pad` char(60) NOT NULL DEFAULT &#39;&#39;,
PRIMARY KEY (`id`),
KEY `k_1` (`k`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;**

**LOAD DATA FROM S3 MANIFEST
&#39;s3-us-west-2://auroraworkshopassets/data/sbtable/sample.manifest&#39;
REPLACE
INTO TABLE sbtest1
CHARACTER SET &#39;latin1&#39;
FIELDS TERMINATED BY &#39;,&#39;
LINES TERMINATED BY &#39;\r\n&#39;;**

# PART 2. Cluster Endpoints and Auto Scaling

In this part we will explore the cluster endpoints and how auto scaling of read replicas operates.

## Task 2.1 – Running a read-only workload

1. On the bastion host, execute the following statement:

**python loadtest.py** **[readerEndpoint]**

1. Open the **Amazon RDS** service console located at: [https://amzn.to/2GNcMPk](https://amzn.to/2GNcMPk).
2. Take note that the reader node is currently receiving load. It may take a minute or more for the metrics to fully reflect the incoming load.



1. After a few minutes return to the list of instances and notice that a new reader is being provisioned to your cluster.

1. Once the replicas are added, note that the they are starting to receive load.

1. You can now type CTRL+C on the bastion host to end the read load, if you wish to. After a while the additional readers will be removed automatically.

# PART 3. Cloning and backtracking databases

## Please have the outputs section from the Cloudformation run handy before you start. You will be required to substitute values in the steps below

## Task 3.1 - Creating a Clone

1. On the bastion host, enter:

**aws rds restore-db-cluster-to-point-in-time --restore-type copy-on-write --use-latest-restorable-time --source-db-cluster-identifier** **[clusterName]**  **--db-cluster-identifier** **[clusterName]****-clone --vpc-security-group-ids **** [dbSecurityGroup] **** --db-subnet-group-name **** [dbSubnetGroup] **** --backtrack-window 86400**

The –restore-type copy-on-write is how the restore-db-cluster method is used to create a DB clone.

1. Next, to check the status of the creation of your clone, enter the following command on the bastion host. The cloning process can take several minutes to complete. See the example output below.

**Note:** This step will create the Aurora DB cluster itself, but without any compute nodes. You will add a computer node in the next step.

**aws rds describe-db-clusters --db-cluster-identifier** **[clusterName]****-clone**

1. Take note of both the **&quot;Status&quot;** and the **&quot;Endpoint.&quot;**  Once the **Status** becomes **available** , you can add an instance to the cluster and once the instance is added, you will want to connect to the cluster via the **Endpoint** value.  To add an instance to the cluster once the status becomes **available** , enter the following:

**aws rds create-db-instance --db-instance-class db.r4.large --engine aurora --db-cluster-identifier** **[clusterName]****-clone --db-instance-identifier **** [clusterName] ****-clone-instance**

1. To check the creation of the instance, enter the following at the command line:

**aws rds describe-db-instances --db-instance-identifier** **[clusterName]****-clone-instance**

1. Once the **DBInstanceStatus** changes from **creating** to **available** , you have a functioning clone. Creating a node in a cluster also takes several minutes.

1. Once your instance is created, connect to the instance using the following command:

**mysql -h** **[cluster endpoint of clone cluster]**  **-u masteruser -p mylab**

**Note:** the master user account credentials will be the same as with the source of the cloned cluster. If you customized the CloudFormation template and changed the values, use the customized username and password.

1. In order to verify that the clone is identical to the source, we will perform a checksum of the sbtest1 table using the following:

**checksum table sbtest1;**

1. The output of your commands should look similar to the example below:

1. Please take note of the value for your specific clone cluster.

1. Next, we will disconnect from the clone and connect to the original cluster with the following:

**quit;**

**mysql –h** **[clusterEndpoint]**  **-u masteruser -p mylab**

1. Next, we will execute the same commands that we executed on the clone:

**checksum table sbtest1;**

1. Please take note of the value for your specific source cluster. The checksum should be identical.



## Task 3.2 - Backtracking the Database

1. Reconnect to the cloned cluster using:

**quit;**

**mysql –h** **[cluster endpoint of clone cluster]**  **-u masteruser -p mylab**

1. Drop the **sbtest1** table:

**Note:** Consider executing the commands below one at a time, waiting a few seconds between each one. This will make it easier to determine a good point in time for testing backtrack.

**select current\_timestamp();**

**drop table sbtest1;**

**select current\_timestamp();**

**quit;**

1. Remember or save the time markers displayed above, you will use them as references later.
2. Run the following command to replace the dropped table using the sysbench command:

**sysbench oltp\_write\_only --threads=1 --mysql-host=**** [cluster endpoint of clone cluster] **** --mysql-user=masteruser --mysql-password=Password1 --mysql-port=3306 --tables=1 --mysql-db=mylab --table-size=1000000 prepare**

1. Reconnect to the cloned cluster, and checksum the table again, the checksum value should be different than both the original clone value and source cluster:

**mysql –h** **[cluster endpoint of clone cluster]**  **-u masteruser -p mylab**

**checksum table sbtest1;**

**quit;**

1. Backtrack the database to a time slightly after the second time marker. (Right after dropping the table).

**aws rds backtrack-db-cluster --db-cluster-identifier** **[clusterName]****-clone --backtrack-to ****&quot;yyyy-mm-ddThh:mm:ssZ&quot;**

1. Run the below command to track the progress of the backtracking operation. The operation should complete in a few minutes.

**aws rds describe-db-clusters --db-cluster-identifier** **[clusterName]****-clone | grep -i EngineMode -A 2 | grep Status**

1. Connect back to the database. The **sbtest1** table should be missing from the database.

**mysql –h** **[cluster endpoint of clone cluster]**  **-u masteruser -p mylab**

**show tables;**

**quit;**

1. Now backtrack again to a time slightly before the first time marker above. (Right before dropping the table).

**aws rds backtrack-db-cluster --db-cluster-identifier** **[clusterName]****-clone --backtrack-to ****&quot;yyyy-mm-ddThh:mm:ssZ&quot;**

1. Run the below command to track the progress of the backtracking operation. The operation should complete in a few minutes.

**aws rds describe-db-clusters --db-cluster-identifier** **[clusterName]****-clone | grep -i EngineMode -A 2 | grep Status**

1. Connect back to the database. The **sbtest1** table should now be available in the database again, but contain the original data set.

**mysql –h** **[cluster endpoint of clone cluster]**  **-u masteruser -p mylab**

**show tables;**

**quit;**

# PART 4. Performance Insights

## Task 4.1 – Generate Load on Your Database Cluster

1. You will use [Percona&#39;s TPCC-like benchmark script](https://github.com/Percona-Lab/sysbench-tpcc) based on sysbench to generate load. For simplicity we have packaged the correct set of commands in an AWS Systems Manager Command Document. You will use AWS Systems Manager Run Command to execute the test.
2. On the workstation host, execute the following statement:

**aws ssm send-command --document-name** **[loadTestRunDoc]**  **--instance-ids** **[bastionInstance]**

1. The command will be sent to the workstation EC2 instance which will prepare the test data set and run the load test. It may take up to a minute for CloudWatch to reflect the additional load in the metrics.

1. Navigate to the RDS service console ([https://amzn.to/2GNcMPk](https://amzn.to/2GNcMPk)) and click on **Performance Insights** in the left side navigation bar.

1. Examine the performance of your DB instance **demostack-node-01** using Performance Insights. What conclusions can you reach?





# Part 5. Working with Aurora Serverless

## Task 5.1 Run CloudFormation Stack to create Cloud 9 IDE

S3 URL for Cloud Formation Template :

[https://aws-quickstart.s3.amazonaws.com/quickstart-cloud9-ide/templates/cloud9-ide-instance.yaml](https://aws-quickstart.s3.amazonaws.com/quickstart-cloud9-ide/templates/cloud9-ide-instance.yaml)

You will need to have public subnet id from the previous cloudformation template outputs section handy for this step.

[https://us-east-2.console.aws.amazon.com/cloudformation/home?region=us-east-2 - /stacks/create/template?stackName=AWS-Cloud9-IDE&amp;templateURL=https://aws-quickstart.s3.amazonaws.com/quickstart-cloud9-ide/templates/cloud9-ide-instance.yaml](https://us-east-2.console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/create/template?stackName=AWS-Cloud9-IDE&amp;templateURL=https://aws-quickstart.s3.amazonaws.com/quickstart-cloud9-ide/templates/cloud9-ide-instance.yaml)



1. Go to the RDS Console click on the &quot;Create Database&quot; orange icon.

1. In the next screen, please ensure that &quot;easy create&quot; is set to off, choose &quot;Amazon Aurora&quot; as Engine Options, and the Edition is &quot;Amazon Aurora with MySQL compatibility&quot;





1. In the Capacity type section choose &quot;Serverless&quot;



1. In the &quot;Settings&quot; section, give &quot;serverless&quot; as the cluster identifier, in &quot;Credentials Settings&quot;, leave &quot;admin&quot; as the username and choose a password that you can remember.



1. Leave the next sections as default and click on the create database button to create the database.



1. Once the Database cluster is created,

We need to modify the instance for the purposes of enabling Data API for the given serverless instance.

Select the database in the RDS console and click on &quot;Modify&quot;



7.On the next screen in the &quot;Network and Security&quot;  section select the checkbox for &quot;Data API&quot; to enable it



1. Select &quot;Apply Immediately&quot; and click on &quot;Modify Cluster&quot; on the next screen.

1. Next, we need to create a database and a table in the serverless database.

You can do this using the Query Editor on the console or any mysql client . Note the Query editor is currently

only available for Aurora Serverless MYSQL

Navigate to the RDS Console and click on the Query Editor option on the left pane.

On the following screen please select the following for the fields.

1. Select the database name from the dropdown ( in this case serverless)
2. Skip the next Field below Database username (i.e Add new database credentials). This is used in the

 event you want to create new users for the DB.

1. Enter &quot;masterusername&quot; in the &quot;Enter Database username&quot; field.
2. Enter the password provided at the time of  db creation. Skip the next field

(&quot;Enter the name of the database or schema&quot;) as you want to create a

new DB and ciick on &quot;Connect to database&quot;.



1. Remove ` and comment and Copy paste the below contents on the &quot;Editor&quot; Section of the next screen.

**DROP DATABASE IF EXISTS employees;**

**CREATE DATABASE IF NOT EXISTS employees;**

**USE employees;**

**SELECT &#39;CREATING DATABASE STRUCTURE&#39; as &#39;INFO&#39;;**

**DROP TABLE IF EXISTS employees;**

**/\*!50503 set default\_storage\_engine = InnoDB \*/;**

**/\*!50503 select CONCAT(&#39;storage engine: &#39;, @@default\_storage\_engine) as INFO \*/;**

**CREATE TABLE employees (**

**    emp\_no      INT             NOT NULL,**

**    birth\_date  DATE            NOT NULL,**

**    first\_name  VARCHAR(14)     NOT NULL,**

**    last\_name   VARCHAR(16)     NOT NULL,**

**    gender      ENUM (&#39;M&#39;,&#39;F&#39;)  NOT NULL,**

**    hire\_date   DATE            NOT NULL,**

**    PRIMARY KEY (emp\_no)**

**);**

**SELECT &#39;LOADING employees&#39; as &#39;INFO&#39;;**

**INSERT INTO `employees` VALUES (10001,&#39;1953-09-02&#39;,&#39;Georgi&#39;,&#39;Facello&#39;,&#39;M&#39;,&#39;1986-06-26&#39;),**

**(10002,&#39;1964-06-02&#39;,&#39;Bezalel&#39;,&#39;Simmel&#39;,&#39;F&#39;,&#39;1985-11-21&#39;),**

**(10003,&#39;1959-12-03&#39;,&#39;Parto&#39;,&#39;Bamford&#39;,&#39;M&#39;,&#39;1986-08-28&#39;),**

**(10004,&#39;1954-05-01&#39;,&#39;Chirstian&#39;,&#39;Koblick&#39;,&#39;M&#39;,&#39;1986-12-01&#39;),**

**(10005,&#39;1955-01-21&#39;,&#39;Kyoichi&#39;,&#39;Maliniak&#39;,&#39;M&#39;,&#39;1989-09-12&#39;),**

**(10006,&#39;1953-04-20&#39;,&#39;Anneke&#39;,&#39;Preusig&#39;,&#39;F&#39;,&#39;1989-06-02&#39;),**

**(10007,&#39;1957-05-23&#39;,&#39;Tzvetan&#39;,&#39;Zielinski&#39;,&#39;F&#39;,&#39;1989-02-10&#39;);**



1. The output tab below the editor will auto refresh as each SQL is executed.

At the end of the last statement you should see the below SQL. Ensure status is reported as SUCCESS for all statements.



1. Create a Secrets to store the database credentials.
2. Go to the Secrets Manager Screen from the Services menu.
3. Click on the &quot;Store a new Secret&quot; button.



1. On the &quot;Select a Secret Type&quot; section, choose &quot;Credentials for RDS Database&quot;, provide the Username and Password that you provided when you created the database.

1. Choose the RDS Database that you created in the previous section and press the next button.
2. Give a friendly name and description and keep note of it, you will need it further down.



1. The next section is where you would create the &quot;Automatic Rotation Policy&quot; for this Lab we will leave those as default and press the &quot;Next Button&quot;

1. Review the details you have provided and click on &quot;Store&quot; to store the Key.
2. Navigate to the AWS Cloud 9 Service and click on &quot;Create Environment&quot;

1. Enter a name for the environment in the next screen, the description is optional.

1. In the following screen leave all the default values as is and proceed to the next step.



1. Review the settings and create your Environment. Once the environment is created your screen should look like this.

1. Click on the &quot;Create Lambda Function&quot; and enter Function Name in the next screen and click &quot;Next&quot;



1. Choose Python 3.6 on the Runtime and use the &quot;empty-python&quot; as the blueprint and click &quot;Next&quot;

1. Choose &quot;none&quot; for the Function Trigger and press Next

1. Leave the Memory and Role as default options



1. Your final screen should look something like the below

1. From the left side tree view, Click on serverless for drop down &amp; then double click the requirements.txt file to open it. Add the following lines at the end of the file.

1. Choose the Lambda\_function tab and copy the function downloaded from this URL - [https://pastebin.com/i2t3uaFr](https://pastebin.com/i2t3uaFr)
2. Replace the cluster\_arn and secrets\_arn variables from the previous steps.

(at lines 6 &amp; 7 )

1. Save the function.
2. In the bottom pane activate the virtual environment by using the command - source serverlessDB/venv/bin/activate



1. Change the directory to the &quot;serverlessDB&quot; and run the command, pip install -r requirements.txt –target .

1. This will collect all the required packages and install them in the serverlessDB folder.
2. Once this is completed, you can click on the Run button to test the function locally.

See the Tabs arranged horizontally on your right for this

        Select serverless with lambda icon and right click to run



1. Select Run Local

1. There is no Payload requirement and that can be left as default.

1. Once the function runs successfully, you will see response and function logs at the bottom pane.

1. You can deploy the function by right clicking on the local function and Deploying it.



1. Once the function is deployed you will be able to see it in the &quot;Remote Functions&quot; tree

1. At this time, you can run this from the Lambda Console and even connect an API to the Lambda function.
