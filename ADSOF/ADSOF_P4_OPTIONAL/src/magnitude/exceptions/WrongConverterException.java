package magnitude.exceptions;

import metricSystems.IMetricSystemConverter;
import units.IPhysicalUnit;

/**
*
* Class for declaring a new type of Unknown Unit Exception.
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*/
@SuppressWarnings("serial")
public class WrongConverterException extends UnknownUnitException {
	
	/** The converter. */
	IMetricSystemConverter converter;
	
	/**
	 * Instantiates a new wrong converter exception.
	 *
	 * @param first unit type
	 * @param second unit type
	 * @param converter
	 */
	public WrongConverterException(IPhysicalUnit firstunit, IPhysicalUnit secondunit, IMetricSystemConverter converter) {
		super(firstunit, secondunit);
		this.converter = converter;
	}

	/**
	 * ToString.
	 *
	 * @return the string
	 */
	public String toString() {
		return converter.sourceSystem() + " converts to " + converter.targetSystem() + " and you're trying to convert " + super.firstunit + " to " + secondunit;
	}
	
}
