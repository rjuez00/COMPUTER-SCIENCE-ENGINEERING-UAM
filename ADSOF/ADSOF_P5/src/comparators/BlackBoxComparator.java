/**
 * 
 */
package comparators;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.function.Predicate;

import graphImplementation.ConstrainedGraph;
import graphImplementation.Node;

/**
 * The class BlackBoxComparator for comparing fulfillment of properties of two constrained graphs.
 * 
 * @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
 *
 * @param <A> the generic type
 * @param <B> the generic type
 */

public class BlackBoxComparator<A, B> implements Comparator<ConstrainedGraph<A,B>>{

	/** The universal condition. */
	ArrayList<Predicate<Node<A>>> universalcond = new ArrayList<>();
	
	/** The existential condition. */
	ArrayList<Predicate<Node<A>>> existentialcond = new ArrayList<>();
	
	/** The unitary condition. */
	ArrayList<Predicate<Node<A>>> unitarycond = new ArrayList<>();

	/**
	 * Instantiates a new black box comparator.
	 */
	public BlackBoxComparator() {
	}

	/**
	 * Adds the criteria.
	 *
	 * @param criteria the criteria
	 * @param cond the predicate of nodes
	 * @return the black box comparator
	 */
	public BlackBoxComparator<A,B> addCriteria(Criteria criteria, Predicate<Node<A>> cond) {
		if(criteria == Criteria.EXISTENTIAL) existentialcond.add(cond);
		else if(criteria == Criteria.UNITARY) unitarycond.add(cond);
		else if(criteria == Criteria.UNIVERSAL) universalcond.add(cond);

		return this;
	}

	/**
	 * Compare the two constrained graphs.
	 *
	 * @param o1 first constrained graph
	 * @param o2 second constrained graph
	 * @return counter positive if o1 greater than o2 and negative if o1 less than o2
	 */
	@Override
	public int compare(ConstrainedGraph<A, B> o1, ConstrainedGraph<A, B> o2) {
		int counter = 0;


		for(Predicate<Node<A>> myCond: universalcond) {
			if(o2.forAll(myCond) == true) counter-=1;
			if(o1.forAll(myCond) == true) counter+=1;
		}
		
		for(Predicate<Node<A>> myCond: existentialcond) {
			if(o2.exists(myCond) == true) counter-=1;
			if(o1.exists(myCond) == true) counter+=1;
		}
		
		for(Predicate<Node<A>> myCond: unitarycond) {
			if(o2.one(myCond) == true) counter-=1;
			if(o1.one(myCond) == true) counter+=1;
		}

		
		return counter;
	}

}
