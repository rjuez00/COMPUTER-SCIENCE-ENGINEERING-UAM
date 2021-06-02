/**
 * 
 */
package metricSystems;

import java.util.Collection;

import units.IPhysicalUnit;

/**
 * @author Rodrigo
 *
 */
public class CompositeMetricSystem extends AbstractMetricSystem {
	
	/**
	 * @param base
	 * @param units
	 */
	public CompositeMetricSystem(IPhysicalUnit base, Collection<IPhysicalUnit> units) {
		super(base, units);
	}

}
