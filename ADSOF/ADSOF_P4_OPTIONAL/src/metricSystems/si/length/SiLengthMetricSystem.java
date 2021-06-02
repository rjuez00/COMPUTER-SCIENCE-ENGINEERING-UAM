package metricSystems.si.length;

import java.util.*;

import metricSystems.IMetricSystem;
import metricSystems.AbstractMetricSystem;
import units.PhysicalUnit;
import units.Quantity;

/**
*
* Class for implementing interface IMetricSystem in length measurements.
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*/
public class SiLengthMetricSystem extends AbstractMetricSystem implements IMetricSystem{
	
	/** Millimeters. */
	static public PhysicalUnit MILLIMETER = new PhysicalUnit(Quantity.L, 0.001, "mm");
	
	/** Meters. */
	static public PhysicalUnit METER = new PhysicalUnit(Quantity.L, 1, "m");
	
	/** Kilometers. */
	static public PhysicalUnit KILOMETER = new PhysicalUnit(Quantity.L, 1000, "km");

	/** Stores the unique object (Singleton pattern). */
	static public SiLengthMetricSystem SYSTEM = intermediateConstructor();
	
	/**
	 * Intermediate constructor.
	 *
	 * @return SiLengthMetricSystem
	 */
	private static SiLengthMetricSystem intermediateConstructor() {
		SiLengthMetricSystem systemtemp = new SiLengthMetricSystem();
		MILLIMETER.setMetricSystem(systemtemp);
		METER.setMetricSystem(systemtemp);
		KILOMETER.setMetricSystem(systemtemp);
		return systemtemp;
	}
	
	/**
	 * Instantiates a new SiLengthMetricSystem.
	 */
	private SiLengthMetricSystem(){
		super(METER,Arrays.asList(KILOMETER, METER, MILLIMETER));
	}
	
	/**
	 * To string.
	 *
	 * @return the string
	 */
	@Override
	public String toString() {
		return "SI Length Metric System";
	}

	
		
}