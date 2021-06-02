/**
 * 
 */
package graphImplementation;

/**
 * Class for the creation and manipulation of the edges of the graph.
 *
 * @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
 * 	
 * @param <A> the generic type of nodes it connects
 * @param <B> the generic type of edges
 */
public class Edge<A, B> {
	
	/** The source node. */
	private Node<A> source;
	
	/** The target node. */
	private Node<A> target;
	
	/** The name of the edge. */
	private B name;
	
	/**
	 * Instantiates a new edge.
	 *
	 * @param source the source node
	 * @param target the target node
	 * @param name the name of the edge
	 */
	public Edge(Node<A> source, Node<A> target, B name) {
		this.source = source;
		this.target = target;
		this.name = name;
	}
	
	/**
	 * Gets the source.
	 *
	 * @return the source
	 */
	protected Node<A> getSource(){
		return source;
	}
	
	/**
	 * Gets the target.
	 *
	 * @return the target
	 */
	protected Node<A> getTarget(){
		return target;
	}
	
	/**
	 * Gets the value.
	 *
	 * @return the value
	 */
	protected B getValue() {
		return name;
	}
	
	/**
	 * Check if two edges are equal (same name).
	 *
	 * @param o the o
	 * @return true, if successful
	 */
	@Override
	public boolean equals(Object o) {
		if(o instanceof Edge<?, ?>) return false;
		return name.equals(((Edge<?,?>)o).name);
		
	}
	
	/**
	 * To string.
	 *
	 * @return the string
	 */
	public String toString() {
		return "( " + this.source.getId() + " --" + this.name +"--> "+ this.target.getId() + " )";
	}

}
