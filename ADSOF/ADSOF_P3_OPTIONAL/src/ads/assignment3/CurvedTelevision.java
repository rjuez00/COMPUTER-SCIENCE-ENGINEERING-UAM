package ads.assignment3;


/**
*
* Curved Television extended from Television with dimension and weight
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/
public class CurvedTelevision extends Television {
	private double weight;
	private Dimension dim;
	
	/**
	 * adds weight of load and dimension of the washer
	 * @param brand
	 * @param model
	 * @param basePrice
	 * @param energy
	 * @param screensize
	 * @param weight
	 * @param dim
	 **/

	public CurvedTelevision(String brand, String model, double basePrice, EnergyEfficiency energy, int screensize, double weight, Dimension dim) {
		super(brand, model, basePrice, energy, screensize);
		this.weight=weight;
		this.dim=dim;
	}

	/**
	 * gets the dimension of curved televisions
	 * @return double Dimension
	 */
	public Dimension getDimension() {
		return dim;
	}
	
	/**
	 * gets weight of curved televisions
	 * @return double weight
	 */
	public double getWeight() {
		return weight;
	}
	
	/**
	 * calculates shipping based on dimensions
	 */
	@Override
	public double calculateShipping() {
		return super.calculateShipping() + 25 * ((dim.sizex*dim.sizey*dim.sizez)/1000000);	
 	}
	
}
