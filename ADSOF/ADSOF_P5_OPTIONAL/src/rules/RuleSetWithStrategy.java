package rules;

import rules.strategies.RuleStrategy;

/**
 * The Class RuleSetWithStrategy.
 * 
 * @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
 *
 * @param <T> the generic type
 */
public class RuleSetWithStrategy<T> extends RuleSet<T>{
	
	/** The Rule strategy. */
	private RuleStrategy<T> strategy;

	/**
	 * Instantiates a new rule set with strategy.
	 *
	 * @param strategy the Rule strategy
	 */
	public RuleSetWithStrategy(RuleStrategy<T> strategy) {
		this.strategy = strategy;
	
	}
	
	
	
	/**
	 * Process all the Set of Rules.
	 */
	@Override
	public void process() {
		this.strategy.processRules(this.getSetofrules(), this.getCollectionofTs());
	}
			
		
}
