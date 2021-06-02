package rules.strategies;

import java.util.Collection;

import rules.Rule;

/**
 * The Interface RuleStrategy.
 * 
 * @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
 *
 * @param <T> the generic type
 */
public interface RuleStrategy<T> {
	
	/**
	 * Process the rules.
	 *
	 * @param setofrules the set of rules
	 * @param objectstoapply the objects to apply
	 */
	void processRules(Collection<Rule<T>> setofrules, Collection<T> objectstoapply);
}
