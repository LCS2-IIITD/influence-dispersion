import utils 
import argparse
import logging
import sys
parser = argparse.ArgumentParser(description='Calculating the IDT metric...')
parser.add_argument('--dumps' , help = 'path to store the pickled files') 
parser.add_argument('--id',help = 'Paper ID According to Dataset')
parser.add_argument('--year' , help = 'Year to get the NID of', type = int)

args = parser.parse_args()
logging.StreamHandler(sys.stdout)
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S' , level=logging.INFO) 

if __name__ == '__main__':
	logging.info('Getting Paper Year Dictionary')
	paper_year_dict = utils.get_pickle_dump(args.dumps, 'paper_year_dict') 
	logging.info('Getting IDT Dictionary')
	IDT_dict = utils.get_pickle_dump(args.dumps, 'IDT_Dict_full')
	id = args.id 
	idi , max_idi, min_idi, nid = utils.get_idi_till_year(IDT_dict[id], int(args.year), paper_year_dict) 
	logging.info('NID: {} | IDI: {} | Max. IDI: {} | Min. IDI: {}'.format(nid, idi, max_idi, min_idi)) 


	
