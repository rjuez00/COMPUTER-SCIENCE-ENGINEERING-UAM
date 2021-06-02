package ads.assignment3;

/**
*
* Refrigerator extended from Kitchen Appliance
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/
public class Refrigerator extends KitchenAppliance {
	boolean nofrost;
	
	
	/**
	 * adds noFrost options 
	 * @param brand
	 * @param model
	 * @param basePrice
	 * @param energy
	 * @param dimension
	 * @param weight
	 * @param nofrost
	 */
	public Refrigerator(String brand, String model, double basePrice, EnergyEfficiency energy, Dimension dimension, double weight, boolean nofrost) {
		super(brand, model, basePrice, energy, dimension, weight);
		this.nofrost = nofrost;
	}
	
	/**
	 * calculates shipping based on dimensions
	 */
	@Override
	public double calculateShipping() {
		double volume3 = super.getDimension().sizex/100 * super.getDimension().sizey/100 * super.getDimension().sizez/100;
		return Math.round(70*volume3);
	}
	
	
}
