TRN_CODES = {
    'SELL': 1,
    'BUY': -1,
    'DEPOSIT': 1,
    'FEE': -1,
    'DIVIDEND': 1
}

def process_fin_data(filename):
    """Reads and processes input data file.

    Args: 
        filename (str): name of input file with positions and transaction data
    
    Returns:
        dict: a dict of 3 dicts representing each section of data 
        (D0-POS, D1-TRN, D1-POS)
    """

    pos_headers = set(['D0-POS', 'D1-POS'])
    trn_headers = set(['D1-TRN'])
    fin_data = {}
    curr_header = ''
    file_path = './data/' + filename

    # read each line of file and hash each record
    with open(file_path) as f:
        for line in f:
            line = line.rstrip()
            if line in pos_headers or line in trn_headers:
                curr_header = line
                fin_data[curr_header] = {}
            else:
                record = line.split(' ')
                symbol = record[0]

                # if record is a position, map record symbol to number of shares
                if curr_header in pos_headers:
                    shares = float(record[1])
                    fin_data[curr_header][symbol] = shares

                # if record is a transaction, map symbol to number of shares 
                # and total value
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

def get_expected_pos(pos, trn):
    """Calculates and returns positions expected after all transactions

    Args:
        pos (dict): initial positions before any transaction
        trn (dict): transactions that occurred in the account on Day 1
    
    Returns:
        dict: expected positions after all transactions at the end of Day 1
    """
    
    for symbol in trn:
        if symbol in pos:
            pos[symbol] += trn[symbol]['share']
        else:
            pos[symbol] = trn[symbol]['share']
        pos['Cash'] += trn[symbol]['total']
    
    return pos


def calculate_recon(pos_expected, pos_observed):
    """Performs unit reconciliation for all positions in the account.

    Args:
        pos_expected (dict): positions and their expected shares/values
        pos_observed (dict): positions and their observed shares/values in account

    Returns:
        dict: positions that failed the unit reconciliation mapped to the
        discrepancies in shares/values
    """

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
    """Write positions that failed unit reconciliation to output file 

    Args:
        recon_fails (dict): positions that failed the unit reconciliation and
        their discrepancies 
        filename (str): name of output file (default = recon_out.txt) 
    
    Returns:
        None
    """

    file_path = './data/' + filename
    open(file_path, 'w').close()  # resetting file content before writing
    with open(file_path, 'w') as outfile:
        for symbol in recon_fails:
            outfile.write(symbol + ' ' + str(recon_fails[symbol]))
            outfile.write('\n')


if __name__ == "__main__":
    
    fin_data = process_fin_data('test_input.txt')
    pos_exp = get_expected_pos(fin_data['D0-POS'], fin_data['D1-TRN'])
    failed_recon = calculate_recon(pos_exp, fin_data['D1-POS'])
    write_recon_file(failed_recon)

    
        
        

        