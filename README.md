python read_commit_log.py -h
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
