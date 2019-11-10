

# Part 5. Working with Aurora Serverless

## Task 5.1 Run CloudFormation Stack to create Cloud 9 IDE

S3 URL for Cloud Formation Template :

[https://aws-quickstart.s3.amazonaws.com/quickstart-cloud9-ide/templates/cloud9-ide-instance.yaml](https://aws-quickstart.s3.amazonaws.com/quickstart-cloud9-ide/templates/cloud9-ide-instance.yaml)

You will need to have public subnet id from the previous cloudformation template outputs section handy for this step.

[https://us-east-2.console.aws.amazon.com/cloudformation/home?region=us-east-2 - /stacks/create/template?stackName=AWS-Cloud9-IDE&amp;templateURL=https://aws-quickstart.s3.amazonaws.com/quickstart-cloud9-ide/templates/cloud9-ide-instance.yaml](https://us-east-2.console.aws.amazon.com/cloudformation/home?region=us-east-2#/stacks/create/template?stackName=AWS-Cloud9-IDE&amp;templateURL=https://aws-quickstart.s3.amazonaws.com/quickstart-cloud9-ide/templates/cloud9-ide-instance.yaml)



1. Go to the RDS Console click on the &quot;Create Database&quot; orange icon.

[image21](./img/image021.png)


1. In the next screen, please ensure that &quot;easy create&quot; is set to off, choose &quot;Amazon Aurora&quot; as Engine Options, and the Edition is &quot;Amazon Aurora with MySQL compatibility&quot;

[image22](./img/image022.png)


1. In the Capacity type section choose &quot;Serverless&quot;

[image23](./img/image023.png)


1. In the &quot;Settings&quot; section, give &quot;serverless&quot; as the cluster identifier, in &quot;Credentials Settings&quot;, leave &quot;admin&quot; as the username and choose a password that you can remember.

[image24](./img/image024.png)


1. Leave the next sections as default and click on the create database button to create the database.

[image25](./img/image025.png)


1. Once the Database cluster is created,

We need to modify the instance for the purposes of enabling Data API for the given serverless instance.

Select the database in the RDS console and click on &quot;Modify&quot;

[image26](./img/image026.png)


7.On the next screen in the &quot;Network and Security&quot;  section select the checkbox for &quot;Data API&quot; to enable it

[image27](./img/image027.png)


1. Select &quot;Apply Immediately&quot; and click on &quot;Modify Cluster&quot; on the next screen.

[image28](./img/image028.png)

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

[image29](./img/image029.png)



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

[image30](./img/image030.png)


1. Create a Secrets to store the database credentials.
2. Go to the Secrets Manager Screen from the Services menu.
3. Click on the &quot;Store a new Secret&quot; button.

[image31](./img/image031.png)


1. On the &quot;Select a Secret Type&quot; section, choose &quot;Credentials for RDS Database&quot;, provide the Username and Password that you provided when you created the database.

[image32](./img/image032.png)

1. Choose the RDS Database that you created in the previous section and press the next button.
2. Give a friendly name and description and keep note of it, you will need it further down.

[image33](./img/image033.png)


1. The next section is where you would create the &quot;Automatic Rotation Policy&quot; for this Lab we will leave those as default and press the &quot;Next Button&quot;

[image34](./img/image034.png)


1. Review the details you have provided and click on &quot;Store&quot; to store the Key.
2. Navigate to the AWS Cloud 9 Service and click on &quot;Create Environment&quot;

[image35](./img/image035.png)


1. Enter a name for the environment in the next screen, the description is optional.

[image36](./img/image036.png)


1. In the following screen leave all the default values as is and proceed to the next step.

[image37](./img/image037.png)


1. Review the settings and create your Environment. Once the environment is created your screen should look like this.

[image38](./img/image038.png)


1. Click on the &quot;Create Lambda Function&quot; and enter Function Name in the next screen and click &quot;Next&quot;

[image39](./img/image039.png)


1. Choose Python 3.6 on the Runtime and use the &quot;empty-python&quot; as the blueprint and click &quot;Next&quot;

[image40](./img/image040.png)


1. Choose &quot;none&quot; for the Function Trigger and press Next

[image41](./img/image041.png)


1. Leave the Memory and Role as default options

[image42](./img/image042.png)


1. Your final screen should look something like the below

[image43](./img/image043.png)


1. From the left side tree view, Click on serverless for drop down &amp; then double click the requirements.txt file to open it. Add the following lines at the end of the file.

```
awscli=1.16.193
```

1. Choose the Lambda\_function tab and copy the function downloaded from this URL - [https://pastebin.com/i2t3uaFr](https://pastebin.com/i2t3uaFr)
2. Replace the cluster\_arn and secrets\_arn variables from the previous steps.

(at lines 6 &amp; 7 )

1. Save the function.
2. In the bottom pane activate the virtual environment by using the command - source serverlessDB/venv/bin/activate

[image45](./img/image045.png)


1. Change the directory to the &quot;serverlessDB&quot; and run the command, pip install -r requirements.txt –target .

[image46](./img/image046.png)


1. This will collect all the required packages and install them in the serverlessDB folder.
2. Once this is completed, you can click on the Run button to test the function locally.

See the Tabs arranged horizontally on your right for this

        Select serverless with lambda icon and right click to run

[image46](./img/image046.png)


1. Select Run Local

[image47](./img/image047.png)


1. There is no Payload requirement and that can be left as default.

[image48](./img/image048.png)


1. Once the function runs successfully, you will see response and function logs at the bottom pane.

1. You can deploy the function by right clicking on the local function and Deploying it.

[image49](./img/image049.png)


1. Once the function is deployed you will be able to see it in the &quot;Remote Functions&quot; tree

[image50](./img/image050.png)


1. At this time, you can run this from the Lambda Console and even connect an API to the Lambda function.
