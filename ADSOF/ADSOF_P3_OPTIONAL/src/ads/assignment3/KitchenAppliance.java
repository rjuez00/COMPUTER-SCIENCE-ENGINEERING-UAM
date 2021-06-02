package ads.assignment3;

/**
*
* Kitchen Appliance extended from Appliance
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/
public abstract class KitchenAppliance extends Appliance {
	private Dimension dimension;
	private double weight;
	
	/**
	 * adds dimensions and weight
	 * @param brand
	 * @param model
	 * @param basePrice
	 * @param energy
	 * @param dimension
	 * @param weight
	 */
	public KitchenAppliance(String brand, String model, double basePrice, EnergyEfficiency energy, Dimension dimension,
			double weight) {
		super(brand, model, basePrice, energy);
		this.dimension = dimension;
		this.weight = weight;
	}

	/*calculates shipping depending on different factors*/
	@Override
	public abstract double calculateShipping();
	
	/**
	 * gets the dimension of washers and refrigerators
	 * @return double Dimension
	 */
	public Dimension getDimension() {
		return dimension;
	}
	
	/**
	 * gets weight of washers and refrigerators
	 * @return double weight
	 */
	public double getWeight() {
		return weight;
	}
	
}
