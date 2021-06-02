package ads.assignment3;

/**
*
* Television extended from Appliance
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/
public class Television extends Appliance {
	private int screensize;
	/**
	 * adds screensize
	 * @param brand
	 * @param model
	 * @param basePrice
	 * @param energy
	 * @param screensize
	 */
	public Television(String brand, String model, double basePrice, EnergyEfficiency energy, int screensize) {
		super(brand, model, basePrice, energy);
		this.screensize = screensize;
		// TODO Auto-generated constructor stub
	}
	
	/**
	 * calculates the shipping of the television based on screensize
	 */
	@Override
	public double calculateShipping() {
		if(screensize <= 40 && super.getBasePrice() > 500) return 0;
		if(screensize <= 40 && super.getBasePrice() < 500) return 35;
		else return 35+(screensize-40);
 	}
	

	

}
