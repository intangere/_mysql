# _mysql
Simple Lazy Mysql ORM
--
Usage:
```
mysql = Mysql() #Create Lazy Mysql Object
mysql.insert('username', 'test').query() #Insert into username field
mysql.where('username', 'test').update('password', 'test1234').query() #Where username=test, update password to test1234
#Let's see if it worked
sql = mysql.where('username', 'test).select('*').query()
print sql
```
