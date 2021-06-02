/**
 * 
 */
package magnitude.exceptions;

import units.IPhysicalUnit;

/**
*
* Class for declaring a new type of Exception.
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*/
@SuppressWarnings("serial")
public abstract class QuantityException  extends Exception {
	
	/** The first unit type. */
	IPhysicalUnit firstype;
	
	/** The second unit type. */
	IPhysicalUnit secondtype;

	/**
	 * Instantiates a new quantity exception.
	 *
	 * @param first unit type
	 * @param second unit type
	 */
	public QuantityException(IPhysicalUnit firstype, IPhysicalUnit secondtype) {
		super();
		this.firstype = firstype;
		this.secondtype = secondtype;
	}

	/**
	 * ToString.
	 *
	 * @return the string
	 */
	@Override
	public String toString() {
		return "Quantities " + secondtype +" and " + firstype + " are not compatible\n";
	}
	
	
	
	

}
