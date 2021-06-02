package metricSystems.si.time;

import java.util.Arrays;

import metricSystems.IMetricSystem;
import metricSystems.AbstractMetricSystem;
import units.PhysicalUnit;
import units.Quantity;

/**
*
* Class for implementing interface IMetricSystem in time measurements.
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*/
public class SiTimeMetricSystem extends AbstractMetricSystem implements IMetricSystem{
	
	/** Milliseconds. */
	static public PhysicalUnit MILLISECOND = new PhysicalUnit(Quantity.t, 0.001, "ms");
	
	/** Seconds. */
	static public PhysicalUnit SECOND = new PhysicalUnit(Quantity.t, 1, "s");
	
	/** Hours. */
	static public PhysicalUnit HOUR = new PhysicalUnit(Quantity.t, 3600, "h");

	/** Stores the unique object (Singleton pattern). */
	static public SiTimeMetricSystem SYSTEM = intermediateConstructor();
	
	/**
	 * Intermediate constructor.
	 *
	 * @return SiTimeMetricSystem
	 */
	private static SiTimeMetricSystem intermediateConstructor() {
		SiTimeMetricSystem systemtemp = new SiTimeMetricSystem();
		MILLISECOND.setMetricSystem(systemtemp);
		SECOND.setMetricSystem(systemtemp);
		HOUR.setMetricSystem(systemtemp);
		return systemtemp;
	}
	
	/**
	 * Instantiates a new SiTimeMetricSystem.
	 */
	private SiTimeMetricSystem(){
		super(SECOND,Arrays.asList(MILLISECOND, SECOND, HOUR));
	}


	/**
	 * To string.
	 *
	 * @return the string
	 */
	@Override
	public String toString() {
		return "SI Time Metric System";
	}

		
	
}