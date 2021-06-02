package ads.p2.billing;


/**
*
*  class to store the description of Food an its specific discounts and promos
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/

public class Food extends Article {
	/*boolean to know if the promo is applied*/
	private boolean promo3x2;
   /**
   * Builds an object food
   * @param id id of article
   * @param desc description of article
   * @param price base price without any discount
   * @param promo check if promo is applied
   */
	public Food(long id, String desc, double price, boolean promo) {
		super(id, desc, price);
		promo3x2 = promo;
	}
   /**
   * Get if promo is applied
   * @return new object Book
   */
	public boolean getPromo3x2() { return promo3x2; }
   /**
   * Setter for the application of the promo
   * @param promo boolean
   */
	public void setPromo3x2(boolean promo) { promo3x2 = promo; }
   /**
   * Get VAT applied
   * @return 10% VAT applied
   */
	public double typeVAT() { return 0.10; }
   /**
   * Calculates the required discount for every type of food
   * @param units double with the cuantity
   * @return double with the amount to discount
   */
	public double discount(double units) {
		if (promo3x2) return getUnitPrice() * (int) (units / 3);
		else return 0.0;		
	}
}

