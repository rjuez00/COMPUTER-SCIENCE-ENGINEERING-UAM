package graphImplementation;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Set;

import exceptions.GraphAlreadyAdded;

/**
 * Class for the creation and manipulation of a graph.
 * 
 * @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
 *
 * @param <A> the generic type
 * @param <B> the generic type
 */
public class Graph<A, B> implements Collection<Node<A>>{
	
	/** The nodes list. Implemented this way to preserve the order in which they are inserted */
	ArrayList<Node<A>> nodes = new ArrayList<>(); 
	
	/** The edges list. */
	ArrayList<Edge<A,B>> edges = new ArrayList<>(); 
	
	

	/**
	 * Size of the graph.
	 *
	 * @return the size
	 */
	@Override
	public int size() {
		return nodes.size();
	}

	/**
	 * Checks if Graph is empty.
	 *
	 * @return true, if is empty
	 */
	@Override
	public boolean isEmpty() {
		if(nodes.isEmpty()==true) return true;
		return false;
	}

	/**
	 * Checks if graph contains the node.
	 *
	 * @param o the node
	 * @return true, if it is contained
	 */
	@Override
	public boolean contains(Object o) {
		if(!(o instanceof Node<?>)) return false;
		return nodes.contains(o);
	}

	/**
	 * Iterator.
	 *
	 * @return the iterator
	 */
	@Override
	public Iterator<Node<A>> iterator() {
		return this.nodes.iterator();
	}

	/**
	 * Nodes of the graph to array.
	 *
	 * @return the Object type array
	 */
	@Override
	public Object[] toArray() {
		return nodes.toArray();
	}

	/**
	 * To array.
	 *
	 * @param <T> the generic type
	 * @param a the node
	 * @return the array
	 */
	@Override
	public <T> T[] toArray(T[] a) {
		return nodes.toArray(a);
	}

	/**
	 * Adds the node to the graph.
	 *
	 * @param e the node
	 * @return true, if successful
	 */
	@Override
	public boolean add(Node<A> e) {
		if(nodes.contains(e)) return false;
		try {
			e.setGraph(this);
		} catch (GraphAlreadyAdded e1) {
			System.out.println(e1);
			e1.printStackTrace();
		}
		nodes.add(e);
		return true;
	}

	/**
	 * Removes the node from the graph.
	 *
	 * @param o the node
	 * @return true, if successful
	 */
	@Override
	public boolean remove(Object o) {
		if(!(o instanceof Node<?>)) return false;        

		for(Edge<A,B> myEdge: edges) {
			if(myEdge.getSource().equals(o) == true) edges.remove(myEdge);
			else if(myEdge.getTarget().equals(o) == true) edges.remove(myEdge);
		}

		if(nodes.contains(o)) {
			nodes.remove(o);
			return true;
		}
		return false;
	}

	/**
	 * Check if a graph contains the collection of nodes.
	 *
	 * @param c the collection of nodes
	 * @return true, if successful
	 */
	@Override
	public boolean containsAll(Collection<?> c) {
		for(Object aux: c) {
			if(this.contains(aux));
			else return false;	
		}
		
		return true;
	}

	/**
	 * Adds all the collection of nodes to the graph.
	 *
	 * @param c the collection of nodes
	 * @return false, if successful
	 */
	@Override
	public boolean addAll(Collection<? extends Node<A>> c) {
		for(Node<A> aux : c) {
			this.add(aux);
		}
		return false;
	}

	/**
	 * Removes all the nodes of the collection.
	 *
	 * @param c the collection
	 * @return true, if successful
	 */
	@Override
	public boolean removeAll(Collection<?> c) {
		for(Object aux: c) 
			if(this.contains(aux)) 
				this.remove(aux);
			
		
		return true;
	}

	/**
	 * Retain all the nodes of the collection.
	 *
	 * @param c the collection
	 * @return true, if successful
	 */
	@Override
	public boolean retainAll(Collection<?> c) {
		for(Node<A> myNode: nodes) 
			if(c.contains(myNode) == false)
				nodes.remove(myNode);
				
		
		return true;
	}

	/**
	 * Clear.
	 */
	@Override
	public void clear() {
		nodes.clear();
		
	}

	/**
	 * Connect two nodes in a graph.
	 *
	 * @param from the initial node
	 * @param i the edge
	 * @param to the final node
	 */
	public void connect(Node<A> from, B i, Node<A> to) {
		if(this.contains(from) == false || this.contains(to) == false) return;
		edges.add( new Edge<A,B>(from, to, i) );
	}
	
	
	/**
	 * To string.
	 *
	 * @return the string
	 */
	public String toString() {
        StringBuilder bldString = new StringBuilder("\nNodes:\n");
        for(Node<A> myNode: nodes)
        	bldString.append(myNode + "\n");
    	bldString.append("Edges:");
    	for(Edge<A,B> myEdge: edges) {
    		bldString.append("\n");
        	bldString.append(myEdge);
    	}
    	return bldString.toString();
	}

	
	
	/**
	 * Gets the edges between two nodes.
	 *
	 * @param source the source node
	 * @param target the target node
	 * @return the set of edges between them
	 */
	protected Set<Edge<A,B>> getEdgesBetween(Node<A> source, Node<A> target){
		Set<Edge<A,B>> filter = new HashSet<>();
		for(Edge<A,B> myEdge: edges) {
			if(myEdge.getSource() == source && myEdge.getTarget() == target)
				filter.add(myEdge);
		}
		return filter;
	}
	
	/**
	 * Gets the edge values between two nodes.
	 *
	 * @param source the source node
	 * @param target the target node
	 * @return the edge values between them
	 */
	protected List<B> getEdgeValuesBetween(Node<A> source, Node<A> target){
		ArrayList<B> filter = new ArrayList<>();
		for(Edge<A,B> myEdge: edges) {
			if(myEdge.getSource() == source && myEdge.getTarget() == target)
				if(filter.contains(myEdge.getValue()) == false) filter.add(myEdge.getValue());
		}
		return filter;
	}
	
	/**
	 * Gets the directly connected nodes to the given.
	 *
	 * @param source the source node
	 * @return the directly connected set of nodes
	 */
	protected Set<Node<A>> getDirectlyConnected(Node<A> source){
		Set<Node<A>> filter = new HashSet<>();
		for(Edge<A,B> myEdge: edges) {
			if(myEdge.getSource() == source) {
				filter.add(myEdge.getTarget());
			}
		}
		return filter;
	}
	
	/**
	 * Gets the node by value.
	 *
	 * @param value the value
	 * @return the node
	 */
	protected Node<A> getNodeByValue(A value){
		for(Node<A> myNode: nodes) 
			if(myNode.getValue().equals(value))
				return myNode;
	
		return null;
	}

}
