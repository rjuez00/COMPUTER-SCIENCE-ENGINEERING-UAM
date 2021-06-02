/**
 * 
 */
package graphImplementation;

import java.util.Optional;
import java.util.function.Predicate;

/**
 * Class for the creation and manipulation of a constrained graph.
 *
 * @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
 * 
 * @param <A> the generic type
 * @param <B> the generic type
 */
public class ConstrainedGraph<A, B> extends Graph<A, B> {
	
	/** The witness node. */
	Node<A> witness;
	
	/**
	 * Instantiates a new constrained graph.
	 */
	public ConstrainedGraph () {
		super();
	}

	/**
	 * If all nodes satisfy the property.
	 *
	 * @param cond the Predicate of nodes
	 * @return true, if successful
	 */
	public Boolean forAll(Predicate<Node<A>> cond) {
		this.witness = null;
		for(Node<A> myNode: this) {
			if(cond.test(myNode) == false) {
				return false;
			}
		}	
		this.witness = this.iterator().next();
		return true;
	}

	/**
	 * If one node satisfies the property.
	 *
	 * @param cond the Predicate of nodes
	 * @return true, if successful
	 */
	public Boolean one(Predicate<Node<A>> cond) {
		this.witness = null;
		int counter=0;
		for(Node<A> myNode: this) {
			if(cond.test(myNode) == true) {
				this.witness = myNode;
				counter+=1;
			}
		}
		if(counter==1) return true;
		else {
			this.witness = null;
			return false; 
		}
	}

	/**
	 * If at least one node satisfies the property.
	 *
	 * @param cond the Predicate of nodes
	 * @return true, if successful
	 */
	public Boolean exists(Predicate<Node<A>> cond) {
		this.witness = null;
		for(Node<A> myNode: this) 
			if(cond.test(myNode) == true) {
				this.witness = myNode;
				return true;
			}
			
		return false;	
	}

	/**
	 * Gets the witness.
	 *
	 * @return the witness
	 */
	public Optional<Node<A>> getWitness() {
		if(witness == null) return Optional.empty();
		return Optional.of(witness);
	}


}
