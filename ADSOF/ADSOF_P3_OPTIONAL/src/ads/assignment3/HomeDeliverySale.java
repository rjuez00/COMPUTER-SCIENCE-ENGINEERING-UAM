package ads.assignment3;

/**
*
* Used for calculating additional charges from Sale
* 
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/
public class HomeDeliverySale extends Sale {
	protected double shipping;
	
	/**
	 * calculates the shipping on creation
	 * @param bought
	 */
	public HomeDeliverySale(Appliance bought) {
		super(bought);
		shipping = obtainShipping();
		total = obtainTotal();
	}
	/**
	 * calculates the shipping on creation
	 * @param bought
	 * @param returned
	 */
	public HomeDeliverySale(Appliance bought, Appliance returned) {
		super(bought, returned);
		shipping = super.bought.calculateShipping();
		total = super.bought.getBasePrice() - super.discount + shipping;
	}
	
	/**
	 * calculates the cost  for this kind of shipping
	 * @return double with price
	 */
	protected double obtainShipping() {
		return super.bought.calculateShipping();
	}
	
	protected double obtainTotal() {
		return super.bought.getBasePrice() - super.discount + shipping;
	}
	
	
	@Override
	public String getTicket() {
		return toString() + String.format("Shipping Cost:                 %-7.2f Euros", shipping) + String.format("\nTOTAL:                         %-7.2f Euros", super.total) + "\n";

	}
	

}
