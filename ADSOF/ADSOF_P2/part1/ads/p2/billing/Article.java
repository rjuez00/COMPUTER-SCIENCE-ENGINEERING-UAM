package ads.p2.billing;

/**
*
* Abstract class to store the description of an Article
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/

public abstract class Article {
	private long identifier;
	private String description;
	/*base price without taking account anything*/
	private double unitPrice;
	
   /**
   * Builds an object Article
   * @param id id of article
   * @param desc description of article
   * @param price base price without any discount
   */
	public Article(long id, String desc, double price) {
		identifier = id; 
		description = desc; 
		unitPrice = price;
	}
   /**
   * Returns struct in string value
   * @return string with info
   */
	public String toString(){
		return "Id: " + identifier + " " + description + " Price: " + unitPrice;
	}
   /**
   * Getter of the id
   * @return id
   */
	public long getIdentifier() { return identifier; }
   /**
   * Getter of the description
   * @return String
   */
	public String getDescription() { return description; }
   /**
   * Getter of the UnitPrice
   * @return double with unit price
   */
	public double getUnitPrice() { return unitPrice; }
   /**
   * Setter of the description
   * @param desc description
   */
	public void setDescription(String desc) { description = desc; }
   /**
   * Setter of the base price
   * @param price base price
   */	
	public void setUnitPrice(double price) { unitPrice = price; }
   /**
   * Obtains the VAT and is 21% unless specified otherwise in subclasses
   * @return a number between 0 and 1 which contains the VAT
   */	
	public double typeVAT() { return 0.21; }
   /**
   * Every subclass of Article will calculate the corresponding discount
   * @param units double with the cuantity
   * @return double with the amount to discount
   */
	public abstract double discount(double units);
   /**
   * Total price is always calculated in the same way
   * @param units amount of units to buy
   * @return double with the final price that the customer needs to pay
   */
	public double totalPrice(double units) {
		return ((unitPrice * units) - discount(units)) 
                     * (1.0 + typeVAT());
	}
}

