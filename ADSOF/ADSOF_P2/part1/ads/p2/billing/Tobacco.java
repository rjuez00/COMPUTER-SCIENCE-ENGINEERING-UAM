package ads.p2.billing;

/**
*
*  class to store the description of Tobacco
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/
public class Tobacco extends Article {
	/**
   * Builds an object tobacco
   * @param id id of article
   * @param desc description of article
   * @param price base price without any discount
   */
	public Tobacco(long id, String desc, double price) {
		super(id, desc, price);
	}
   /**
   * Calculates the required discount for Tobacco
   * @param units double with the cuantity
   * @return double with the amount to discount
   */
	public double discount(double units) { return 0.0; }
	
}

