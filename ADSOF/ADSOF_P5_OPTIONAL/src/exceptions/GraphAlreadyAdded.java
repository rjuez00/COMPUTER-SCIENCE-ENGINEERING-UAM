package exceptions;

import graphImplementation.*;

/**
 * Exception for knowing if a graph has been already added.
 * 
 * @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
 * 
 */

@SuppressWarnings("serial")
public class GraphAlreadyAdded extends Exception {
	
	/** Graph one. */
	Graph<?,?> to;
	
	/** Graph two. */
	Graph<?,?> from;
	
	/** The node. */
	Node<?> node;
	
	/**
	 * Instantiates a new exception.
	 *
	 * @param from Graph one
	 * @param to Graph two
	 * @param node the node
	 */
	public GraphAlreadyAdded(Graph<?,?> from, Graph<?,?> to, Node<?> node) {
		this.to = to;
		this.from = from;
		this.node = node;
	}

	/**
	 * To string.
	 *
	 * @return the string
	 */
	public String toString() {
		return "Can't add " + node + " to " + to + " because is already part of " + from;
	}
}
