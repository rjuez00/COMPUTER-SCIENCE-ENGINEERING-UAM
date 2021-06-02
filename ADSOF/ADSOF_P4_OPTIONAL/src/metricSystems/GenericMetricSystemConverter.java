/**
 * 
 */
package metricSystems;

import magnitude.IMagnitude;
import magnitude.Magnitude;
import magnitude.exceptions.QuantityException;
import magnitude.exceptions.UnknownUnitException;
import magnitude.exceptions.WrongConverterException;
import units.IPhysicalUnit;

/**
*
* Class for doing conversions implementing IMetricSystemConverter.
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*/
public class GenericMetricSystemConverter implements IMetricSystemConverter {
	
	/** Source system. */
	private IMetricSystem source;
	
	/** Target system. */
	private IMetricSystem target;
	
	/** Ratio. */
	private double ratio;
	
	/**
	 * Instantiates a new GenericMetricSystemConverter.
	 *
	 * @param source
	 * @param target
	 * @param ratio
	 */
	public GenericMetricSystemConverter(IMetricSystem source, IMetricSystem target, double ratio) {
		this.source = source;
		this.target = target;
		this.ratio = ratio;
	}

	/**
	 * Source getter.
	 *
	 * @return the source
	 */
	@Override
	public IMetricSystem sourceSystem() {
		return source;
	}

	/**
	 * Target getter.
	 *
	 * @return the target
	 */
	@Override
	public IMetricSystem targetSystem() {
		return target;
	}

	/**
	 * Converts into the specified unit if possible.
	 *
	 * @param unit to be transformed
	 * @param unit to transform
	 * @return the new magnitude
	 * @throws UnknownUnitException if unknown unit or wrong converter
	 */
	@Override
	public IMagnitude transformTo(IMagnitude from, IPhysicalUnit to) throws UnknownUnitException{
		if(from.getUnit().getMetricSystem() != this.sourceSystem() || to.getMetricSystem() != this.targetSystem()) throw new WrongConverterException(from.getUnit(), to, this);
		double result = 0;
		try {
			result = this.targetSystem().base().transformTo(from.transformTo(this.sourceSystem().base()).getValue() * ratio, to);
		} catch (QuantityException e) {
			if(e.getClass() == UnknownUnitException.class) throw (UnknownUnitException)e;
			System.out.println(e);
			return null;
		}
		
		
		return new Magnitude(result, to);
	}

	/**
	 * Reverse method.
	 *
	 * @return a new conversion in reverse
	 */
	@Override
	public IMetricSystemConverter reverse() {
		return new GenericMetricSystemConverter(target, source, 1/ratio);			
	}

}
