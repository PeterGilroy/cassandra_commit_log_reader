# A Cassandra commitlog reader created in python
This can be used to read the commitlogs created by Cassandra 3.11, 4.x and DSE 5.1, 6.8, 6.9.

This command was created with the help of the following article on the layout of the commitlogs:

https://cassandra.apache.org/_/blog/Learn-How-CommitLog-Works-in-Apache-Cassandra.html

and the Cassandra source code:

https://github.com/apache/cassandra/blob/cassandra-4.1/src/java/org/apache/cassandra/db/commitlog/CommitLogDescriptor.java

https://github.com/apache/cassandra/blob/cassandra-4.1/src/java/org/apache/cassandra/db/Mutation.java



## Command help:

```
$ python read_commit_log.py -h
usage: read_commit_log.py [-h] [-s | -f] [-t TABLE_FILE_NAME] [-u] file_path

positional arguments:
  file_path             Path to CommitLog file which you want to read

optional arguments:
  -h, --help            show this help message and exit
  -s, --summary         Gives a summary of the CommitLog. Just the header information and total number of mutations
  -f, --full            Full output. The output can be VERY large. Pipe to 'less' to more easily view output.
  -t TABLE_FILE_NAME, --table_file_name TABLE_FILE_NAME
                        Resolve the table ID to the table name. Provide a file name containing the keyspace, table and UUID of the table. Command
                        to do this is: cqlsh -e "copy system_schema.tables (keyspace_name,table_name,id) to 'tables.out' with header=false;"
  -u, --user            Only output non-system keyspace mutations and summary information.
```

## Example usage:
### Create an alias to the command:
```
$ alias clr='python ~/tools/cassandra_commit_log_reader/read_commit_log.py'
```
### Command with no options:
Take a copy of the commitlog that want to read and then run the command:
```
$ clr CommitLog-7-1739458796224.log
File name             : CommitLog-7-1739458796224.log
Version               : 7
ID                    : 1739458796224
Commit Log Parameters : 31613

SyncMarker - Mutation : 1 - 1
Table ID        : 7ad54392-bcdd-35a6-8417-4e047860b377
Keyspace Name   : system
Table Name      : local

SyncMarker - Mutation : 2 - 1
Table ID        : 7ad54392-bcdd-35a6-8417-4e047860b377
Keyspace Name   : system
Table Name      : local
...
SyncMarker - Mutation : 70 - 1
Table ID        : 5b2178e0-e9fe-11ef-a2ab-c7fec5dd3731
Keyspace Name   : unknownkeyspace
Table Name      : unknowntable

Total Count of Mutations : 1157
```
This will show the header information from the commmitlog. 
The 'File name' is from the command line but the 'Version' and 'ID' are extracted from the commitlog. 
The Version and ID should match these parts from the file name.

You will then see a summary of each mutation showing the sync marker and mutation number and then which table this is for. 
The default system table names are converted from the the table ID to the table name as these are consistent across all clusters.

Finally there will be a count of the number of mutations displayed.

**Note:** the output can be VERY verbose depending on the number of entries in the commitlog.
Pipe the output to `less` to have more control on the output.

### Command with table names resolved:
You can use the `-t` option to show the table names. 

To do this you need a file containing the keyspace name, table name and table ID.
This can be created using the following command:
```
$ cqlsh -e "copy system_schema.tables (keyspace_name,table_name,id) to 'tables.out' with header=false;"
```
Then reference this file in the command:
```
$ clr CommitLog-7-1739458796224.log -t tables.out
File name             : CommitLog-7-1739458796224.log
Version               : 7
ID                    : 1739458796224
Commit Log Parameters : 31613

SyncMarker - Mutation : 1 - 1
Table ID        : 7ad54392-bcdd-35a6-8417-4e047860b377
Keyspace Name   : system
Table Name      : local
...
SyncMarker - Mutation : 70 - 1
Table ID        : 5b2178e0-e9fe-11ef-a2ab-c7fec5dd3731
Keyspace Name   : peter
Table Name      : peter2

Total Count of Mutations : 1157
```

### Command with only user created tables:
You can use the `-u` option to limit the output to user created tables:
```
$ clr CommitLog-7-1739458796224.log -t tables.out -u
File name             : CommitLog-7-1739458796224.log
Version               : 7
ID                    : 1739458796224
Commit Log Parameters : 31613

SyncMarker - Mutation : 12 - 1
Table ID        : 5b2178e0-e9fe-11ef-a2ab-c7fec5dd3731
Keyspace Name   : peter
Table Name      : peter2

SyncMarker - Mutation : 40 - 1
Table ID        : 5b2178e0-e9fe-11ef-a2ab-c7fec5dd3731
Keyspace Name   : peter
Table Name      : peter2

SyncMarker - Mutation : 44 - 1
Table ID        : 5b2178e0-e9fe-11ef-a2ab-c7fec5dd3731
Keyspace Name   : peter
Table Name      : peter2

SyncMarker - Mutation : 63 - 1
Table ID        : 5b2178e0-e9fe-11ef-a2ab-c7fec5dd3731
Keyspace Name   : peter
Table Name      : peter2

SyncMarker - Mutation : 67 - 1
Table ID        : f7944250-e9f6-11ef-baf0-f120541aa681
Keyspace Name   : peter
Table Name      : peter1

SyncMarker - Mutation : 70 - 1
Table ID        : 5b2178e0-e9fe-11ef-a2ab-c7fec5dd3731
Keyspace Name   : peter
Table Name      : peter2

Total Count of Mutations : 6
```

### Command with summary information only:
Use the `-s` option to only show a summary.

With only user created tables:
```
$ clr CommitLog-7-1739458796224.log -t tables.out -u -s
File name             : CommitLog-7-1739458796224.log
Version               : 7
ID                    : 1739458796224
Commit Log Parameters : 31613

Total Count of Mutations : 6
```

Or with the full contents:
```
$ clr CommitLog-7-1739458796224.log -t tables.out -s
File name             : CommitLog-7-1739458796224.log
Version               : 7
ID                    : 1739458796224
Commit Log Parameters : 31613

Total Count of Mutations : 1157
```

### Command with mutation data:
Use the `-f` parameter to show the mutation data:
```
$ clr CommitLog-7-1739458796224.log -t tables.out -u -f
File name             : CommitLog-7-1739458796224.log
Version               : 7
ID                    : 1739458796224
Commit Log Parameters : 31613

SyncMarker - Mutation : 12 - 1
Mutation Size   : 61
Table ID        : 5b2178e0-e9fe-11ef-a2ab-c7fec5dd3731
Keyspace Name   : peter
Table Name      : peter2
Key             : b'\x00\x00\x00\x03'
Time Created ns : 2025-02-10 10:20:38
Time Created ns : 10fd0dbca608ae76
Mutation        : b'\x00\x02$\x00\tThree-One\x00$\x00\tThree-Two\x00'

SyncMarker - Mutation : 40 - 1
Mutation Size   : 48
Table ID        : 5b2178e0-e9fe-11ef-a2ab-c7fec5dd3731
Keyspace Name   : peter
Table Name      : peter2
Key             : b'\x00\x00\x00\x03'
Time Created ns : 2025-02-10 10:20:41
Time Created ns : 10fd0dbd6ea9bd97
Mutation        : b'\x00\x01$\x00\tThree-Two\x00'

SyncMarker - Mutation : 44 - 1
Mutation Size   : 41
Table ID        : 5b2178e0-e9fe-11ef-a2ab-c7fec5dd3731
Keyspace Name   : peter
Table Name      : peter2
Key             : b'\x00\x00\x00\x03'
Time Created ns : 2034-03-31 10:20:18
Time Created ns : 14fd0dbd8b4d7417
Mutation        : Deletion - b'\x00\x00\x00\x00'

SyncMarker - Mutation : 63 - 1
Mutation Size   : 48
Table ID        : 5b2178e0-e9fe-11ef-a2ab-c7fec5dd3731
Keyspace Name   : peter
Table Name      : peter2
Key             : b'\x00\x00\x00\x03'
Time Created ns : 2025-02-10 10:20:44
Time Created ns : 10fd0dbe11f3d745
Mutation        : b'\x00\x01$\x00\tThree-Two\x00'

SyncMarker - Mutation : 67 - 1
Mutation Size   : 46
Table ID        : f7944250-e9f6-11ef-baf0-f120541aa681
Keyspace Name   : peter
Table Name      : peter1
Key             : b'\x00\x00\x00\x04'
Time Created ns : 2025-02-10 10:20:44
Time Created ns : 10fd0dbe2e945f8b
Mutation        : {b'c2': b'\x04Four'}

SyncMarker - Mutation : 70 - 1
Mutation Size   : 48
Table ID        : 5b2178e0-e9fe-11ef-a2ab-c7fec5dd3731
Keyspace Name   : peter
Table Name      : peter2
Key             : b'\x00\x00\x00\x03'
Time Created ns : 2025-02-10 10:20:44
Time Created ns : 10fd0dbe31d6ccf2
Mutation        : b'\x00\x01$\x00\tThree-Two\x00'

Total Count of Mutations : 6
```
These are the mutations from the following cql statements:
```
cqlsh> begin batch insert into peter.peter2 (c1, c2) values (3, 'Three-Two'); insert into peter.peter2 (c1, c2) values (3, 'Three-One'); apply batch;
cqlsh> insert into peter.peter2 (c1, c2) values (3, 'Three-Two') ;
cqlsh> delete from peter.peter2 where c1 = 3;
cqlsh> insert into peter.peter2 (c1, c2) values (3, 'Three-Two') ;
cqlsh> insert into peter.peter1 (c1, c2) values (4, 'Four') ;
cqlsh> insert into peter.peter2 (c1, c2) values (3, 'Three-Two') ;

```
On the following tables:
```
create table peter.peter1 (c1 int primary key, c2 text) ;
create table peter.peter2 (c1 int, c2 text, primary key (c1,c2)) ;
```

## Limitations:
This only reads commitlogs that are not encrypted and not compressed.

Extra formatting is only performed on mutations on simple tables without a clustering column.
