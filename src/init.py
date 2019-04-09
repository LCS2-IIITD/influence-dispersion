import utils 
import argparse
import logging
import sys
import pickle
parser = argparse.ArgumentParser(description='Calculating the IDT metric...')
parser.add_argument('--dataset' , help = 'path of the dataset')
parser.add_argument('--dumps' , help = 'path to store the pickled files') 
parser.add_argument('--graph_path', help = 'Path to pickle file of citation graph')
parser.add_argument('--year_dict_path' , help = 'Path to pickle file of Publication year Dictionary')

args = parser.parse_args()
logging.StreamHandler(sys.stdout)
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S' , level=logging.INFO) 

if __name__ == '__main__':
	global_citation_graph = ''
	if args.graph_path is None:
		logging.info('Parsing Dataset')
		global_citation_graph = utils.parse_dataset(args.dataset)
		utils.dump_file(args.dumps, 'global_citation_graph_full' , global_citation_graph)
	else:
		logging.info('Getting Pickle Graph')
		global_citation_graph = utils.get_pickle_dump(args.graph_path , 'global_citation_graph')

	paper_year_dict = ' '
	if args.year_dict_path is None:
		logging.info('Parsing Dates from dataset')
		paper_year_dict = utils.parse_dates(args.dataset) 
		logging.info('Serialising Paper- Year Dictionary') 
		utils.dump_file(args.dumps , 'paper_year_dict' , paper_year_dict) 
	else:
		logging.info('Unpickling the Date Dictionary')
		paper_year_dict = utils.get_pickle_dump(args.year_dict_path , 'paper_year_dict')

	logging.info('Removing Invalid Edges')
	global_citation_graph = utils.check_edge_validity(global_citation_graph, paper_year_dict)
	logging.info('Removing Cycles')
	global_citation_graph = utils.remove_cycles(global_citation_graph) 
	logging.info('Removed Cycles')
	utils.dump_file(args.dumps , 'global_citation_graph_full_decyclised' , global_citation_graph) 
	IDT_Dict, IDT_root_to_leaf_paths = utils.IDT_init(global_citation_graph)
	logging.info('Serialising the Graph')
	
	
	logging.info('Serialising IDT Dictionary & IDT_root_to_leaf_paths')
	utils.dump_file(args.dumps , 'IDT_Dict_full' , IDT_Dict) 
	utils.dump_file(args.dumps , 'IDT_root_to_leaf_paths_full' , IDT_root_to_leaf_paths)  



