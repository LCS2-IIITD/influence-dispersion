import networkx as nx 
import os
from os import listdir
import pickle
import random
#global Variables
INDEX_OFFSET = 6
CITE_OFFSET = 3
YEAR_OFFSET_SHORT = 2
YEAR_OFFSET_LONG = 3
EMPTY = ""


def get_pickle_dump(filepath,filename):
	"""
	@Params:
	filename: filename inside the ./dumps folder
	@Returns:
	Variable: Returns the pickled variable
	"""

	with open(filepath +'/'+filename+'.pickle','rb') as handle:
		Variable = pickle.load(handle)
	return Variable


def dump_file(filepath,filename, Variable):
	"""
	@Params:
	filename: filename inside the ./dumps folder for dumping
	Variable: Variable to dump inside the file
	@Returns:
	None
	"""
	with open(filepath +'/'+filename+'.pickle','wb') as handle:
		pickle.dump(Variable,handle,protocol=pickle.HIGHEST_PROTOCOL)

def extract_paper_id(line):
	"""
	@Params:
	line: text line
	@Returns: 
	paper_id: extracts the paper-id enclosed within "[*]"
	"""
	line = line.split("[")
	# "-2" is to remove the last 2 characters for CLRF line endings.
	paper_id = line[-1][:-2]
	return paper_id


def parse_dataset(path):
	"""
	@Params
	path: Path to the Dataset
	@Returns
	A global citation graph with edges from the citer to the cited.
	"""

	global_citation_graph = nx.DiGraph() 
	fields = os.listdir(path)
	for field in fields:
		if field.split("_")[-1] != 'data.txt': #if not a data text file
			continue
		dataset_path = path + "/" + field
		file = open(dataset_path, 'rb')
		line = file.readline().decode('utf8')
		name = EMPTY
		while line:
			if line[:INDEX_OFFSET] == '#index':
				name = line[INDEX_OFFSET:-1]

			elif line[:CITE_OFFSET] == '#%*' and name != EMPTY:
				cited_by_index_name = extract_paper_id(line) 
				global_citation_graph.add_edge(name , cited_by_index_name)

			elif line[:CITE_OFFSET] == "#$*" and name != EMPTY:
				citing_index_name = extract_paper_id(line) 
				global_citation_graph.add_edge(citing_index_name , name)
			line = file.readline().decode('utf8')


	return global_citation_graph

def parse_dates(path):
	"""
	@Params:
	path: Path to Dataset
	@Returns: 
	PAPER_YEAR_DICT: Dictionary with paper ids as keys publishing years as venues
	"""
	PAPER_YEAR_DICT = {}
	fields = listdir(path)
	for field in fields:
		if field.split("_")[-1] != 'data.txt':
			continue

		dataset_path = path + "/" + field
		file = open(dataset_path, 'rb')
		line = file.readline().decode('utf8')
		# line = (line.encode('ascii', 'ignore')).decode("utf-8")
		paper_name = EMPTY

		while line:
			if line[:INDEX_OFFSET] == "#index":
				paper_name = line[INDEX_OFFSET:-1]

			elif line[:YEAR_OFFSET_SHORT] == "#y" and paper_name != EMPTY and line[:4] != "#ypp" and line[:5] != "#yno.":
				year = line[YEAR_OFFSET_SHORT:-1]
				PAPER_YEAR_DICT[paper_name] = year 
				paper_name = EMPTY

			elif line[:CITE_OFFSET] == '#%*':
				paper_name = extract_paper_id(line)

			elif line[:YEAR_OFFSET_LONG] == '#%y' and paper_name != EMPTY and line[:5] != "#%ypp" and line[:6] != "#%yno.":
				year = line[YEAR_OFFSET_LONG:-1]
				PAPER_YEAR_DICT[paper_name] = year
				paper_name = EMPTY

			elif line[:CITE_OFFSET] == '#$*':
				paper_name = extract_paper_id(line)

			elif line[:YEAR_OFFSET_LONG] == '#$y' and paper_name != EMPTY and line[:5] != "#$ypp" and line[:6] != "#$yno.":
				year = line[YEAR_OFFSET_LONG:-1]
				PAPER_YEAR_DICT[paper_name] = year
				paper_name = EMPTY

			line = file.readline().decode('utf8')
			# line = (line.encode('ascii', 'ignore')).decode("utf-8")
	
	return PAPER_YEAR_DICT



def check_edge_validity(global_citation_graph, PAPER_YEAR_DICT):
	"""
	@Params:
	global_citation_graph: The global citation graph with all edges
	PAPER_YEAR_DICT: Contains the publishing of the papers

	@Returns:
	global_citation_graph: The global citation graph with noisy edges removed 
							i.e. those edges whose citer's publishing year is 
							less than cited's publishing year
	"""
	edge_set = list(global_citation_graph.edges())

	for edge_ in edge_set:
		edge_1_present = edge_[0] in PAPER_YEAR_DICT
		edge_2_present = edge_[1] in PAPER_YEAR_DICT
		if  edge_1_present and edge_2_present and PAPER_YEAR_DICT[edge_[0]] < PAPER_YEAR_DICT[edge_[1]]:
			global_citation_graph.remove_edge(*edge_)

		elif edge_[0] == edge_[1]:
			global_citation_graph.remove_edge(*edge_)

		elif not edge_1_present or not edge_2_present:
			global_citation_graph.remove_edge(*edge_)

	global_citation_graph = nx.DiGraph() 
	global_citation_graph.add_edges_from(edge_set)

	return global_citation_graph



def remove_cycles(global_citation_graph):
	"""
	@Params:
	global_citation_graph

	@Returns: 
	global_citation_graph: with no cycles due to noisy data by randomly removing one edge in the cycle
							any subgraphs

	"""
	node_list = list(global_citation_graph.nodes())

	for paper in node_list:

		induced_subgraph = set()
		induced_subgraph_node_list = global_citation_graph.in_edges(nbunch = [paper])

		for e in induced_subgraph_node_list:
			induced_subgraph.add(e[0])

		induced_subgraph.add(paper)

		subgraph_ = global_citation_graph.subgraph(induced_subgraph)
		cycle_lists = nx.simple_cycles(subgraph_)

		for cycle_list in list(cycle_lists):
			length_of_cycle = len(cycle_list)
			if length_of_cycle == 1:
				try:
					global_citation_graph.remove_edge(cycle_list[0] , cycle_list[0])
				except IndexError:
					print(cycle_list)

				except nx.exception.NetworkXError:
					pass

			elif length_of_cycle == 2:
				try:
					global_citation_graph.remove_edge(cycle_list[0] , cycle_list[1])
				except IndexError:
					print(cycle_list)

				except nx.exception.NetworkXError:
					pass

			#Removing a Random Edge
			else:
				r = random.randint(2,length_of_cycle - 1)
				try:
					global_citation_graph.remove_edge(cycle_list[r- 1] , cycle_list[r])
				except IndexError:
					print(cycle_list)
				except nx.exception.NetworkXError:
					pass

	return global_citation_graph




def IDT_init(global_citation_graph):
	"""
	@Params:
	global_citation_graph: The global citation graph 

	@Returns:
	IDT: a dictionary with key as the paper index and value as the IDT (Influence Dispersion Tree)
	IDT_root_to_leaf_paths: Dict with keys as Paper Name and value as All Root to leaf paths
	"""
	IDT = {}
	IDT_root_to_leaf_paths = {} 
	nodes_with_cycle = 0
	for paper in global_citation_graph.nodes().copy():

		depth_dict = {}
		induced_graph = set()
		induced_graph_list = list(global_citation_graph.in_edges(nbunch = [paper]))


		for e in induced_graph_list:
			induced_graph.add(e[0])

		induced_graph.add(paper)

		
		#IDG has the reversed edges compared to the IDG discussed in paper. This
		# has been taken care of at the end when the reversed IDT graph is returned
		IDG = global_citation_graph.subgraph(induced_graph)

		for e in IDG.nodes():
			e_list = list(IDG.out_edges(nbunch = [e]))
			if len(e_list) > 1:
				IDG.remove_edge(e , paper)

		visited = set()
		not_visited = set(IDG.nodes())
		not_visited.discard(paper)
		visited.add(paper)
		depth_dict[paper] = 0
		cur_depth = 1
		while(len(not_visited) > 0):
			cur_visit_set = set()
			for p in not_visited:
				if all_edges_in_visited(IDG,p,visited):
					ancestor_paper = get_parent_with_most_depth(depth_dict , IDG , p)
					IDG = remove_edges_except(p , ancestor_paper , IDG)
					cur_visit_set.add(p)
					depth_dict[p] = cur_depth
			visited = visited.union(cur_visit_set)
			for p in cur_visit_set:
				not_visited.discard(p)
			cur_depth += 1

		branch = []
		total_branches = []
		get_depth_of_each_branch(IDG , paper , 0, branch , total_branches)
		IDT_root_to_leaf_paths[paper] = total_branches
		# IDT_ = IDG.reverse(copy = False)
		IDT_ = IDG 
		IDT[paper] = IDT_

	return IDT , IDT_root_to_leaf_paths



def all_edges_in_visited(IDG,p, visited):
	"""
	@Params: 
	IDG: IDG of the paper 
	p: paper whose neighbours we need to check
	visited: set of nodes which are visited
	@Returns:
	True if all the neighbours are visited else False
	"""
	edge_list = list(IDG.out_edges(nbunch = [p]))
	for e in edge_list:
		if e[1] not in visited:
			return False
	return True


def get_parent_with_most_depth(depth_dict , IDG, p):
	"""
	@Params: 
	IDG: IDG of the paper 
	p: paper whose neighbours we need to check
	depth_dict: Dict with all the depth of the papers in the IDG
	@Returns:
	The neighbour which has the most depth and has been visited.
	"""
	edge_list = list(IDG.out_edges(nbunch = [p]))
	max_depth = -1
	ancestor_paper = EMPTY
	for e in edge_list:
		if depth_dict[e[1]] > max_depth:
			max_depth = depth_dict[e[1]]
			ancestor_paper = e[1]
	return ancestor_paper

def remove_edges_except(paper, ancestor_paper , IDG):
	"""
	@Params: 
	IDG: IDG of the paper 
	paper: paper whose neighbours we need to check
	ancestor_paper: The ancestor with whom we need to preserve the edges
	@Returns:
	The IDG with all but the given ancestor's edge removed
	"""
	edge_list = list(IDG.out_edges(nbunch = paper))
	for e in edge_list:
		if e[1] != ancestor_paper:
			IDG.remove_edge(*e) 
	return IDG


def convert_IDG_to_IDT(IDG):
	visited = set()
	not_visited = set(IDG.nodes())
	not_visited.discard(paper)
	visited.add(paper)
	depth_dict[paper] = 0
	cur_depth = 1
	while(len(not_visited) > 0):
		cur_visit_set = set()
		for p in not_visited:
			if all_edges_in_visited(IDG,p,visited):
				ancestor_paper = get_parent_with_most_depth(depth_dict , IDG , p)
				IDG = remove_edges_except(p , ancestor_paper , IDG)
				cur_visit_set.add(p)
				depth_dict[p] = cur_depth
		visited = visited.union(cur_visit_set)
		for p in cur_visit_set:
			not_visited.discard(p)
		cur_depth += 1

	branch = []
	total_branches = []
	get_depth_of_each_branch(H , paper , 0, branch , total_branches)
	# IDT_ = IDG.reverse(copy = False)

	return IDT_, total_branches

def get_max_idi(num_citations):
	"""
	@Params: 
	num_citations: Number of citations of a paper whose max IDI is to be calculated 
	@Returns:
	The max IDI of the paper
	"""
	return (num_citations - int((num_citations - 1) / 2)) * (float(1 + int((num_citations - 1) / 2)))

def get_min_idi(num_citations):
	"""
	@Params: 
	num_citations: Number of citations of a paper whose min IDI is to be calculated 
	@Returns:
	The min IDI of the paper
	"""
	return num_citations 

def get_nid(idi, num_citations):
	if num_citations > 3:
		max_idi = get_max_idi(num_citations)
		min_idi = get_min_idi(num_citations)
		ideal_idi = min_idi
		nid = abs(idi - ideal_idi) / float(abs(max_idi - min_idi))
		return nid
	return 0.0

def get_idi_till_year(IDT, year, PAPER_YEAR_DICT):
	"""
	@Params: 
	IDT: IDT of the paper 
	year: Year untill which IDI is to be calculated. Nodes will be removed from the IDT accordingly.
	PAPER_YEAR_DICT: Dictionary with paper ids as keys and year of publication as values.
	@Returns:
	The IDI of the paper. Max and min IDI corresponding to the number of citations are also returned.
	"""

	IDT = get_idt_till_year(IDT, year, PAPER_YEAR_DICT)
	

	if len(IDT.edges()) == 0:
		return 0, 0, 0, 0

	nodes = list(IDT.nodes())
	num_citations = len(nodes) - 1
	cur_paper = None
	for v in nodes:
		out_edges = IDT.out_edges(nbunch = [v])
		if len(out_edges) == 0:
			cur_paper = v
			break

	if cur_paper == None:
		print('No root node in given IDT')
		return 0, 0, 0, 0

	leaf_nodes = []
	for v in nodes:
		in_edges = IDT.in_edges(nbunch = [v])
		if len(in_edges) == 0:
			leaf_nodes.append(v)
	v_count = {i : 0 for i in nodes}
	for v in leaf_nodes:
		paths = list(nx.all_shortest_paths(IDT , source = v , target = cur_paper))
		for path in paths:
			for e in path:
				v_count[e] += 1

	idi = 0
	for i in nodes:
		if i != cur_paper:
			idi += v_count[i]


	return idi, get_max_idi(num_citations), get_min_idi(num_citations), get_nid(idi, num_citations)

def get_idt_till_year(IDT, year, PAPER_YEAR_DICT):
	"""
	@Params: 
	IDT: IDT of the paper 
	year: Year untill which IDI is to be calculated. Nodes will be removed from the IDT accordingly.
	PAPER_YEAR_DICT: Dictionary with paper ids as keys and year of publication as values.
	@Returns:
	The pruned IDT of the paper. Papers (nodes) published after 'year' are removed from the IDT.
	"""
	nodes = list(IDT.nodes())
	cur_paper = None
	for v in nodes:
		out_edges = IDT.out_edges(nbunch = [v])
		if len(out_edges) == 0:
			cur_paper = v
			break
			
	if cur_paper == None:
		print('No root node in given IDT')
		exit(1)
	
	
	induced_graph = set()
	induced_graph_list = list(IDT.nodes())

	for p in induced_graph_list:
		if p in PAPER_YEAR_DICT and int(PAPER_YEAR_DICT[p]) <= year:
			induced_graph.add(p)


	induced_graph.add(cur_paper)
	H = IDT.subgraph(induced_graph)

	return H

def get_depth_of_each_branch(G , paper, cur_depth, branch, total_branches):
	e_list = list(G.in_edges(nbunch = [paper]))
	branch.append(paper)
	if len(e_list) == 0:
		total_branches.append(branch)
		return
	for e in e_list:
		get_depth_of_each_branch(G , e[0] , 1 + cur_depth , branch[:] ,total_branches)
