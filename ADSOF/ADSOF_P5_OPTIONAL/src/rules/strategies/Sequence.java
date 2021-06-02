/**
 * 
 */
package rules.strategies;

import java.util.Collection;

import rules.Rule;

/**
 * The Class Sequence.
 *
 * @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
 * 
 * @param <T> the generic type
 */
public class Sequence<T> implements RuleStrategy<T>{

	/**
	 * Process rules in sequence.
	 *
	 * @param setofrules the set of rules
	 * @param objectstoapply the objects to apply
	 */
	@Override
	public void processRules(Collection<Rule<T>> setofrules, Collection<T> objectstoapply) {
		for(Rule<T> myRule: setofrules) 
			objectstoapply.stream().filter(myRule.getWhen()).forEach(myRule.getExec());	
	}

	

	

}
