/**
 * 
 */
package rules.strategies;

import java.util.Collection;

import rules.Rule;

/**
 * The Class to process rules as long as possible.
 *
 * @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
 * 
 * @param <T> the generic type
 */
public class AsLongAsPossible<T> implements RuleStrategy<T>{

	/**
	 * Process rules as long as possible.
	 *
	 * @param setofrules the set of rules
	 * @param objectstoapply the objects to apply
	 */
	@Override
	public void processRules(Collection<Rule<T>> setofrules, Collection<T> objectstoapply) {
		for(Rule<T> myRule : setofrules) 
			for(T myT: objectstoapply)
				while(myRule.getWhen().test(myT) == true) 
					myRule.getExec().accept(myT);	
				
		
	}

	

	

}
	

