package rules;

import java.util.ArrayList;
import java.util.Collection;

/**
 * The Class RuleSet.
 *
 * @param <T> the generic type
 */
public class RuleSet<T> {
	
	/** The set of rules. */
	private ArrayList<Rule<T>> setofrules = new ArrayList<>();
	
	/** The collection of T's. */
	private Collection<T> collectionofTs;
	
	/**
	 * Gets the set of rules.
	 *
	 * @return the set of rules
	 */
	public ArrayList<Rule<T>> getSetofrules() {
		return setofrules;
	}
	
	/**
	 * Gets the collection of T's.
	 *
	 * @return the collectionofTs
	 */
	public Collection<T> getCollectionofTs() {
		return collectionofTs;
	}
	
	/**
	 * Adds a Rule to the RuleSet.
	 *
	 * @param exec the Rule
	 * @return the rule set
	 */
	public RuleSet<T> add(Rule<T> exec) {
		setofrules.add(exec);
		return this;
	}
	
	/**
	 * Sets the Exec context.
	 *
	 * @param collectionofTs the new exec context
	 */
	public void setExecContext(Collection<T> collectionofTs) {
		this.collectionofTs = collectionofTs;
	}
	
	/**
	 * Process all the Rules of the RuleSet.
	 */
	public void process() {
		for(Rule<T> myRule: this.setofrules) 
			collectionofTs.stream().filter(myRule.getWhen()).forEach(myRule.getExec());		
	}

}
