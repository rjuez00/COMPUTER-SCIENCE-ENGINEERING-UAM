/**
 * 
 */
package metricSystems.si.length.converters;

import metricSystems.GenericMetricSystemConverter;
import metricSystems.IMetricSystemConverter;
import metricSystems.imperial.length.ImperialLengthMetricSystem;
import metricSystems.si.length.SiLengthMetricSystem;

/**
*
* Class for declaring a conversion from SI length to Imperial length.
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*/
public class SiLength2ImperialConverter extends GenericMetricSystemConverter implements IMetricSystemConverter {

	/**
	 * @param source
	 * @param target
	 * @param conversion
	 */
	public SiLength2ImperialConverter() {
		super(SiLengthMetricSystem.SYSTEM, ImperialLengthMetricSystem.SYSTEM, 3.280839895);
		
	}

}
