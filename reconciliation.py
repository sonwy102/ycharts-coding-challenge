TRN_CODES = {
    'SELL': 1,
    'BUY': -1,
    'DEPOSIT': 1,
    'FEE': -1,
    'DIVIDEND': 1
}

def process_fin_data(filename):
    
    file_path = './data/' + filename
    pos_headers = set(['D0-POS', 'D1-POS'])
    trn_headers = set(['D1-TRN'])

    fin_data = {}
    curr_header = ''
    with open(file_path) as f:
        
        for line in f:
            line = line.rstrip()
            if line in pos_headers or line in trn_headers:
                curr_header = line
                fin_data[curr_header] = {}
            else:
                record = line.split(' ')
                symbol = record[0]
                if curr_header in pos_headers:
                    shares = float(record[1])
                    fin_data[curr_header][symbol] = shares
                elif curr_header in trn_headers:
                    code = TRN_CODES[record[1]]
                    shares = float(record[2])
                    total_val = float(record[3])
                    if symbol not in fin_data[curr_header]:
                        fin_data[curr_header][symbol] = {
                            'share': -1 * code * shares, 
                            'total': code * total_val
                        }
                    else:
                        fin_data[curr_header][symbol]['share'] += -1 * code * shares
                        fin_data[curr_header][symbol]['total'] += code * total_val
    
    return fin_data

def calculate_expected_pos(pos, trn):
    
    for symbol in trn:
        if symbol in pos:
            pos[symbol] += trn[symbol]['share']
        else:
            pos[symbol] = trn[symbol]['share']
        pos['Cash'] += trn[symbol]['total']
    
    return pos

def calculate_recon(pos_expected, pos_observed):
    
    recon_fails = pos_observed.copy()

    for symbol in pos_expected:
        if symbol not in pos_observed:
            recon_fails[symbol] = 0 - pos_expected[symbol]
        else:    
            recon_fails[symbol] -= pos_expected[symbol]
        
        if recon_fails[symbol] == 0:
            recon_fails.pop(symbol)

    return recon_fails                

def write_recon_file(recon_fails, filename='recon_out.txt'):
    
    file_path = './data/' + filename
    with open(file_path, 'w') as outfile:
        for symbol in recon_fails:
            outfile.write(symbol + ' ' + str(recon_fails[symbol]))
            outfile.write('\n')
        
        

        