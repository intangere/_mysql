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

#More advanced usage
mysql.where('username', 'test').update('email', 'test@test.com').update('age', '24').query()
#This can be rewritten as:
mysql.where('username', 'test').update(['email', 'age'], ['test@test.com', '24']).query()
#Select only certain values
sql = mysql.where('username', 'test).select(['email', 'age']).query()
mysql.insert('username', 'another_test').insert('password', 'password').query()
mysql.insert(['username','password'], ['another_test', 'pass123']).query()

#Lazy usage
mysql.where('username', 'username')
#Some event happens
mysql.update('event_field', event.value_here)
#Some other event
mysql.update('event_field_2', event_2.value_here)
mysql.query()
```
