from tools.utils import *

def save_pairs_2_db():
    name_files = os.listdir(raw_data_dir)
    name_files = [x.split('.')[0] for x in name_files]
    pair_list = list(itertools.combinations(name_files,2))
    random.seed(2019)
    random.shuffle(pair_list)
    if os.path.exists(db_path):
        logger.info('Remove old db,path is {}'.format(db_path))
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    logger.info('Create table,name is {}'.format(table))

    # Create table
    c.execute('''CREATE TABLE {}
             (id,index_i, index_j,label,state,create_time,label_time,user)'''.
          format(table))
    logger.info('Write pairs to table {}'.format(table))
    for id, pair in enumerate(pair_list):
        create_time = getNowTime()
        c.execute("INSERT INTO pairs VALUES ({},{},{},{},{},'{}','{}','{}')".format(
        id + 1, pair[0], pair[1], -1, wait_state, create_time, '',''))
    conn.commit()
    conn.close()
    logger.info('Finish create table {}'.format(table))

if __name__ == '__main__':
    save_pairs_2_db()