import struct
import binascii
#import sys
import argparse
import os.path
import datetime
#import json

# Set the list of default system tables that have the same uuid
def set_system_tables():
    system_tables_data = [['system_auth', 'cidr_groups', '9c48af00-13f6-3059-bb0e-8fcabba6eecb'],
                          ['system_auth', 'cidr_permissions', 'b8b43d5f-d6c0-331c-8f7d-765ea658f4c4'],
                          ['system_auth', 'identity_to_role', '0bd47a48-d6ba-3c8e-b442-0f6349329bda'],
                          ['system_auth', 'network_permissions', 'd46780c2-2f1c-3db9-b4c1-b8d9fbc0cc23'],
                          ['system_auth', 'resource_role_permissons_index', '5f2fbdad-91f1-3946-bd25-d5da3a5c35ec'], 
                          ['system_auth', 'role_members', '0ecdaa87-f8fb-3e60-88d1-74fb36fe5c0d'], 
                          ['system_auth', 'role_permissions', '3afbe79f-2194-31a7-add7-f5ab90d8ec9c'], 
                          ['system_auth', 'roles', '5bc52802-de25-35ed-aeab-188eecebb090'], 
                          ['system_schema', 'aggregates', '924c5587-2e3a-345b-b10c-12f37c1ba895'],
                          ['system_schema', 'column_masks', '738cc5ed-0168-3268-b9d1-853d4bc278af'],
                          ['system_schema', 'columns', '24101c25-a2ae-3af7-87c1-b40ee1aca33f'], 
                          ['system_schema', 'dropped_columns', '5e7583b5-f3f4-3af1-9a39-b7e1d6f5f11f'], 
                          ['system_schema', 'functions', '96489b79-80be-3e14-a701-66a0b9159450'], 
                          ['system_schema', 'indexes', '0feb57ac-311f-382f-ba6d-9024d305702f'], 
                          ['system_schema', 'keyspaces', 'abac5682-dea6-31c5-b535-b3d6cffd0fb6'], 
                          ['system_schema', 'tables', 'afddfb9d-bc1e-3068-8056-eed6c302ba09'], 
                          ['system_schema', 'triggers', '4df70b66-6b05-3251-95a1-32b54005fd48'], 
                          ['system_schema', 'types', '5a8b1ca8-6602-3f77-a045-9273d308917a'], 
                          ['system_schema', 'views', '9786ac1c-dd58-3201-a7cd-ad556410c985'], 
                          ['system_distributed', 'parent_repair_history', 'deabd734-b99d-3b9c-92e5-fd92eb5abf14'], 
                          ['system_distributed', 'partition_denylist', 'd6123acc-8649-3496-9d4e-f3fe39a6018b'], 
                          ['system_distributed', 'repair_history', '759fffad-624b-3181-80ee-fa9a52d1f627'], 
                          ['system_distributed', 'view_build_status', '5582b59f-8e4e-35e1-b913-3acada51eb04'],
                          ['system_distributed', 'nodesync_status', 'c0e1b5f4-c731-3317-a5a2-2587bbef62f8'], 
                          ['system', 'IndexInfo', '9f5c6374-d485-3229-9a0a-5094af9ad1e3'], 
                          ['system', 'available_ranges', 'c539fcab-d65a-31d1-8133-d25605643ee3'], 
                          ['system', 'available_ranges_v2', '4224a088-2ac9-3d0c-889d-fbb5f0facda0'], 
                          ['system', 'batches', '919a4bc5-7a33-3573-b03e-13fc3f68b465'], 
                          ['system', 'built_views', '4b3c50a9-ea87-3d76-9101-6dbc9c38494a'], 
                          ['system', 'compaction_history', 'b4dbb7b4-dc49-3fb5-b3bf-ce6e434832ca'], 
                          ['system', 'local', '7ad54392-bcdd-35a6-8417-4e047860b377'], 
                          ['system', 'paxos', 'b7b7f0c2-fd0a-3410-8c05-3ef614bb7c2d'], 
                          ['system', 'paxos_repair_history', 'ecb86667-40b2-3316-bb91-e612c8047457'], 
                          ['system', 'peer_events', '59dfeaea-8db2-3341-91ef-109974d81484'], 
                          ['system', 'peer_events_v2', '0e65065f-e401-38ed-9507-b9213fae8d11'], 
                          ['system', 'peers', '37f71aca-7dc2-383b-a706-72528af04d4f'], 
                          ['system', 'peers_v2', 'c4325fbb-8e5e-3baf-bd07-0f9250ed818e'], 
                          ['system', 'prepared_statements', '18a9c257-6a0c-3841-ba71-8cd529849fef'], 
                          ['system', 'repairs', 'a3d277d1-cfaf-36f5-a2a7-38d5eea9ad6a'], 
                          ['system', 'size_estimates', '618f817b-005f-3678-b8a4-53f3930b8e86'], 
                          ['system', 'sstable_activity', '5a1ff267-ace0-3f12-8563-cfae6103c65e'], 
                          ['system', 'sstable_activity_v2', '62efe31f-3be8-310c-8d29-8963439c1288'], 
                          ['system', 'table_estimates', '176c39cd-b93d-33a5-a218-8eb06a56f66e'], 
                          ['system', 'top_partitions', '7e5a361c-317c-351f-b15f-ffd8afd3dd4b'], 
                          ['system', 'transferred_ranges', '6cad20f7-d4f5-3af2-b6e2-0da33c6c1f83'], 
                          ['system', 'transferred_ranges_v2', '1ff78f1a-7df1-3a2a-a998-6f4932270af5'], 
                          ['system', 'view_builds_in_progress', '6c22df66-c3bd-3df6-b74d-21179c6a9fe9'],
                          ['system', 'nodesync_checkpoints', '2459e663-3235-3e9d-b072-add3d46ca545'], 
                          ['system_traces', 'events', '8826e8e9-e16a-3728-8753-3bc1fc713c25'], 
                          ['system_traces', 'sessions', 'c5e99f16-8677-3914-b17e-960613512345'],
                          ['dse_perf','cell_count_histograms','f8babf46-788b-3e1c-984d-6c62dedf354c'],
                          ['dse_perf','cell_count_histograms_summary','38083a4c-14e1-3bf2-acfe-b6d473fb03c6'],
                          ['dse_perf','dropped_messages','624fd93a-a7eb-3b8f-838f-7658b25a9ab2'],
                          ['dse_perf','graph_event_log','71aadc7f-1208-33f5-9706-d791d8ff5691'],
                          ['dse_perf','node_slow_log','75a7d794-06d0-3286-9bfa-84d92cabaebc'],
                          ['dse_perf','partition_size_histograms','80c91efa-d1d0-3f74-bb2c-f802742b4808'],
                          ['dse_perf','partition_size_histograms_summary','7b1cb180-44b0-3dc6-82d8-7f77da833e61'],
                          ['dse_perf','range_latency_histograms','92cda678-46ce-366f-9af5-af9ec805c0b6'],
                          ['dse_perf','range_latency_histograms_global','ec4f7f83-6cfc-3061-894f-745e81aae120'],
                          ['dse_perf','range_latency_histograms_ks','3599b53e-2413-3dec-b876-262e685e815a'],
                          ['dse_perf','range_latency_histograms_summary','d855eec9-49a8-323a-b900-108a3f1fd798'],
                          ['dse_perf','read_latency_histograms','4d79fdae-c4f5-3aac-8dd7-622f6ce44c73'],
                          ['dse_perf','read_latency_histograms_global','852314ef-2d74-3549-beef-0b4b4d3dc489'],
                          ['dse_perf','read_latency_histograms_ks','727ab411-96fe-3db1-b7c1-1f7f39c6e7b3'],
                          ['dse_perf','read_latency_histograms_summary','352211d1-fb91-304d-94a1-da70bfe2a3ed'],
                          ['dse_perf','schema_migration_log','a39d81e1-f6a2-38e6-bd57-68f6f0bc4170'],
                          ['dse_perf','slow_transaction_log','65a75ae6-ca23-3bc9-8cdc-4e92a80d7059'],
                          ['dse_perf','solr_slow_sub_query_log','5fe071b8-1162-3060-9967-3b7ac36a3683'],
                          ['dse_perf','sstables_per_read_histograms','0375e5d3-63b2-3d8d-9e3c-d99e43f5a4e5'],
                          ['dse_perf','sstables_per_read_histograms_ks','e798162f-e0dc-302b-8c76-bb483b1c4564'],
                          ['dse_perf','sstables_per_read_histograms_summary','d75da3fa-95b9-36ae-a53b-1db9912db5e7'],
                          ['dse_perf','write_latency_histograms','46186ea8-6885-3afe-9d25-71f7f72a0362'],
                          ['dse_perf','write_latency_histograms_global','3dd21557-266c-3265-8255-d45f89d12e5e'],
                          ['dse_perf','write_latency_histograms_ks','9b2c3f3c-f32e-35bb-a732-8776f8943f40'],
                          ['dse_perf','write_latency_histograms_summary','6bdbc450-264a-395f-9010-4ec6bbca372b']
                         ]
    return system_tables_data

# Retrieve the table name from the array of table names using the tableid
def find_table_name(table_id):
    #print(table_id)
    keyspacename = "unknownkeyspace"
    tablename = "unknowntable"
    for row in tables_data:
        if row[2] == table_id:
            #print(row[2])
            keyspacename = row[0]
            #print(keyspacename)
            tablename = row[1]
    return keyspacename, tablename

def check_system_keyspace(table_id):
    #print(table_id)
    keyspacename = "unknownkeyspace"
    tablename = "unknowntable"
    for row in system_tables_data:
        if row[2] == table_id:
            #print(row[2])
            keyspacename = row[0]
            #print(keyspacename)
            tablename = row[1]
    return keyspacename, tablename

# Format the table id into uuid format
def format_table_id(table_id_hex):
    formatted_table_id = f"{table_id_hex[:8]}-{table_id_hex[8:12]}-{table_id_hex[12:16]}-{table_id_hex[16:20]}-{table_id_hex[20:]}"
    return formatted_table_id

def convert_microseconds_epoch_to_utc(microseconds_epoch):
    # Convert microseconds to seconds
    seconds_epoch = microseconds_epoch / 1e6
    # Create a datetime object from the epoch time
    utc_datetime = datetime.datetime.utcfromtimestamp(seconds_epoch)
    # Format the datetime object to a human-readable string
    human_readable_date_time = utc_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return human_readable_date_time

def convert_milliseconds_epoch_to_utc(milliseconds_epoch):
    # Convert milliseconds to seconds
    seconds_epoch = milliseconds_epoch / 1e3
    # Create a datetime object from the epoch time
    utc_datetime = datetime.datetime.utcfromtimestamp(seconds_epoch)
    # Format the datetime object to a human-readable string
    human_readable_date_time = utc_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return human_readable_date_time

# There seems to be an odd offset used for some timestamps
def convert_epoch_with_offset_to_utc(nanoseconds_cas_epoch):
    # Convert the offset from milliseconds to seconds
    #offset = 513927723714
    offset = 515033060720
    milliseconds_cas_epoch = nanoseconds_cas_epoch // 1000000
    # Add the offset to the epoch time
    adjusted_epoch = milliseconds_cas_epoch + offset
    human_readable_date_time = convert_milliseconds_epoch_to_utc(adjusted_epoch)
    return human_readable_date_time

def check_truncated_at(new_mutation):
    # Check for trunacacted_at
    trunc_at_check = new_mutation[2:14].hex()
    # hex of truncated_at is 7472756e63617465645f6174
    if trunc_at_check ==  "7472756e63617465645f6174":
        trunc_at_true = True
        trunc_at_time_hex = new_mutation[-8:]
        trunc_at_time_int = int(binascii.hexlify(trunc_at_time_hex), 16)
        trunc_at_time = convert_milliseconds_epoch_to_utc(trunc_at_time_int)
        trunc_at_tableid_hex = new_mutation[20:36].hex()       
        if args.table_file_name is not None:
            trunc_at_table_id_formatted = format_table_id(trunc_at_tableid_hex)
            trunc_at_table_id_formatted_names = find_table_name(trunc_at_table_id_formatted)
            keyspace_name = trunc_at_table_id_formatted_names[0]
            table_name = trunc_at_table_id_formatted_names[1]
            formatted_mutation = "Truncation marker for " + keyspace_name + "." + table_name + " (" + trunc_at_table_id_formatted + ") at " + trunc_at_time
        else:
            formatted_mutation = "Truncation marker for table " + format_table_id(trunc_at_tableid_hex) + " at " + trunc_at_time
        return formatted_mutation, trunc_at_true
    else:
        trunc_at_true = False
        formatted_mutation = new_mutation
        return formatted_mutation, trunc_at_true

def check_truncated_at_v6(new_mutation):
    # Check for trunacacted_at
    trunc_at_check = new_mutation[6:18].hex()
    # hex of truncated_at is 7472756e63617465645f6174
    if trunc_at_check ==  "7472756e63617465645f6174":
        trunc_at_true = True
        trunc_at_time_hex = new_mutation[-17:-9]
        trunc_at_time_int = int(binascii.hexlify(trunc_at_time_hex), 16)
        trunc_at_time = convert_epoch_with_offset_to_utc(trunc_at_time_int)
        trunc_at_tableid_hex = new_mutation[20:36].hex()       
        if args.table_file_name is not None:
            trunc_at_table_id_formatted = format_table_id(trunc_at_tableid_hex)
            trunc_at_table_id_formatted_names = find_table_name(trunc_at_table_id_formatted)
            keyspace_name = trunc_at_table_id_formatted_names[0]
            table_name = trunc_at_table_id_formatted_names[1]
            formatted_mutation = "Truncation marker for " + keyspace_name + "." + table_name + " (" + trunc_at_table_id_formatted + ") at " + trunc_at_time
        else:
            formatted_mutation = "Truncation marker for table " + format_table_id(trunc_at_tableid_hex) + " at " + trunc_at_time
        return formatted_mutation, trunc_at_true
    else:
        trunc_at_true = False
        formatted_mutation = new_mutation
        return formatted_mutation, trunc_at_true

def check_gossip(new_mutation):
    # Check for gossip_generation
    gossip_check = new_mutation[2:19].hex()
    # hex of gossip_generation is 676f737369705f67656e65726174696f6e
    if gossip_check ==  "676f737369705f67656e65726174696f6e":
        formatted_mutation = "Gossip Generation " + str(int(binascii.hexlify(new_mutation[-4:]),16))
        return formatted_mutation
    else:
        formatted_mutation = new_mutation
        return formatted_mutation  

def check_deletion(new_mutation):
    is_deletion_true = False
    num_elements = new_mutation[0]
    # deletion marks with \xad
    if num_elements == 173 or num_elements == 180:
        is_deletion_true = True
        new_mutation = new_mutation[4:]
        formatted_mutation = "Deletion - " + str(new_mutation)
        return formatted_mutation, is_deletion_true
    else:
        formatted_mutation = new_mutation
        return formatted_mutation, is_deletion_true

# Make the mutation byte string more readable
def decode_byte_string(version, new_mutation, mutation_type):
    # Initialize an empty dictionary
    formatted_mutation = {}

    # Get the number of elements
    num_elements = new_mutation[0]
    if num_elements == 0:
        formatted_mutation = new_mutation
        return formatted_mutation

    # Initialize the index to the second byte
    index = 1
    # Extract the keys
    keys = []

    for _ in range(num_elements):
        key_length = new_mutation[index]
        #print(key_length)
        index += 1
        key = new_mutation[index:index + key_length]
        #key = new_mutation[index:index + key_length].decode('utf-8')
        keys.append(key)
        index += key_length

    # Split the remaining byte string by the delimiter dependent on version
    if version == 6 or mutation_type == '2':
        parts = new_mutation[1:].split(b'\x01,')
    else:
        parts = new_mutation[1:].split(b'$\x00')
    # Extract the values split on \x08
    #values = parts[1].split(b'\x08')[1:]
    if version == 6:
        try:
            values = parts[1].split(b'\x1a')[1:]
        except IndexError:
            print(new_mutation)
            print("There was an IndexError")
            formatted_mutation = new_mutation
            return formatted_mutation
    else:
        values = parts[1].split(b'\x08')[1:]
    # Map the keys to their respective values
    for i, key in enumerate(keys):
        try:
            value = values[i]
        except IndexError:
            print("There was another IndexError")
            formatted_mutation = new_mutation
            return formatted_mutation
        formatted_mutation[key] = value

    #print(formatted_mutation)
    return formatted_mutation

# Iterate through the commit log to sead the sync markers and mutations
# Descrioption of commit log format available at:
# https://cassandra.apache.org/_/blog/Learn-How-CommitLog-Works-in-Apache-Cassandra.html
def read_commit_log(file_path):
    mutations = []  # List to store all mutations

    with open(file_path, 'rb') as f:
        # Read and verify the header
        version = struct.unpack('>I', f.read(4))[0]
        log_id = struct.unpack('>Q', f.read(8))[0]
        parameters_length = struct.unpack('>H', f.read(2))[0]
        parameters = struct.unpack('>H', f.read(parameters_length))[0]
        header_crc = struct.unpack('>I', f.read(4))[0]

        # Verify Header CRC - not used
        #header_data = struct.pack('>IHI', version, log_id, parameters_length) + parameters
        #assert binascii.crc32(header_data) & 0xffffffff == header_crc, "Header CRC mismatch"
        #calc_header_crc = binascii.crc32(header_data) & 0xffffffff

        # Print the header information 
        print(f"File name             : {file_path}")
        print(f"Version               : {version}")
        print(f"ID                    : {log_id}")
        #print(f"Parameters Length: {parameters_length}")
        print(f"Commit Log Parameters : {parameters}")
        #print(f"Header CRC: {header_crc}")
        #print(f"Calculated header CRC: {calc_header_crc}")

        # Initialize the total count of mutations
        total_mutations_count = 0

        # Read and verify the sync marker
        sync_marker_num = 1
        while True:
            #print(f"Sync Marker: {sync_marker_num}")
            # Read 4 bytes for offset_to_next_sync_block
            offset_data = f.read(4)
            #print(offset_data)
            if len(offset_data) < 4:
                break  # End of file reached
            if offset_data == b'\x00\x00\x00\x00':
                break  # blank record
            offset_to_next_sync_block = struct.unpack('>I', offset_data)[0]
            offset_crc = struct.unpack('>I', f.read(4))[0]

            # Verify Offset CRC - not used
            #offset_data = struct.pack('>I', offset_to_next_sync_block)
            #assert binascii.crc32(offset_data) & 0xffffffff == offset_crc, "Offset CRC mismatch"
            #print(f"Offset to Next Sync Block: {offset_to_next_sync_block}")
            #print(f"Offset CRC: {offset_crc}")

            # Loop through the file reading mutations
            while f.tell() < offset_to_next_sync_block:
                # Read Mutation
                mutation_size_data = f.read(4)
                if len(mutation_size_data) < 4:
                    break  # End of file reached
                mutation_size = struct.unpack('>I', mutation_size_data)[0]
                mutation_size_crc = struct.unpack('>I', f.read(4))[0]

                # Verify Mutation Size CRC - not used
                mutation_size_data = struct.pack('>I', mutation_size)
                #assert binascii.crc32(mutation_size_data) & 0xffffffff == mutation_size_crc, "Mutation Size CRC mismatch"

                mutation_body = f.read(mutation_size)
                mutation_body_crc = struct.unpack('>I', f.read(4))[0]

                # Read the table name
                table_id = mutation_body[1:1 + 16]
                table_id_hex = table_id.hex()
                #print(table_id_hex)
                formatted_table_id = format_table_id(table_id_hex)
                #print(formatted_table_id)
                keyspace_table = ('unknown','unknown')
                mutation_type = '1'

                # check if this is a system keyspace - if so later we won't format the mutation as the mutation vary
                system_keyspace = check_system_keyspace(formatted_table_id)
                is_system_keyspace = system_keyspace[0].startswith("system")
                keyspace_table = system_keyspace
                if args.table_file_name is not None:
                    keyspace_table = find_table_name(formatted_table_id)
                if args.summary == True:
                    #don't worry about extracting all the info
                    pass
                else:
                    if version == 6:
                        #print(mutation_body)
                        key_size_raw = mutation_body[17]
                        key_size = key_size_raw + 1 
                        key = mutation_body[18:17 + key_size]
                        formatted_key = key
                        time_nano = "n/a"
                        the_mutation_start = key_size + 27
                        the_mutation = mutation_body[the_mutation_start:-1]
                        formatted_mutation = the_mutation
                        partition_data = "n/a"
    
    
                    if version == 7 or version == 8:
                        key_size_raw = mutation_body[17]
                        key_size = key_size_raw + 1
                        key = mutation_body[18:17 + key_size]
                        formatted_key = key
                        time_nano = mutation_body[17 + key_size:25 + key_size]
                        the_mutation_start = key_size + 27
                        the_mutation = mutation_body[the_mutation_start:-1]
                        #print(mutation_body)
                        #print(the_mutation)
                        # Check to see if the mutation is a deletion or a system keyspace - special handling for these
                        is_deletion_check = check_deletion(the_mutation)
                        if is_deletion_check[1] == True:
                            formatted_mutation = is_deletion_check[0]
                        elif is_system_keyspace == True:
                            #print(system_keyspace[0] + "." + system_keyspace[1])
                            truncated_mutation_check = check_truncated_at(the_mutation)
                            is_truncated_at = truncated_mutation_check[1]
                            #print(truncated_mutation_check)
                            if is_truncated_at == True:
                                formatted_mutation = truncated_mutation_check[0]
                            else:
                                formatted_mutation = check_gossip(truncated_mutation_check[0])
                            #print(formatted_mutation)
                        else: 
                            formatted_mutation = decode_byte_string(version, the_mutation, mutation_type)                  
                        partition_data = "n/a"
    
                    if version == 680:            
                        key_size_raw = mutation_body[18:19].hex()
                        key_size = int(key_size_raw, 16) + 1
                        key = mutation_body[19:18 + key_size]
                        formatted_key = key
                        partition_data_size_raw = mutation_body[18 + key_size:19 + key_size].hex()
                        partition_data_size = int(partition_data_size_raw, 16)
                        #print(partition_data_size)
                        partition_data = mutation_body[18 + key_size:19 + key_size + partition_data_size].hex()
                        #print(partition_data)
                        time_nano = mutation_body[19 + key_size + partition_data_size:27 + key_size + partition_data_size]
                        magic_byte=mutation_body[27 + key_size + partition_data_size:29 + key_size + partition_data_size].hex()
                        #print(magic_byte)
                        if magic_byte != '0000':
                            mutation_type = '2'
                        #print(mutation_type)          
                        if mutation_type == '2':
                            the_mutation_start = key_size + partition_data_size + 34
                        else:
                            the_mutation_start = key_size + partition_data_size + 29
                        the_mutation = mutation_body[the_mutation_start:-1]
                        #formatted_mutation = decode_byte_string(version, the_mutation, mutation_type)
                        formatted_mutation = the_mutation
    
                    # Verify Mutation Body CRC - not used
                    #assert binascii.crc32(mutation_body) & 0xffffffff == mutation_body_crc, "Mutation Body CRC mismatch"

                # Store the mutation details in the list
                if args.full == True:
                    if args.user == True and (keyspace_table[0].startswith("system") == True or keyspace_table[0].startswith("dse_perf") == True):
                        pass
                    else:
                        mutations.append({
                            "MutationSize": mutation_size,
                            "TableID": formatted_table_id,
                            "KeyspaceName": keyspace_table[0],
                            "TableName": keyspace_table[1],
                            "Key": key,
                            "FormattedKey": formatted_key,
                            "PartitionData": partition_data,
                            "TimeCreatedns": time_nano,
                            #"Mutation": the_mutation,
                            "FormattedMutation": formatted_mutation,
                        })
                else:
                    if args.user == True and (keyspace_table[0].startswith("system") == True or keyspace_table[0].startswith("dse_perf") == True):
                        pass
                    else:
                        mutations.append({
                            "MutationBody": mutation_body,
                            "TableID": formatted_table_id,
                            "KeyspaceName": keyspace_table[0],
                            "TableName": keyspace_table[1],
                        })
                        
    
            # Increment the total count of mutations
            total_mutations_count += len(mutations)

            #Print the output
            mutation_number = 1
            for mutation in mutations:
                if args.full == True:
                    if args.user == True and mutation['KeyspaceName'].startswith("system") == True:
                        #mutation_number += 1
                        pass
                    else:
                        print(f"\nSyncMarker - Mutation : {sync_marker_num} - {mutation_number}")
                        print(f"Mutation Size   : {mutation['MutationSize']}")
                        print(f"Table ID        : {mutation['TableID']}")
                        if args.table_file_name is not None:
                            print(f"Keyspace Name   : {mutation['KeyspaceName']}")
                            print(f"Table Name      : {mutation['TableName']}")
                        print(f"Key             : {mutation['FormattedKey']}")
                        if version == 680:
                            print(f"Partition Data  : {mutation['PartitionData']}")
                        if not version == 6:
                            TimeCreatednshex = mutation['TimeCreatedns'].hex()
                            this_date_time = convert_epoch_with_offset_to_utc(int(binascii.hexlify(mutation['TimeCreatedns']), 16))
                            print(f"Time Created ns : {this_date_time}")
                            print(f"Time Created ns : {TimeCreatednshex}")
                        print(f"Mutation        : {mutation['FormattedMutation']}")
                elif args.summary == True:
                    #do nothing
                    pass
                else:
                    print(f"\nSyncMarker - Mutation : {sync_marker_num} - {mutation_number}")
                    print(f"Table ID        : {mutation['TableID']}")
                    print(f"Keyspace Name   : {mutation['KeyspaceName']}")
                    print(f"Table Name      : {mutation['TableName']}")
                mutation_number += 1
            sync_marker_num += 1
            # reset the list
            mutations = [] 

    # Print the total count of mutations
    print(f"\nTotal Count of Mutations : {total_mutations_count}")



# Read the commit log name passed in from the command and if not prompt for the commit log name
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-s", "--summary", action="store_true", help="Gives a summary of the CommitLog. Just the header information and total number of mutations")
group.add_argument("-f", "--full", action="store_true", help="Full output. The output can be VERY large. Pipe to \'less\' to more easily view output.")
parser.add_argument("file_path", help="Path to CommitLog file which you want to read")
#parser.add_argument("-t", "--table", action ="store_true", help="Resolve the table ID to the table name.")
parser.add_argument("-t", "--table_file_name", type=str, help="Resolve the table ID to the table name. Provide a file name containing the keyspace, table and UUID of the table. Command to do this is: cqlsh -e \"copy system_schema.tables (keyspace_name,table_name,id) to 'tables.out' with header=false;\"")
parser.add_argument("-u", "--user", action ="store_true", help="Only output non-system keyspace mutations and summary information.")
args = parser.parse_args()

# Read the tables.out file
tables_data = []
tables_files_path = args.table_file_name
#print(args.table)
if args.table_file_name is not None:
    if os.path.exists(tables_files_path):
        with open(tables_files_path, 'r') as file:
            lines = file.readlines()
            # Process each line
            for line in lines[0:]:  # Skip the header line
                # Ignore blank lines
                if line.strip():
                    # Split the line by the delimiter and strip whitespace
                    elements = [element.strip() for element in line.split(',')]
                    # Append the processed line to the main list
                    tables_data.append(elements)


# Define the default system tables
system_tables_data = set_system_tables()

# Check if the commit log exists and if so run the read_commit_log
if os.path.exists(args.file_path):
    #print(args.file_path)
    read_commit_log(args.file_path)
else:
    print("Commit log file " + args.file_path + " does not exist.")
    exit (1)