package magnitude;

import magnitude.exceptions.*;
import metricSystems.IMetricSystemConverter;
import units.CompositeUnit;
import units.IPhysicalUnit;
import units.PhysicalUnit;

/**
*
* Class for implementing the interface IMagnitude.
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*/
public class Magnitude implements IMagnitude {
	
	/** Unit. */
	IPhysicalUnit unit;
	
	/** Quantity. */
	double quantity;

	/**
	 * Instantiates a new magnitude.
	 *
	 * @param quantity
	 * @param unit
	 */
	public Magnitude(double quantity, IPhysicalUnit unit) {
		this.quantity = quantity;
		this.unit = unit;
	}

	/**
	 * Adds two quantities of the same type.
	 *
	 * @param magnitude
	 * @return the magnitude added
	 * @throws QuantityException
	 */
	@Override
	public IMagnitude add(IMagnitude m) throws QuantityException {
		//we don't do error control because the transformTo method does it for us
		this.quantity += m.transformTo(this.getUnit()).getValue();

		return this;

	}

	/**
	 * Subtracts two quantities of the same type.
	 *
	 * @param magnitude
	 * @return the magnitude added
	 * @throws QuantityException
	 */
	@Override
	public IMagnitude subs(IMagnitude m) throws QuantityException {
		//we don't do error control because the transformTo method does it for us
		this.quantity -= m.transformTo(this.getUnit()).getValue();

		return this;
	}

	/**
	 * Transforms the unit using a registered converter.
	 *
	 * @param unit
	 * @return the new magnitude
	 * @throws QuantityException if unknown unit or different quantity
	 */
	@Override
	public IMagnitude transformTo(IPhysicalUnit c) throws QuantityException {
		IMetricSystemConverter converter;
		if (this.getUnit().getQuantity() != c.getQuantity())
			throw new DifferentQuantityException(this.getUnit(), c);
		
		if(c.getClass() != this.getUnit().getClass()) throw new UnknownUnitException(c, this.getUnit()); //if trying to convert unit to composite or viceversa
		else if(c.getClass() == CompositeUnit.class || (c.getClass() == PhysicalUnit.class && (this.getUnit().getMetricSystem() == c.getMetricSystem()))) 
			return new Magnitude(this.getUnit().transformTo(this.getValue(), c), c);	
				
		else {
			if ((converter = this.getUnit().getMetricSystem().getConverter(c.getMetricSystem())) == null) 
				throw new UnknownUnitException(this.getUnit(),c);
			
			else return converter.transformTo(this, c);
		}
		
	}

	/**
	 * Gets the unit.
	 *
	 * @return the unit
	 */
	@Override
	public IPhysicalUnit getUnit() {
		return this.unit;
	}

	/**
	 * Gets the value.
	 *
	 * @return the value
	 */
	@Override
	public double getValue() {
		return this.quantity;
	}
	
	/**
	 * ToString.
	 *
	 * @return the string
	 */
	@Override
	public String toString() {
		return Double.toString(this.getValue()) + " [" + this.getUnit() + "]";
	}
}
