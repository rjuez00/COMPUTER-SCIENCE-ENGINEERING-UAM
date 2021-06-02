package ads.assignment3;

/**
*
* Washer extended from Kitchen Appliance
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/
public class Washer extends KitchenAppliance {
	private double kilosLoad;
	private int rpm;
	
	/**
	 * kitchen appliance constructor
	 * @param brand
	 * @param model
	 * @param basePrice
	 * @param energy
	 * @param dimension
	 * @param weight
	 */
	public Washer(String brand, String model, double basePrice, EnergyEfficiency energy, Dimension dimension,
			double weight) {
		super(brand, model, basePrice, energy, dimension, weight);
		kilosLoad = -1; // doesnt apply
		rpm = -1; // doesnt apply
	}

	/**
	 * adds kilos of load and rpm of the washer
	 * @param brand
	 * @param model
	 * @param basePrice
	 * @param energy
	 * @param dimension
	 * @param weight
	 * @param kilosload
	 * @param rpm
	 */
	public Washer(String brand, String model, double basePrice, EnergyEfficiency energy, Dimension dimension,
			double weight, double kilosload, int rpm) {
		super(brand, model, basePrice, energy, dimension, weight);
		this.kilosLoad = kilosload;
		this.rpm = rpm;
	}

	@Override
	public double calculateShipping() {
		if (super.getWeight() <= 50) {
			return 35;
		} else {
			return 35 + 0.5 * (super.getWeight()-50);
		}

	}
	/**
	 * getter of the kilos that the washer is capable of handling
	 * @return double with kilograms
	 */
	public double getKilosLoad() {
		return kilosLoad;
	}

	/**
	 * getter of the revolutions per minute the washer is capable of achieving
	 * @return integer with rpm
	 */
	public int getRpm() {
		return rpm;
	}

}
