""" flute_to_galapagos: Convert FluTE output to Galapagos readable format.
    
    DESCRIPTION
        This program converts FluTE LogX output files into Galapagos format.

    USAGE
        python flute_to_galapagos.py [input file]
        python flute_to_galapagos.py [input file] [log file]

    INPUT
        input file - The input file should be a LogX file (e.g. Log2) produced by FluTE
        log file - If provided, the log file will contain information useful for debugging

    OUTPUT
        The program outputs a CSV file that can be uploaded and read by Galapagos
"""

import sys
import os
import datetime

outlog = None

def add_to_output(out, simulator_time, tract_id, age_ranges, disease_state, infection_state, state_values):
    for i in range(len(state_values)):
        out_row = [simulator_time, tract_id, age_ranges[i], disease_state, infection_state, state_values[i]]
        out.write(','.join(out_row) + '\n')

if len(sys.argv) < 2:
    basename = os.path.basename(__file__)
    print('DESCRIPTION\n    This program converts FluTE LogX output files into Galapagos format.\n')
    print('USAGE\n    python %s [input file]\n    python %s [input file] [log file]\n' % (basename, basename))
    print('INPUT\n    input file - The input file should be a LogX file (e.g. Log2) produced by FluTE\n' +
        '    log file - If provided, the log file will contain information useful for debugging\n')
    print('OUTPUT\n    The program outputs a CSV file that can be uploaded and read by Galapagos\n')
else:
    filepath = sys.argv[1]
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print('Error: Please enter a valid file path as your first command line argument.')
        sys.exit(1)

    filename = os.path.basename(filepath)

    if len(sys.argv) == 3:
        logfile = sys.argv[2]
        outlog = open(logfile, 'a')
        outlog.write('galapagos_%s\n' % filename)
        outlog.write('--------------------------\n')

    flute_data = []
    for i in range(1, len(lines)):
        flute_data.append(lines[i].rstrip('\n').split(','))

    curr_row = 1
    total_rows = len(flute_data)

    age_ranges = ['0-4', '5-18', '19-29', '30-64', '65+']
    with open('galapagos_' + filename, 'w+') as out:
        out.write('simulator_time,location,age_range,disease_state,infection_state,count\n')
        for row in flute_data:
            simulator_time = row[0]
            tract_id = row[1]

            symptomatic = row[2:7]
            newly_infected = row[12:17]
            susceptible = row[22:27]
            exposed = row[27:32]
            infectious = row[32:37]
            recovered = row[37:42]
            newly_infectious = row[42:47]

            #cum_sympyomatic = row[7:12]
            #ever_infected = row[17:22]
            #add_to_output(out, simulator_time, tract_id, age_ranges, 'symptomatic', 'infectious', symptomatic)
            #add_to_output(out, simulator_time, tract_id, age_ranges, 'cum_sympyomatic', cum_sympyomatic)

            add_to_output(out, simulator_time, tract_id, age_ranges, 'asymptomatic', 'newly_latent', newly_infected)
            add_to_output(out, simulator_time, tract_id, age_ranges, 'asymptomatic', 'susceptible', susceptible)
            add_to_output(out, simulator_time, tract_id, age_ranges, 'asymptomatic', 'exposed', exposed)
            add_to_output(out, simulator_time, tract_id, age_ranges, 'symptomatic', 'infectious', infectious)
            add_to_output(out, simulator_time, tract_id, age_ranges, 'recovery', 'recovered', recovered)
            add_to_output(out, simulator_time, tract_id, age_ranges, 'symptomatic', 'newly_infectious', newly_infectious)


            if(outlog is not None and (curr_row % 10000 == 0 or curr_row == 1 or curr_row == total_rows)):
                outlog.write('%s - Writing to file: %d/%d\n' % (datetime.datetime.now(), curr_row, total_rows))

            curr_row += 1

    if outlog is not None:
        outlog.write('\n')
        outlog.close()
