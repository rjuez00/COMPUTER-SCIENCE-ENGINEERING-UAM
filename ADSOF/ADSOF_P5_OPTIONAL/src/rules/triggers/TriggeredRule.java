package rules.triggers;

import rules.Rule;

/**
 * TriggeredRule which has similar functionality to rule but observing an object
 *
 * @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
 * 
 * @param <T> the generic type
 */
public class TriggeredRule<T extends Observed<T>> extends Rule<T> {
	
	
	/**
	 * creates a rule with name of the triggered rule
	 * @param name of the trigger
	 */
	public TriggeredRule(String name) {
		super(name, null);
	}
	
	/**
	 * returns a triggered rule with the name specified
	 * @param <T> must comply with the observed interface
	 * @param name of the rule 
	 * @return the triggeredrule
	 */
	public static <T extends Observed<T>> TriggeredRule<T> trigRule(String name) {
		return new TriggeredRule<T>(name);
	}
	/**
	 * applies a triggered rule to the observed (hence the extends observed) of the type
	 * @param appliedTo the object to apply must comply with observed interface
	 * @param desc the description of the rule
	 * @return the rule itself according to the fluent design
	 */
	public Rule<T> trigger(T appliedTo, String desc) {
		super.setDescription(desc);
		appliedTo.addTriggerer(this);
		return this;
	}

}
