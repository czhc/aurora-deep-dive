
import boto3 

def lambda_handler(event, context):
    rdsData = boto3.client('rds-data')
    
    cluster_arn = '' 
    secret_arn = ''
     
    response1 = rdsData.execute_statement(
                resourceArn = cluster_arn, 
                secretArn = secret_arn, 
                database = 'employees', 
                sql = 'select max(emp_no)+1 from employees')
    
    nextVal = response1['records'][0][0]
    
    
    
    param0 = {'name':'empno', 'value':nextVal}
    param1 = {'name':'firstname', 'value':{'stringValue': 'JACKSON'}}
    param2 = {'name':'lastname', 'value':{'stringValue': 'MATEO'}}
    
    
    paramSet = [param0, param1, param2]

    tr = rdsData.begin_transaction(
         resourceArn = cluster_arn, 
         secretArn = secret_arn, 
         database = 'employees') 
         
    print (tr['transactionId'])
    
    response2 = rdsData.execute_statement(
            resourceArn = cluster_arn, 
            secretArn = secret_arn, 
            database = 'employees', 
            parameters = paramSet,
            sql = 'insert into employees(emp_no, birth_date, first_name, last_name, hire_date) VALUES(:empno, DATE_ADD(CURRENT_DATE(), INTERVAL -30 YEAR), :firstname, :lastname, current_date())')

    cr = rdsData.commit_transaction(
         resourceArn = cluster_arn, 
         secretArn = secret_arn, 
         transactionId = tr['transactionId']) 

    print  (cr['transactionStatus'] )

    return 0
