import argparse
import GraphAnalyzeToolKit as GTK
from GraphManager import GraphManager as GM
import FileToPy as FTP
import random;
import matplotlib.pyplot as plt
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process file paths for graph data.')
    parser.add_argument('-d', '--data_folder', type=str, required=False, help="Path to the folder containing graph data files "+
                                                                            "\nExpected file names format:\n"+
                                                                            "- edges_file.txt: This file contains the edges of the graphs.\n"+
                                                                            "- edges_labels_file.txt: This file contains the edge labels of the graphs.\n"+
                                                                            "- graph_inds_file.txt: This file contains the graph indicators.\n"+
                                                                            "- graph_labels_file.txt: This file contains the graph labels.\n"+
                                                                            "- nodes_labels_file.txt: This file contains the node labels of the graphs.")
    parser.add_argument('-Uid', '--graph_ids', nargs='+', type=int, required=False, help='List of unknown graph IDs')
    parser.add_argument('-Kid', '--known_ids', type=int, required=False, help='size of known graph IDs list')
    parser.add_argument('-ct', '--generate_contingency_table', action='store_true', help='Generate contingency table')
    parser.add_argument('-n', '--iterations', type=int, default=1, help='Number of iterations')
    parser.add_argument('-gr','--generate_graphs',action='store_true',help='generate_graphs')
    parser.add_argument('-o', '--output_file', type=str, default='contingency_table.txt', help='Output file for contingency table')
    return parser.parse_args()

def main():
    args = parse_arguments()

    edges_file = os.path.join(args.data_folder, 'edges_file.txt')
    edges_labels_file = os.path.join(args.data_folder, 'edges_labels_file.txt')
    graph_inds_file = os.path.join(args.data_folder, 'graph_inds_file.txt')
    graph_labels_file = os.path.join(args.data_folder, 'graph_labels_file.txt')
    nodes_labels_file = os.path.join(args.data_folder, 'nodes_labels_file.txt')
        
    if not all(map(os.path.isfile, [edges_file, edges_labels_file, graph_inds_file, graph_labels_file, nodes_labels_file])):
        print("One or more required files are missing in the specified folder.")
        return
        
    INS = FTP.FileToPy(edges_file, edges_labels_file, graph_inds_file, graph_labels_file, nodes_labels_file)
    
    if args.generate_contingency_table:
        subgraph_list = GTK.generate_contingency_table(args.graph_ids, random.sample(range(1, INS.nbGraphe), args.known_ids), INS, args.iterations, args.output_file)
        print(f"Contingency table generated and saved in {args.output_file}")

    if args.generate_graphs:
        GM_instance = GM(edges_file, edges_labels_file, graph_inds_file, graph_labels_file, nodes_labels_file)
        total = GM_instance.get_max()
        print(total)
        gref = random.randint(1, total)  # Nombre à exclure
        random_nums = GM_instance.random_inator(gref)

        # maintenant on fait une série de résultats 
        result1 = GM_instance.diagMaker(gref, random_nums[0])
        result2 = GM_instance.diagMaker(gref, random_nums[1])
        result3 = GM_instance.diagMaker(gref, random_nums[2])

        output_folder = "plots"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        results = [result1, result2, result3]
        GM_instance.plot_and_save_results(gref, random_nums, results, output_folder)

        print(f"Graph generated and saved in {output_folder}")
    
    else:
        print("Option to generate contingency table not specified.")

if __name__ == "__main__":
    main()
