package metricSystems;

import java.util.ArrayList;
import java.util.Collection;
import units.IPhysicalUnit;

/**
*
* Abstract class for implementing interface IMetricSystem.
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*/
public abstract class AbstractMetricSystem implements IMetricSystem{
	
	/** The converters. */
	private static ArrayList<IMetricSystemConverter> converters = new ArrayList<>();
	
	/** Base. */
	private IPhysicalUnit base;
	
	/** Collection of units. */
	private Collection<IPhysicalUnit> units;
	
	/**
	 * Instantiates a new abstract metric system.
	 *
	 * @param base
	 * @param the units
	 */
	protected AbstractMetricSystem(IPhysicalUnit base, Collection<IPhysicalUnit> units){
		if(units.contains(base) == false) {
			units.add(base);
		}
		this.base = base;
		this.units = units;
	}

	/**
	 * Base getter.
	 *
	 * @return base
	 */
	@Override
	public IPhysicalUnit base() {
		return base;
	}

	/**
	 * Units getter.
	 *
	 * @return the collection
	 */
	@Override
	public Collection<IPhysicalUnit> units() {
		return units;
	}
	
	/**
	 * Gets the converter.
	 *
	 * @param IMetricSystem
	 * @return the converter(IMetricSystemConverter)
	 */
	public IMetricSystemConverter getConverter(IMetricSystem to) {
		for(IMetricSystemConverter converter: AbstractMetricSystem.converters) {
			if(converter.targetSystem() == to && converter.sourceSystem() == this) {
				return converter;
			}
		}
		return null;
	}
	
	/**
	 * Registers the converter.
	 *
	 * @param register the register
	 */
	public static void registerConverter(IMetricSystemConverter register) {
		if(converters.contains(register)) return;
		converters.add(register);
		if(converters.contains(register.reverse())) return;
		converters.add(register.reverse());
	}
}
