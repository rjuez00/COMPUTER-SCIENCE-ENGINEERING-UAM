package testers;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import comparators.BlackBoxComparator;
import comparators.Criteria;
import graphImplementation.ConstrainedGraph;
import graphImplementation.Node;

public class Tester2 {

	public static void main(String[] args) {
		ConstrainedGraph<Integer, Integer> g = new ConstrainedGraph<Integer, Integer>();
		Node<Integer> n1 = new Node<Integer>(1);
		Node<Integer> n2 = new Node<Integer>(2);
		Node<Integer> n3 = new Node<Integer>(3);
		g.addAll(Arrays.asList(n1, n2, n3));
		g.connect(n1, 1, n2);
		g.connect(n1, 7, n3);
		g.connect(n2, 1, n3);
		System.out.println("All nodes of g connected with n3? "+g.forAll(n -> n.equals(n3) || n.isConnectedTo(n3))); // true
		System.out.println("Is there exactly one node connected to n2? "+g.one( n -> n.isConnectedTo(n2))); // true
		System.out.println("Is there at least one node of g connected to n2? "+g.exists( n -> n.isConnectedTo(n2))); // (*) true
		
		
		
		g.exists( n -> n.getValue().equals(89)); // Not satisfied: Optional is null
		g.getWitness().ifPresent( w -> System.out.println("Witness 1 = "+g.getWitness().get()));
		g.exists( n -> n.isConnectedTo(n2)); // Satisfied: Optional has value
		g.getWitness().ifPresent( w -> System.out.println("Witness 2 = "+g.getWitness().get()));

		
		
		System.out.println("\n");
		
		ConstrainedGraph<Integer, Integer> g1 = new ConstrainedGraph<Integer, Integer>();
		g1.addAll(Arrays.asList(new Node<Integer>(4)));
		
		BlackBoxComparator<Integer, Integer> bbc = new BlackBoxComparator<Integer, Integer>();
		bbc.addCriteria( Criteria.EXISTENTIAL, n -> n.isConnectedTo(1)). // corrected
		addCriteria( Criteria.UNITARY, n -> n.neighbours().isEmpty()).
		addCriteria( Criteria.UNIVERSAL, n -> n.getValue().equals(4));
		


		List<ConstrainedGraph<Integer, Integer>> cgs = Arrays.asList(g, g1);
		Collections.sort(cgs, bbc); // We use the comparator to order a list with two graphs
		System.out.println(cgs); // prints g (satisfies the 2nd property) and then g1 (satisfies the 2nd and 3rd) (corrected)
	}

}
