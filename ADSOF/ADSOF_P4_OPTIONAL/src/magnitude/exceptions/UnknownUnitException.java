/**
 * 
 */
package magnitude.exceptions;

import units.IPhysicalUnit;

/**
*
* Class for declaring a new type of Quantity Exception.
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*/
@SuppressWarnings("serial")
public class UnknownUnitException extends QuantityException {
	
	/** The first unit type. */
	IPhysicalUnit firstunit;
	
	/** The second unit type. */
	IPhysicalUnit secondunit;

	/**
	 * Instantiates a new unknown unit exception.
	 *
	 * @param first unit type
	 * @param second unit type
	 */
	public UnknownUnitException( IPhysicalUnit firstunit, IPhysicalUnit secondunit) {
		super(firstunit, secondunit);
		this.firstunit = firstunit;
		this.secondunit = secondunit;

	}
	
	/**
	 * ToString.
	 *
	 * @return the string
	 */
	@Override
	public String toString() {
		return "Cannot transform " + firstunit + " to " + secondunit;
	}
	

}
