package units;

import magnitude.exceptions.UnknownUnitException;
import magnitude.exceptions.DifferentQuantityException;
import magnitude.exceptions.QuantityException;
import metricSystems.IMetricSystem;

/**
*
* Class for implementing interface IPhysicalUnit
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*/
public class PhysicalUnit implements IPhysicalUnit{
	
	/** Unit type. */
	Quantity type;
	
	/** Base. */
	double base;
	
	/** Abbreviation. */
	String abbrev;
	
	/** System. */
	IMetricSystem system;
	
	/**
	 * Instantiates a new unit.
	 *
	 * @param type
	 * @param base
	 * @param abbreviation
	 */
	public PhysicalUnit(Quantity type, double base, String abbv) {
		this.type = type;
		this.base = base;	
		this.abbrev = abbv;
	}
	
	/**
	 * Necessary because it cannot be received in the constructor as it has not been created yet in the MetricSystemclass.
	 *
	 * @param new metric system
	 */
	public void setMetricSystem(IMetricSystem system) {
		this.system = system;
	}

	/**
	 * For knowing  if the unit can be transformed to another one that is passed as a parameter.
	 *
	 * @param IPhysicalUnit
	 * @return true, if successful
	 */
	@Override
	public boolean canTransformTo(IPhysicalUnit u) {
		if(this.getQuantity() != u.getQuantity()) return false;
		if(this.getMetricSystem() != u.getMetricSystem()) return false;
		
		return true;
	}

	/**
	 * Transform to the new unit.
	 *
	 * @param base
	 * @param IPhysicalUnit
	 * @return the final unit conversion
	 * @throws QuantityException if different quantities or unknown units
	 */
	@Override
	public double transformTo(double d, IPhysicalUnit u) throws QuantityException {
		if(this.canTransformTo(u) == false) throw new DifferentQuantityException(this, u);
		if(this.getClass() != u.getClass()) throw new UnknownUnitException(this, u);
		
		return d*this.base/((PhysicalUnit)u).base;
	}

	/**
	 * Gets the quantity.
	 *
	 * @return the quantity
	 */
	@Override
	public Quantity getQuantity() {
		return type;
	}

	/**
	 * Abbreviation.
	 *
	 * @return the string of abbreviation
	 */
	@Override
	public String abbrev() {
		return abbrev;
	}
	
	/**
	 * ToString.
	 *
	 * @return the string
	 */
	@Override
	public String toString() {
		return abbrev + " " + type;
	}

	/**
	 * Gets the metric system.
	 *
	 * @return the metric system
	 */
	@Override
	public IMetricSystem getMetricSystem() {
		return system;
	}
	
	
}
