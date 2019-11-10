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
