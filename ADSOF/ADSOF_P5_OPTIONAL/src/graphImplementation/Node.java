package graphImplementation;

import java.util.Collection;
import java.util.List;

import exceptions.GraphAlreadyAdded;

/**
 * 
 * Class for the creation and manipulation of the nodes of the graph.
 *
 * @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
 *
 * @param <T> the generic type
 */
public class Node<T> implements Comparable<Node<T>>{
	
	/** The counterid. */
	private static int counterid = 0;
	
	/** The id. */
	private int id;
	
	/** The name. */
	private T name;
	
	/** The graph associated. */
	private Graph<T, ?> graph = null;
	
	/**
	 * Instantiates a new node.
	 *
	 * @param argument the argument
	 */
	public Node(T argument) {
		this.name = argument;
		id = counterid;
		counterid += 1;
	}
	
	/**
	 * Sets the graph associated to the node.
	 *
	 * @param the graph
	 * @return true, if successful
	 * @throws GraphAlreadyAdded if the graph is already added
	 */
	protected boolean setGraph(Graph<T, ?> graph) throws GraphAlreadyAdded {
		if(this.graph != null) {
			throw new GraphAlreadyAdded(this.graph, graph, this);
		}
		this.graph = graph;
		return true;
	}

	/**
	 * Compare to another node.
	 *
	 * @param o the node
	 * @return 0 if equal
	 */
	@Override
	public int compareTo(Node<T> o) {
		return this.id - o.id;
	}
	
	/**
	 * Hash code.
	 *
	 * @return the id
	 */
	@Override
	public int hashCode() {
		return id;
	}
	
	/**
	 * Check if two nodes are equal.
	 *
	 * @param o the object
	 * @return true, if successful
	 */
	@SuppressWarnings("unchecked")
	@Override
	public boolean equals(Object o) {
		if(!(o instanceof Node<?>)) return false;
		if(this.compareTo((Node<T>)o) == 0) 
			return true;
		
		return false;
	}
	
	/**
	 * To string.
	 *
	 * @return the string
	 */
	@Override
	public String toString() {
		return id + " " + "["+name.toString()+"]";
	}
	
	/**
	 * Gets a list of the edge values.
	 *
	 * @param n2 a node
	 * @return the edge values
	 */
	public List<?> getEdgeValues(Node<T> n2) {
		List<?> values = graph.getEdgeValuesBetween(this, n2);
		return values;
	}
	
	/**
	 * Get the collection of nodes which is directly connected in associated graph.
	 *
	 * @return the collection
	 */
	public Collection<Node<T>> neighbours() {
		return graph.getDirectlyConnected(this);
	}
	
	
	/**
	 * Checks if a Node is connected to another.
	 *
	 * @param n2 the n 2
	 * @return true, if they are connected
	 */
	public boolean isConnectedTo(Node<T> n2) {
		return !(graph.getEdgesBetween(this, n2).isEmpty());

	}
	
	/**
	 * Checks if a Node is connected to another by its value.
	 *
	 * @param valuetarget the value
	 * @return true, if they are connected
	 */
	public boolean isConnectedTo(T valuetarget) {
		Node<T> target = graph.getNodeByValue(valuetarget);
		if(target == null) return false;
		return !(graph.getEdgesBetween(this, target).isEmpty());

	}
	
	/**
	 * Gets the value.
	 *
	 * @return the value
	 */
	public T getValue() {
		return name;
	}
	
	/**
	 * Sets the value.
	 *
	 * @param i the new value
	 */
	public void setValue(T i) {
		this.name = i;
		return;
	}

	/**
	 * Gets the id.
	 *
	 * @return the id
	 */
	protected int getId() {
		return id;
	}

	
}
