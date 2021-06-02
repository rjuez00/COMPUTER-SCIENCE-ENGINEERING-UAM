package ads.assignment3;

/**
 *
 * Abstract class to store the description of an Article
 *
 * @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz -
 *         juanluis.sanzc@estudiante.uam.es
 *
 *
 */

public abstract class Appliance {
	private EnergyEfficiency energy;
	private String brand;
	private String model;
	private double basePrice;

	/**
	 * Appliance constructor
	 * @param brand
	 * @param model
	 * @param basePrice
	 * @param energy
	 */
	public Appliance(String brand, String model, double basePrice, EnergyEfficiency energy) {
		this.brand = brand;
		this.model = model;
		this.basePrice = basePrice;
		this.energy = energy;
	}
	
	public String toString() {
		return this.getBrand() + " " + this.getModel() + ", " + this.getBasePrice();
	}
	
	/**
	 * calculates the shipping of set appliance
	 * @return double with the shipping price
	 */
	public abstract double calculateShipping();
	
	/**
	 * gets the brand
	 * @return brand string
	 */
	public String getBrand() {
		return brand;
	}

	/**
	 * 
	 * @return energy effiency
	 */
	public EnergyEfficiency getEnergy() {
		return energy;
	}
	
	/**
	 * gets model
	 * @return string model
	 */
	public String getModel() {
		return model;
	}
	
	/**
	 * base price without any discount or additional charges
	 * @return double with price
	 */
	public double getBasePrice() {
		return basePrice;
	}
	
	@Override
	public boolean equals(Object obj) { 
		if (obj == null || obj.getClass() != this.getClass()) return false;

		return  (this.brand.equals((((Appliance) obj).getBrand()))) && 
				(this.model.equals((((Appliance) obj).getModel())));
	}
	
	@Override 
	public int hashCode() {
		return brand.hashCode()*model.hashCode();
	}
	
}
