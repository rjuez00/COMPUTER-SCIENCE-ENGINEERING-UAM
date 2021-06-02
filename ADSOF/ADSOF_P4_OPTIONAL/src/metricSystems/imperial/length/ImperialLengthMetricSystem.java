package metricSystems.imperial.length;

import java.util.Arrays;

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
public class ImperialLengthMetricSystem extends AbstractMetricSystem implements IMetricSystem{
	
	/** Inches. */
	static public PhysicalUnit INCH = new PhysicalUnit(Quantity.L, 1/12, "in");
	
	/** Foots. */
	static public PhysicalUnit FOOT = new PhysicalUnit(Quantity.L, 1, "ft");
	
	/** Yards. */
	static public PhysicalUnit YARD = new PhysicalUnit(Quantity.L, 3, "yd");
	
	/** Miles. */
	static public PhysicalUnit MILE = new PhysicalUnit(Quantity.L, 5280, "ml");

	/** Stores the unique object (Singleton pattern). */
	static public ImperialLengthMetricSystem SYSTEM = intermediateConstructor();
	
	/**
	 * Intermediate constructor.
	 *
	 * @return ImperialLengthMetricSystem
	 */
	private static ImperialLengthMetricSystem intermediateConstructor() {
		ImperialLengthMetricSystem systemtemp = new ImperialLengthMetricSystem();
		INCH.setMetricSystem(systemtemp);
		FOOT.setMetricSystem(systemtemp);
		YARD.setMetricSystem(systemtemp);
		MILE.setMetricSystem(systemtemp);

		return systemtemp;
	}
	
	/**
	 * Instantiates a new ImperialLengthMetricSystem.
	 */
	private ImperialLengthMetricSystem(){
		super(FOOT,Arrays.asList(INCH, FOOT, YARD, MILE));
	}
	
	/**
	 * To string.
	 *
	 * @return the string
	 */
	@Override
	public String toString() {
		return "Imperial Length Metric System";
	}
	
	
	
	
}