import os
import time
import csv
import copy
import shutil

from lib import path_utils, metaparameters, parser, data_utils


def write_data(connections_aggregated, configuration_aggregated, target_path):
    # Cleanup
    if os.path.isdir(target_path):
        shutil.rmtree(target_path)
    os.mkdir(target_path)

    # Create folder for each logfile
    for filename in connections_aggregated:
        if not os.path.isdir('{0}/{1}'.format(target_path, filename)):
            os.makedirs('{0}/{1}'.format(target_path, filename))

        # Write each connection to a separate file
        for connection in list(connections_aggregated[filename]):

            # Normal values over time for each connection
            csvfile = open('{0}/{1}/{2}.csv'.format(target_path, filename, connection), 'w+')
            csvwriter = csv.writer(csvfile, delimiter=',')

            for key in connections_aggregated[filename][connection]:
                tmp = connections_aggregated[filename][connection][key]
                tmp.insert(0, key)
                csvwriter.writerow(tmp)

            csvfile.close()

    # Session total data RELAY
    filename = "aggregated_data_RELAY"
    csvfile_session_avg = open('{0}/{1}.csv'.format(target_path, filename), 'w+')
    csvwriter_session_avg = csv.writer(csvfile_session_avg, delimiter=',')

    for key in configuration_aggregated['RELAY']:
        tmp = [key]
        tmp.extend(configuration_aggregated['RELAY'][key])
        csvwriter_session_avg.writerow(tmp)

    csvfile_session_avg.close()

    # Session total data P2P
    filename = "aggregated_data_P2P"
    csvfile_session_avg = open('{0}/{1}.csv'.format(target_path, filename), 'w+')
    csvwriter_session_avg = csv.writer(csvfile_session_avg, delimiter=',')

    for key in configuration_aggregated['P2P']:
        tmp = [key]
        tmp.extend(configuration_aggregated['P2P'][key])
        csvwriter_session_avg.writerow(tmp)

    csvfile_session_avg.close()


# Unifies the timestamps and data length of all provided files
def unify_timestamps(session_infos):
    i_start_ts_relay = -1
    i_end_ts_relay = 1000000000000
    i_end_ts_p2p = 1000000000000

    # Find lower and upper timestamp
    for file in session_infos:
        for connection in session_infos[file]:
            if "RELAY" in connection:
                # Find largest interval that is covered by all files
                if session_infos[file][connection]['timestamp'][0] > i_start_ts_relay:
                    i_start_ts_relay = session_infos[file][connection]['timestamp'][0]
                if session_infos[file][connection]['timestamp'][-1] < i_end_ts_relay:
                    i_end_ts_relay = session_infos[file][connection]['timestamp'][-1]

            if "P2P" in connection:
                if session_infos[file][connection]['timestamp'][-1] < i_end_ts_p2p:
                    i_end_ts_p2p = session_infos[file][connection]['timestamp'][-1]

    # Cut the data at the defined indices
    for file in session_infos:
        for connection in session_infos[file]:
            i_index = -1
            if "RELAY" in connection:
                # Find start/end index
                for timestamp in session_infos[file][connection]['timestamp']:
                    if timestamp == i_start_ts_relay:
                        i_index_start = session_infos[file][connection]['timestamp'].index(timestamp)
                    if timestamp == i_end_ts_relay:
                        i_index_end = session_infos[file][connection]['timestamp'].index(timestamp)
                        break

                # Cut all data
                for key in session_infos[file][connection]:
                    session_infos[file][connection][key] = session_infos[file][connection][key][i_index_start:i_index_end]

            if "P2P" in connection:
                # Find timestamp
                for timestamp in session_infos[file][connection]['timestamp']:
                    if timestamp == i_end_ts_p2p:
                        i_index = session_infos[file][connection]['timestamp'].index(timestamp)
                        break
                # Cut data
                for key in session_infos[file][connection]:
                    session_infos[file][connection][key] = session_infos[file][connection][key][:i_index]
    return session_infos


# Parses one measurement. Input path is directory with corresponding logfiles
# e.g. 181025_10.53/
def parse_measurement(path):
    # 2 = 2 log files 4 = log files + tcpdumps
    if len(os.listdir(path)) == 2 or len(os.listdir(path)) == 4:
        parse_measurement_2_clients(path)
    elif len(os.listdir(path)) == 3 or len(os.listdir(path)) == 6:
        parse_measurement_3_clients(path)


# Parse one measurement with two clients
def parse_measurement_2_clients(path):
    logfiles_connection_data_aggregated = {}

    b_found_data = False

    # Parse each file
    for file in os.listdir(path):
        if not file.endswith(".log"):
            continue
        filename = os.path.join(path, file)
        dict_file_infos = parser.parse_file_2_clients(filename)

        # dict_file_infos:
        # conn1
        #   ssrc1
        #   ssrc2
        # conn2
        #   ssrc1
        #   ssrc2

        # parser.parse returns an empty dict on failure
        if len(dict_file_infos) == 0:
            continue

        logfiles_connection_data_aggregated[file] = dict_file_infos
        b_found_data = True

    # Only write data if at least one file was parsed correctly
    if b_found_data and len(logfiles_connection_data_aggregated) == 2:
        logfiles_connection_data_aggregated = unify_timestamps(logfiles_connection_data_aggregated)

        # To calculate metaprameters we must make sure to have both files
        logfiles_connection_data_aggregated = metaparameters.add_metaparameters(logfiles_connection_data_aggregated)

        # Get aggregated data for this session
        logfiles_data_aggregated = data_utils.get_session_aggregated(logfiles_connection_data_aggregated)

        target_path = path.replace('logs', 'parsed')
        write_data(logfiles_connection_data_aggregated, logfiles_data_aggregated, target_path)


# Parse one measurement with three clients
def parse_measurement_3_clients(path):
    logfiles_connection_data_aggregated = dict()
    logfiles_media_direction = dict()

    b_found_data = False

    # Parse each file
    for file in os.listdir(path):
        if not file.endswith(".log"):
            continue
        filename = os.path.join(path, file)
        dict_file_infos, dict_media_directions = parser.parse_file_3_clients(filename)

        if len(dict_file_infos) == 0:
            continue

        logfiles_media_direction[file] = dict_media_directions
        logfiles_connection_data_aggregated[file] = dict_file_infos
        b_found_data = True



    # Only write data if at least one file was parsed correctly
    if b_found_data and len(logfiles_connection_data_aggregated) == 3:
        logfiles_connection_data_aggregated = unify_timestamps(logfiles_connection_data_aggregated)

        # Calculate metaparameters
        logfiles_connection_data_aggregated = metaparameters.add_metaparameters(logfiles_connection_data_aggregated,
                                                                                logfiles_media_direction)

        # Get aggregated data for session
        logfiles_data_aggregated = data_utils.get_session_aggregated(logfiles_connection_data_aggregated)

        target_path = path.replace('logs', 'parsed')
        write_data(logfiles_connection_data_aggregated, logfiles_data_aggregated, target_path)


# Starting point for script execution
if __name__ == "__main__":

    ts_start = time.time()

    # Cleanup target directory
    if os.path.exists('parsed/'):
        shutil.rmtree('parsed/')
        os.makedirs('parsed/')

    bandwidth_list = os.listdir('logs/')

    # Stores results from single measurements (same bandwidth)
    dict_measurement_averages = {}

    # Stores averages for different bandwidths
    dict_bandwidth_averages = {}

    # Parse all bandwidths
    for bandwidth in bandwidth_list:
        if not os.path.isdir(os.path.join('parsed/', bandwidth)):
            os.makedirs(os.path.join('parsed/', bandwidth))

        # Parse all measurements for a single bandwidth
        for measurement in os.listdir(os.path.join('logs/', bandwidth)):
            parse_measurement(os.path.join('logs/', bandwidth, measurement))

    ts_end = time.time()
    duration = float(ts_end) - float(ts_start)

    print("Parsed {0} files".format(parser.gi_parsed_files_count))
    print("Processing time: {0}s".format(duration))

    path_utils.move_results_complete()
